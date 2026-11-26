# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_fastapi_common.context import dbengine
from openg2p_registry_core.app import Initializer as CoreInitializer
from sqlalchemy import text
from sqlalchemy.dialects import postgresql

from .photo_support import install_photo_support

from .register_domain.models import (
    G2PIntakeFormAddress,
    G2PIntakeFormDisplacementHistory,
    G2PIntakeFormEducationRecord,
    G2PIntakeFormIdentityDocument,
    G2PIntakeFormOccupationSkill,
    G2PIntakeFormRefugee,
    G2PIntakeFormRelative,
    G2PIntakeFormSpecificNeeds,
    G2PRegisterAddress,
    G2PRegisterDisplacementHistory,
    G2PRegisterEducationRecord,
    G2PRegisterHistoryAddress,
    G2PRegisterHistoryDisplacementHistory,
    G2PRegisterHistoryEducationRecord,
    G2PRegisterHistoryIdentityDocument,
    G2PRegisterHistoryOccupationSkill,
    G2PRegisterHistoryRefugee,
    G2PRegisterHistoryRelative,
    G2PRegisterHistorySpecificNeeds,
    G2PRegisterIdentityDocument,
    G2PRegisterOccupationSkill,
    G2PRegisterRefugee,
    G2PRegisterRelative,
    G2PRegisterSpecificNeeds,
)
from .register_domain.services import (
    G2PRegisterDomainServiceAddress,
    G2PRegisterDomainServiceDisplacementHistory,
    G2PRegisterDomainServiceEducationRecord,
    G2PRegisterDomainServiceIdentityDocument,
    G2PRegisterDomainServiceOccupationSkill,
    G2PRegisterDomainServiceRefugee,
    G2PRegisterDomainServiceRelative,
    G2PRegisterDomainServiceSpecificNeeds,
)

_logger = logging.getLogger(_config.logging_default_logger_name)


async def add_missing_columns(model) -> list[str]:
    """Add the model's columns that its existing table lacks; return their names."""
    table = model.__table__
    dialect = postgresql.dialect()
    async with dbengine.get().begin() as conn:
        existing = set(
            (
                await conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns "
                        "WHERE table_schema = current_schema() AND table_name = :name"
                    ),
                    {"name": table.name},
                )
            ).scalars()
        )
        if not existing:
            return []
        added = []
        for column in table.columns:
            if column.name in existing:
                continue
            ddl = (
                f'ALTER TABLE "{table.name}" ADD COLUMN IF NOT EXISTS "{column.name}" '
                + column.type.compile(dialect=dialect)
            )
            default = column.server_default
            if default is not None:
                value = getattr(default.arg, "text", default.arg)
                ddl += f" DEFAULT {value}"
                if not column.nullable:
                    ddl += " NOT NULL"
            await conn.execute(text(ddl))
            added.append(column.name)
    if added:
        _logger.info("Added columns to %s: %s", table.name, added)
    return added


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        CoreInitializer().initialize()
        install_photo_support()

        G2PRegisterDomainServiceRefugee()
        G2PRegisterDomainServiceIdentityDocument()
        G2PRegisterDomainServiceDisplacementHistory()
        G2PRegisterDomainServiceSpecificNeeds()
        G2PRegisterDomainServiceRelative()
        G2PRegisterDomainServiceAddress()
        G2PRegisterDomainServiceEducationRecord()
        G2PRegisterDomainServiceOccupationSkill()

    def migrate_database(self, args):
        async def migrate():
            _logger.info("Migrating refugee extension database")

            for model in (
                G2PRegisterRefugee,
                G2PRegisterHistoryRefugee,
                G2PIntakeFormRefugee,
                G2PRegisterIdentityDocument,
                G2PRegisterHistoryIdentityDocument,
                G2PIntakeFormIdentityDocument,
                G2PRegisterDisplacementHistory,
                G2PRegisterHistoryDisplacementHistory,
                G2PIntakeFormDisplacementHistory,
                G2PRegisterSpecificNeeds,
                G2PRegisterHistorySpecificNeeds,
                G2PIntakeFormSpecificNeeds,
                G2PRegisterRelative,
                G2PRegisterHistoryRelative,
                G2PIntakeFormRelative,
                G2PRegisterAddress,
                G2PRegisterHistoryAddress,
                G2PIntakeFormAddress,
                G2PRegisterEducationRecord,
                G2PRegisterHistoryEducationRecord,
                G2PIntakeFormEducationRecord,
                G2PRegisterOccupationSkill,
                G2PRegisterHistoryOccupationSkill,
                G2PIntakeFormOccupationSkill,
            ):
                await model.create_migrate()
                await add_missing_columns(model)

        asyncio.run(migrate())
