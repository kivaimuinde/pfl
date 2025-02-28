from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import redirect
from django.utils.timezone import now
import datetime

class AutoLogoutMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return  # Skip if user is not logged in

        last_activity = request.session.get('last_activity')

        if last_activity:
            # Convert last_activity back to datetime
            last_activity = datetime.datetime.fromisoformat(last_activity)
            inactive_time = (now() - last_activity).total_seconds()

            if inactive_time > settings.SESSION_COOKIE_AGE:
                from django.contrib.auth import logout as auto_logout
                auto_logout(request)
                request.session.flush()
                return redirect('core:login')  # Redirect to login page

        # Update last activity timestamp as an ISO-formatted string
        request.session['last_activity'] = now().isoformat()
