from django.conf import settings


def user_context(request):
    return {
        'user': request.user if request.user.is_authenticated else None
    }


