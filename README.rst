Django Flask Routes: Fast Functional Serializers
================================================

This is a package that lets you do flask like
routing in Django.


.. code-block:: python

    from django.http import HttpRequest
    from routes import ViewCollection

    view_collection = ViewCollection('view')

    view_collection.export('GET', '/awesome')
    def view(request):
        return HttpRequest('ok')


Now you can make a GET request to /awesome
