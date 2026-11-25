from typing import Optional


class G2PGeoAddressLinesSchema:
    """address_line_1 / address_line_2 for register and intake schemas using G2PGeo.

    G2PGeo ORM model has both columns, while G2PGeoSchema omits them.
    """

    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
