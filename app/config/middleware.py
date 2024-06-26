class JsonContentTypeMiddleware:
    """
    플러터에서 charset=utf-8 없으면 한글이 깨짐
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Content-Type이 application/json인 경우에만 charset=utf-8을 추가합니다.
        if response.get("Content-Type", "").startswith("application/json"):
            response["Content-Type"] = "application/json; charset=utf-8"
        return response
