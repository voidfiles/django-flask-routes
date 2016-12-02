from django.http import HttpResponse
from .view_collection import api_v1


@api_v1.export('GET', 'hello')
def test(request):
    return HttpResponse('ok')
