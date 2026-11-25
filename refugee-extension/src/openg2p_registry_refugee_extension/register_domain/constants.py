"""
Fixed UUIDs for Refugee Registry registers.

Every metadata SQL file (register definitions, sections, schemas, tabs,
intake forms) references these exact UUIDs.

Register Map:
- Household:           a0000000-0000-0000-0000-000000000001  (REGISTER, master=NULL, mints functional ID)
- Refugee:             a0000000-0000-0000-0000-000000000002  (REGISTER, master=NULL, mints functional ID)
- IdentityDocument:    a0000000-0000-0000-0000-000000000003  (TABLE, master=Refugee)
- DisplacementHistory: a0000000-0000-0000-0000-000000000004  (TABLE, master=Refugee)
- SpecificNeeds:       a0000000-0000-0000-0000-000000000005  (TABLE, master=Refugee)
- Relative:            a0000000-0000-0000-0000-000000000006  (TABLE, master=Refugee)
- Address:             a0000000-0000-0000-0000-000000000007  (TABLE, master=Refugee)
- EducationRecord:     a0000000-0000-0000-0000-000000000008  (TABLE, master=Refugee)
- OccupationSkill:     a0000000-0000-0000-0000-000000000009  (TABLE, master=Refugee)
"""

REGISTER_IDS = {
    "Household": "a0000000-0000-0000-0000-000000000001",
    "Refugee": "a0000000-0000-0000-0000-000000000002",
    "IdentityDocument": "a0000000-0000-0000-0000-000000000003",
    "DisplacementHistory": "a0000000-0000-0000-0000-000000000004",
    "SpecificNeeds": "a0000000-0000-0000-0000-000000000005",
    "Relative": "a0000000-0000-0000-0000-000000000006",
    "Address": "a0000000-0000-0000-0000-000000000007",
    "EducationRecord": "a0000000-0000-0000-0000-000000000008",
    "OccupationSkill": "a0000000-0000-0000-0000-000000000009",
}
