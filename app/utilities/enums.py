from enum import Enum


class Season(str, Enum):
    summer = "Summer"
    winter = "Winter"


class Sex(str, Enum):
    male = "M"
    female = "F"


class MedalType(str, Enum):
    bronze = "Bronze"
    silver = "Silver"
    gold = "Gold"
