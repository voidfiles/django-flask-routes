from collections import defaultdict

from django.conf.urls import url
from django.core.urlresolvers import RegexURLResolver
from django.views.decorators.csrf import csrf_exempt


class keydefaultdict(defaultdict):
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret

    def __contains__(self, item):
        actually_contains = super(keydefaultdict, self).__contains__(item)
        if actually_contains:
            return True

        try:
            self.default_factory(item)
            return True
        except:
            return False


def default_handler(request, view_func, view_args, view_kwargs):
    return view_func(request, *view_args, **view_kwargs)


class ViewCollection(object):
    def __init__(self, name, handler=default_handler):
        self.name = name
        self.handler = handler
        # http method -> url patterns for that method
        self.url_patterns = {m: [] for m in ('HEAD', 'GET', 'POST', 'PUT', 'PATCH', 'DELETE')}
        # http method -> url resolver for that method
        self.resolvers = keydefaultdict(lambda method: RegexURLResolver('', self.url_patterns[method]))

    def export(self, method, path, **kwargs):
        "Mark a function is safe to export in a View Collection"

        def _inner(f):
            path_pattern = r'^' + path + r'/?$'

            f.__bound_kwargs = kwargs

            methods = [method]
            if method == 'GET':
                methods.append('HEAD')

            # save this function in the right urlconfs
            for http_method in methods:
                url_patterns = self.url_patterns[http_method]
                url_patterns += [url(path_pattern, f, name=f.__name__)]

            return f

        return _inner

    def _handler(self, request, path):
        view_func, view_args, view_kwargs = self.resolvers[request.method].resolve(path)
        return self.handler(request, view_func, view_args, view_kwargs)

    @property
    def urls(self):

        @csrf_exempt
        def _handler(*args, **kwargs):
            return self._handler(*args, **kwargs)

        return([
            # TODO add self.VERSION to this url instead of all the _handler ones (will change lots of ajax_api stuff)
            url(r'^(?P<path>.+)$', _handler),
        ], self.name, self.name)
