from core.enums import Choices


class CategoryChoices(Choices):
    DAILY = "daily"
    MBTI = "mbti"
    FOOD = "food"


class GenderChoices(Choices):
    male = "남성"
    female = "여성"
