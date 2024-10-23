from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [reverse('login'), reverse('logout')]  # Προσθέστε το reverse('logout')
        if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
            exempt_urls += [reverse(url) for url in settings.LOGIN_EXEMPT_URLS]

        if not request.user.is_authenticated and request.path not in exempt_urls:
            return redirect('%s?next=%s' % (reverse('login'), request.path))
        response = self.get_response(request)
        return response
 