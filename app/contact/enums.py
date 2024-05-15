from core.enums import Choices


class SNSService(Choices):
    KAKAO = "kakao"
    INSTA = "instagram"


class MessageStatus(Choices):
    ACCEPT = "accept"
    WAIT = "pending"
    REFUSE = "refuse"


class MessageTypeChoices(Choices):
    MESSAGE = "message"
    RING = "ring"
    HEART = "heart"
