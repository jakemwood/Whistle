from enum import Enum


class OutgoingBehavior(Enum):
    BLOCK = 0
    ALLOW = 1
    SEEK_PERMISSION_RECIPIENT = 2
    SEEK_PERMISSION_CAREGIVER = 3
    SEEK_ALL_PERMISSION = 4
    BOT_RESPOND = 5


def enum_to_choices(enm):
    return [(x, x.value) for x in enm]
