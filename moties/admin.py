from django.contrib import admin
from moties.models import *

class TagInline(admin.TabularInline):
    model = Motie.tags.through

class MotieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titel','content','indiener','woordvoerder','indiendatum']}),
        ('Status', {'fields': ['status', 'congres']}),
        ('Overig', {'fields': ['hoofdstuk', 'tags']}),
    ]
    inlines = [
        # TagInline,
    ]
    list_display = ('titel', 'status', 'datum', 'congres')
    list_filter = ['datum', 'congres', 'tags']
    search_fields = ['titel', 'content', 'woordvoerder', 'indiener']
    date_hierarchy = 'datum'

admin.site.register(Motie, MotieAdmin)
admin.site.register(Hoofdstuk)
admin.site.register(Tag)
admin.site.register(Congres)
