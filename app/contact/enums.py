from core.enums import Choices


class SNSService(Choices):
    KAKAO = "kakao"
    INSTA = "instagram"


class MessageStatus(Choices):
    ACCEPTED = "accepted"
    WAIT = "pending"
    REFUSED = "refused"
    EXPIRED = "expired"


class MessageTypeChoices(Choices):
    MESSAGE = "message"
    RING = "ring"
    HEART = "heart"
