from django.conf.urls import *
from tastypie.api import Api

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include


from timeline.api.resources import FactResource, SessionResource, TimelineResource

api = Api(api_name='v1')
api.register(FactResource())
api.register(SessionResource())
api.register(TimelineResource())

urlpatterns = [
    path('api/', include(api.urls)),
]