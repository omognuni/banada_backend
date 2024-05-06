from core.enums import Choices


class SNSService(Choices):
    KAKAO = "kakao"
    INSTA = "instagram"


class MessageStatus(Choices):
    ACCEPT = "승낙"
    REFUSE = "거절"
