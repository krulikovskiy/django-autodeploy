from django.http import JsonResponse
from .utils import add_release


def hook(request):
    add_release()
    return JsonResponse({'status': True})
