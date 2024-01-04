class SensitiveHeadersMiddleware:
    def __init__(self, request):
        self.request = request

    def __call__(self, request):
        self.filter_sensitive_headers(request)
        return self.request(request)

    def filter_sensitive_headers(self, request):
        sensitive_headers = ['Authorization', 'Cookie', 'Set-Cookie', 'WWW-Authenticate', 'Proxy-Authenticate']
        request.filtered_headers = {k: v for k, v in request.headers.items() if k not in sensitive_headers}
