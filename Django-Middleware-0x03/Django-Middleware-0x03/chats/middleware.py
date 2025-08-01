import logging
from datetime import datetime, time
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from collections import defaultdict, deque

# Configure logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)

# File handler to write logs to requests.log
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
    

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        allowed_start = time(18, 0)  # 6:00 PM
        allowed_end = time(21, 0)    # 9:00 PM

        # Only restrict /api/messages/ and /api/conversations/ endpoints
        if request.path.startswith('/api/'):
            if not (allowed_start <= current_time <= allowed_end):
                return HttpResponseForbidden("Chat access is restricted at this time. Allowed between 6PM and 9PM.")

        response = self.get_response(request)
        return response
    

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_log = defaultdict(deque)  # {ip_address: deque([timestamp1, timestamp2, ...])}
        self.TIME_WINDOW = 60  # seconds
        self.MESSAGE_LIMIT = 5

    def __call__(self, request):
        # Only apply to message POST requests
        if request.path.startswith('/api/messages/') and request.method == 'POST':
            ip_address = self.get_client_ip(request)
            now = time.time()

            # Remove timestamps older than TIME_WINDOW
            while self.requests_log[ip_address] and now - self.requests_log[ip_address][0] > self.TIME_WINDOW:
                self.requests_log[ip_address].popleft()

            if len(self.requests_log[ip_address]) >= self.MESSAGE_LIMIT:
                return JsonResponse(
                    {'error': 'Rate limit exceeded. Max 5 messages per minute.'},
                    status=429  # HTTP 429 Too Many Requests
                )

            # Log current request timestamp
            self.requests_log[ip_address].append(now)

        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip



class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only enforce on protected endpoints (adjust path as needed)
        protected_paths = ['/api/messages/', '/api/conversations/']

        if any(request.path.startswith(path) for path in protected_paths):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Authentication required.")

            # Assuming user.role field exists with 'admin', 'moderator', 'guest'
            if getattr(user, 'role', None) not in ['admin', 'moderator']:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        response = self.get_response(request)
        return response