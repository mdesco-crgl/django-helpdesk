import warnings
import traceback
import logging
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class WarningTracebackMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Force warnings to become "catchable" during this request
        warnings.filterwarnings("error", category=RuntimeWarning, message=".*received a naive datetime.*")
        return None

    def process_exception(self, request, exception):
        # If the naive datetime error happens, log the URL and the Traceback
        if isinstance(exception, RuntimeWarning) and "received a naive datetime" in str(exception):
            logger.error(f"!!! NAIVE DATETIME DETECTED !!!")
            logger.error(f"URL: {request.build_absolute_uri()}")
            logger.error(f"TRACEBACK:\n{traceback.format_exc()}")

            # Optional: Allow the page to load anyway by returning None
            # after logging, or let it crash so you see it in the browser.
            return None
