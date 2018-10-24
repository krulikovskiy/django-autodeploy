from django.http import JsonResponse
from .utils import add_release, celery, celery_schedule


def hook(request):

    return JsonResponse({'status': True, '123': 123})
