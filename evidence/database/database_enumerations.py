from enum import StrEnum
from typing import List


class ObjectType(StrEnum):
    GROUP = "Group"
    PERSON = "Person"
    LOCATION = "Location"
    PLACE = "Place"
    TAG = "Tag"


class OperationType(StrEnum):
    CREATE = "Create"
    READ = "Read"
    RENAME = "Rename"
    UPDATE = "Update"
    DELETE = "Delete"
    ADD_DETAIL = "AddDetail"
    REMOVE_DETAIL = "RemoveDetail"


class GroupType(StrEnum):
    COMPANY = "company"
    ORGANIZATION = "organization"
    FAMILY = "family"


class PersonStatus(StrEnum):
    LIVING = "Alive"
    DEAD = "Deceased"
    MISSING = "Missing"
    UNKNOWN = "Unknown"


class LocationType(StrEnum):
    COUNTRY = "country"
    REGION = "region"
    STATE = "state"
    CITY = "city"

    def get_place_types(self) -> List[str]:
        place_types = [
            LocationType.COUNTRY,
            LocationType.REGION,
            LocationType.STATE,
            LocationType.CITY,
        ]
        return place_types
