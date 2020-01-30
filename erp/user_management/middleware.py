from django.http import HttpResponseForbidden

class AdminMiddleware:
    def process_request(self, request):
        if request.path == '/admin/':
            if request.user.is_authenticated() and not request.user.is_staff:
                return HttpResponseForbidden('Forbidden')
        return None

