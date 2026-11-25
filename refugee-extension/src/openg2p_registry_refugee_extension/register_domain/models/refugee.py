from openg2p_registry_core.models import (
    G2PGeo,
    G2PGeoHistory,
    G2PPerson,
    G2PPersonHistory,
    G2PRegister,
    G2PRegisterHistory,
)
from openg2p_registry_core.models.g2p_intake_form import G2PIntakeForm
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from ..services import G2PRegisterDomainServiceRefugee
from .enums import HighestEducationLevelEnum, RelationshipToGroupEnum, ReligionEnum

# TODO: Biometrics (fingerprints, iris, face templates, BIMS history/duplicate flags)
# are out of scope for Step 3 and deferred to a separate integration step.


class G2PRefugee:
    """Domain attributes for Refugee individual (inherits G2PPerson core fields).

    Links to Household via G2PRegister.link_internal_record_id (same pattern as
    Farmer -> Household in farmer-registry). Photo is stored via
    G2PRegister.record_image_document_id.
    """

    relationship_to_group: Mapped[RelationshipToGroupEnum] = mapped_column(
        String, nullable=True
    )
    country_of_origin: Mapped[str] = mapped_column(String, nullable=True)
    fathers_name: Mapped[str] = mapped_column(String, nullable=True)
    mothers_name: Mapped[str] = mapped_column(String, nullable=True)
    highest_education_level: Mapped[HighestEducationLevelEnum] = mapped_column(
        String, nullable=True
    )
    last_occupation: Mapped[str] = mapped_column(String, nullable=True)
    religion: Mapped[ReligionEnum] = mapped_column(String, nullable=True)
    languages_known: Mapped[list] = mapped_column(JSONB, nullable=True)
    place_of_birth: Mapped[str] = mapped_column(String, nullable=True)


class G2PRegisterRefugee(G2PRegister, G2PPerson, G2PGeo, G2PRefugee):
    __tablename__ = "g2p_register_refugees"

    def get_record_name_fields(self) -> str:
        """Return refugee fields used to build record_name."""
        return G2PRegisterDomainServiceRefugee().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return refugee fields used to build search_text."""
        return G2PRegisterDomainServiceRefugee().construct_search_text(self.to_dict())


class G2PRegisterHistoryRefugee(
    G2PRegisterHistory, G2PPersonHistory, G2PGeoHistory, G2PRefugee
):
    __tablename__ = "g2p_register_history_refugees"


class G2PIntakeFormRefugee(
    G2PIntakeForm, G2PRegister, G2PPerson, G2PGeo, G2PRefugee
):
    __tablename__ = "g2p_intake_form_refugees"

    def get_record_name_fields(self) -> str:
        """Return refugee fields used to build record_name."""
        return G2PRegisterDomainServiceRefugee().construct_record_name(self.to_dict())

    def get_search_text_fields(self) -> str:
        """Return refugee fields used to build search_text."""
        return G2PRegisterDomainServiceRefugee().construct_search_text(self.to_dict())
