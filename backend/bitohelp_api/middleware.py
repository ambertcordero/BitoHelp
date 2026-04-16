"""Custom middleware for CSRF exemption on API endpoints."""
from django.utils.deprecation import MiddlewareMixin


class CsrfExemptForApiMiddleware(MiddlewareMixin):
    """Middleware that exempts API endpoints from CSRF checks."""
    
    def process_request(self, request):
        if request.path.startswith('/api/'):
            # Mark the request as not requiring CSRF check
            request.csrf_processing_done = True
        return None


# Backward compatibility - function-based middleware
def csrf_exempt_for_api(get_response):
    """Middleware that exempts API endpoints from CSRF checks."""
    middleware = CsrfExemptForApiMiddleware(get_response)
    return middleware
