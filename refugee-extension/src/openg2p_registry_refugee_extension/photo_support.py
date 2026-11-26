"""Photo upload and public presigned-URL support for Refugee Registry.

1. Re-signs MinIO presigned GET URLs with MINIO_PUBLIC_ENDPOINT (when set) so
   browsers can fetch objects from localhost:<REFUGEE_MINIO_PORT> instead of
   the Docker-internal `minio:9000` hostname.
2. Syncs section documents labeled `"photo"` to `record_image_document_id` on
   `g2p_intake_form_refugees` and `g2p_register_refugees` during intake save
   and approval, and falls back to `"photo"` in `documents` on record read.
"""

from __future__ import annotations

import logging
import os
from datetime import timedelta

from minio import Minio
from sqlalchemy import text

from .register_domain.constants import REGISTER_IDS

_logger = logging.getLogger(__name__)
_INSTALLED = False


def _patch_minio_public_url() -> None:
    from openg2p_registry_core.helpers.document.minio_client import MinioClient

    orig_init = MinioClient.__init__
    orig_get_url = MinioClient.get_url

    def patched_init(
        self,
        endpoint: str,
        access_key: str,
        secret_key: str,
        secure: bool,
        read_access_key=None,
        read_secret_key=None,
    ):
        orig_init(
            self,
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure,
            read_access_key=read_access_key,
            read_secret_key=read_secret_key,
        )
        public_ep = os.environ.get("MINIO_PUBLIC_ENDPOINT", "").strip()
        if public_ep:
            public_ep = public_ep.removeprefix("http://").removeprefix("https://").rstrip("/")
            self._public_client = Minio(
                endpoint=public_ep,
                access_key=read_access_key or access_key,
                secret_key=read_secret_key or secret_key,
                secure=secure,
                region="us-east-1",
            )
        else:
            self._public_client = None

    def patched_get_url(
        self,
        document_store_id: str,
        bucket,
        expires: timedelta = timedelta(hours=1),
    ) -> str:
        client = getattr(self, "_public_client", None)
        if client is not None:
            return client.presigned_get_object(
                bucket_name=bucket,
                object_name=document_store_id,
                expires=expires,
            )
        return orig_get_url(self, document_store_id, bucket, expires=expires)

    MinioClient.__init__ = patched_init
    MinioClient.get_url = patched_get_url


def _extract_photo_doc_id(documents) -> str | None:
    for doc in documents or []:
        label = getattr(doc, "label", None)
        if label is None and isinstance(doc, dict):
            label = doc.get("label")
        if label == "photo":
            doc_id = getattr(doc, "document_id", None)
            if doc_id is None and isinstance(doc, dict):
                doc_id = doc.get("document_id")
            if doc_id:
                return str(doc_id)
    return None


def _patch_intake_and_register_photo_sync() -> None:
    from openg2p_registry_core.services.g2p_register_service import G2PRegisterService
    from openg2p_registry_core.services.intake_form_data_service import G2PIntakeFormDataService

    refugee_reg_id = REGISTER_IDS["Refugee"]

    orig_upsert_sub_docs = G2PIntakeFormDataService._upsert_submission_section_documents
    orig_upsert_live_docs = G2PIntakeFormDataService._upsert_live_documents

    async def patched_upsert_sub_docs(self, submission, section_id, documents, session):
        await orig_upsert_sub_docs(self, submission, section_id, documents, session)
        photo_id = _extract_photo_doc_id(documents)
        if photo_id and getattr(submission, "register_id", None) == refugee_reg_id:
            await session.execute(
                text(
                    "UPDATE g2p_intake_form_refugees "
                    "SET record_image_document_id = :doc_id "
                    "WHERE internal_record_id = :rec_id"
                ),
                {"doc_id": photo_id, "rec_id": str(submission.submission_id)},
            )

    async def patched_upsert_live_docs(
        self, submission, section, internal_record_id, documents, session
    ):
        await orig_upsert_live_docs(
            self, submission, section, internal_record_id, documents, session
        )
        photo_id = _extract_photo_doc_id(documents)
        if photo_id and getattr(submission, "register_id", None) == refugee_reg_id:
            await session.execute(
                text(
                    "UPDATE g2p_register_refugees "
                    "SET record_image_document_id = :doc_id "
                    "WHERE internal_record_id = :rec_id"
                ),
                {"doc_id": photo_id, "rec_id": str(internal_record_id)},
            )

    G2PIntakeFormDataService._upsert_submission_section_documents = patched_upsert_sub_docs
    G2PIntakeFormDataService._upsert_live_documents = patched_upsert_live_docs

    if hasattr(G2PRegisterService, "get_record_data"):
        orig_get_record_data = G2PRegisterService.get_record_data

        async def patched_get_record_data(self, *args, **kwargs):
            res = await orig_get_record_data(self, *args, **kwargs)
            if res is not None and not getattr(res, "record_image_document_id", None):
                photo_id = _extract_photo_doc_id(getattr(res, "documents", None))
                if photo_id:
                    res.record_image_document_id = photo_id
                    for doc in getattr(res, "documents", None) or []:
                        if getattr(doc, "document_id", None) == photo_id and getattr(
                            doc, "presigned_url", None
                        ):
                            res.record_image_url = doc.presigned_url
                            break
            return res

        G2PRegisterService.get_record_data = patched_get_record_data


def install_photo_support() -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    _INSTALLED = True
    _patch_minio_public_url()
    _patch_intake_and_register_photo_sync()
    _logger.info("Installed refugee photo upload and public MinIO URL support")
