from django.contrib import admin

# Register your models here.

from .models import Gas, Region, Station, Site, Ship, Harvester, Setup

admin.site.register(Gas)
admin.site.register(Region)
admin.site.register(Station)
#admin.site.register(Site)
#admin.site.register(Ship)
admin.site.register(Harvester)
admin.site.register(Setup)
