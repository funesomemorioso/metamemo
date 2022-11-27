from django.urls import include, path
from tastypie.api import Api

from timeline.api.resources import FactResource, SessionResource, TimelineResource

api = Api(api_name="v1")
api.register(FactResource())
api.register(SessionResource())
api.register(TimelineResource())

urlpatterns = [
    path("api/", include(api.urls)),
]
