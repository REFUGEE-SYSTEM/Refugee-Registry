from openg2p_registry_core.interfaces import G2PPayloadEnricherInterface

from ...register_domain.models import G2PRegisterRefugee


class G2PRefugeeEnricherService(G2PPayloadEnricherInterface):
    def enrich(self, payload: dict) -> dict:
        return payload
