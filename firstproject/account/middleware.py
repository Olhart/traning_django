from time import timezone
from account.models import Session
from django.utils import timezone

class CheckSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        
        try:
            sessid = request.COOKIES.get('sessid')
            
            for cookie in request.COOKIES:
                session = Session.objects.get(
                key=sessid,
                expires__gte=timezone.now()
            )
            request.custom_session = session
            request.custom_user = session.user
        except Session.DoesNotExist:
            request.custom_session = None
            request.custom_user = None
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response