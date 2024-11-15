from django.utils.deprecation import MiddlewareMixin

from users.models import User


class CustomUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated:
            request.user = User.objects.get(pk=request.user.pk)


__all__ = ()
