from django.contrib.sessions.models import Session

from store.models import SiteStats


class VisitorsTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        site_stats, created = SiteStats.objects.get_or_create(id=1)
        user = request.user
        if user.is_authenticated:
            site_stats.auth_visitors.add(request.user)
        else:
            if not request.session.get("has_visited"):
                request.session["has_visited"] = True
                site_stats.anonymous_visitor_count += 1
                site_stats.save()
        response = self.get_response(request)
        return response
