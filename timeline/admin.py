from django.contrib import admin
from timeline.models import Fact, Timeline, Session

# Register your models here.
admin.site.register(Fact)
admin.site.register(Session)
admin.site.register(Timeline)
