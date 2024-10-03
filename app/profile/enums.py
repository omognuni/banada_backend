from core.enums import Choices


class CategoryChoices(Choices):
    DAILY = "daily"
    MBTI = "mbti"
    FOOD = "food"


class GenderChoices(Choices):
    male = "남성"
    female = "여성"


class ProfileStatus(Choices):
    ACTIVE = "활성화"
    BANNED = "영구 정지"
    TEMP_BANNED = "일시 정지"
