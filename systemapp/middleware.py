from django.utils.deprecation import MiddlewareMixin
from .models import APIUsageLog

class APIUsageMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = request.user if request.user.is_authenticated else None
        ip_address = request.META.get('REMOTE_ADDR', '')
        endpoint = request.path
        request_method = request.method

        # Create APIUsageLog instance and save it
        APIUsageLog.objects.create(
            user=user,
            endpoint=endpoint,
            request_method=request_method,
            ip_address=ip_address,
        )

        return None
