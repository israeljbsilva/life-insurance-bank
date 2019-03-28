import logging

from utils.utils import RequestUtils


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger(__name__)

    def __call__(self, request):
        return self.get_response(request)

    def _should_not_log(self, request):
        return RequestUtils.is_admin_or_api_docs(request) or '/static/' in request.path

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self._should_not_log(request):
            return

        url = request.path

        self.logger.info(f'URL: {url}')

    def process_response(self, request, response):
        response_content = response.content

        try:
            response_body = response_content.decode()
        except UnicodeDecodeError:
            response_body = None

        self.logger.info(f'RESPONSE: {response_body} \t STATUS: {response.status_code}')

        return response
