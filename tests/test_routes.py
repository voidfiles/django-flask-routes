from django.conf import settings
settings.configure()

import django
django.setup()
from django.urls import RegexURLPattern

from routes import ViewCollection


class MockRequest(object):
    method = 'GET'


def test_view_collection():
    view_collection = ViewCollection('bbb')

    called = {}

    @view_collection.export('GET', '/awesome')
    def test_function(request):
        called['a'] = True

        return 'ok'

    assert isinstance(view_collection.urls[0][0], RegexURLPattern)
    request = MockRequest()
    resp = view_collection._handler(request, '/awesome')
    assert resp == 'ok'
    assert called['a'] == True


def test_handler():
    called = {}

    def test_handler(request, view_func, view_args, view_kwargs):
        called['b'] = True

        return view_func(request, *view_args, **view_kwargs)

    view_collection = ViewCollection('bbb', test_handler)

    @view_collection.export('GET', '/awesome')
    def test_function(request):
        called['a'] = True

        return 'ok'

    request = MockRequest()
    resp = view_collection._handler(request, '/awesome')
    assert resp == 'ok'
    assert called['a'] == True
    assert called['b'] == True
