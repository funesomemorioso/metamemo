from tastypie import fields
from tastypie.resources import ModelResource, Resource, ALL_WITH_RELATIONS
from timeline.models import Fact, Session, Timeline

class TimelineResource(ModelResource):
    class Meta:
        resource_name = 'timeline'
        queryset = Timeline.objects.all()
        filtering = {
            "name" : ('exact',)
        }
    def determine_format(self, request):
        return 'application/json'

class SessionResource(ModelResource):
    timeline = fields.ForeignKey(TimelineResource, 'timeline', full=True)

    class Meta:
        resource_name = 'session'
        queryset = Session.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            "timeline": ALL_WITH_RELATIONS,
        }
    
    def determine_format(self, request):
        return 'application/json'

class FactResource(ModelResource):
    timeline = fields.ForeignKey(TimelineResource, 'timeline', full=True)

    class Meta:
        resource_name = 'fact'
        queryset = Fact.objects.all()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        filtering = {
            "timeline": ALL_WITH_RELATIONS,
        }
    
    def determine_format(self, request):
        return 'application/json'
