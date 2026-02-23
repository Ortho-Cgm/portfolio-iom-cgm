# core/middleware.py
from user_agents import parse
from .models import VisitorLog
from django.utils.timezone import now

class VisitorTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # éviter admin / fichiers statiques
        if request.path.startswith("/admin") or request.path.startswith("/static"):
            return response

        ua_string = request.META.get("HTTP_USER_AGENT", "")
        user_agent = parse(ua_string)

        ip = request.META.get("HTTP_X_FORWARDED_FOR")
        if ip:
            ip = ip.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        today = now().date()

        if not VisitorLog.objects.filter(
            ip_address=ip,
            page=request.path,
            visited_at__date=today
        ).exists():
            VisitorLog.objects.create(
            ip_address=ip,
            browser=f"{user_agent.browser.family} {user_agent.browser.version_string}",
            os=f"{user_agent.os.family} {user_agent.os.version_string}",
            device="Mobile" if user_agent.is_mobile else "Tablet" if user_agent.is_tablet else "Desktop",
            user_agent=ua_string,
            page=request.path,
        )

        return response