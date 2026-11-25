# ruff: noqa: E402
import asyncio
import logging

from .config import Settings

_config = Settings.get_config()

from openg2p_fastapi_common.app import Initializer as BaseInitializer
from openg2p_registry_core.app import Initializer as CoreInitializer

from .register_domain.models import (
    G2PIntakeFormAddress,
    G2PIntakeFormDisplacementHistory,
    G2PIntakeFormEducationRecord,
    G2PIntakeFormHousehold,
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
    G2PRegisterHistoryHousehold,
    G2PRegisterHistoryIdentityDocument,
    G2PRegisterHistoryOccupationSkill,
    G2PRegisterHistoryRefugee,
    G2PRegisterHistoryRelative,
    G2PRegisterHistorySpecificNeeds,
    G2PRegisterHousehold,
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
    G2PRegisterDomainServiceHousehold,
    G2PRegisterDomainServiceIdentityDocument,
    G2PRegisterDomainServiceOccupationSkill,
    G2PRegisterDomainServiceRefugee,
    G2PRegisterDomainServiceRelative,
    G2PRegisterDomainServiceSpecificNeeds,
)

_logger = logging.getLogger(_config.logging_default_logger_name)


class Initializer(BaseInitializer):
    def initialize(self, **kwargs):
        super().initialize()
        CoreInitializer().initialize()

        G2PRegisterDomainServiceHousehold()
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
                G2PRegisterHousehold,
                G2PRegisterHistoryHousehold,
                G2PIntakeFormHousehold,
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

        asyncio.run(migrate())
