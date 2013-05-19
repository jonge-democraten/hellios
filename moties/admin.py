from django.contrib import admin
from moties.models import *

class TagInline(admin.TabularInline):
    model = Motie.tags.through

class CommentInline(admin.TabularInline):
    model = Comment

class MotieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titel','constateringen','overwegingen','uitspraken','toelichting','content','indiener','woordvoerder','indiendatum']}),
        ('Status', {'fields': ['status', 'congres']}),
        ('Overig', {'fields': ['tags',]}),
    ]
    inlines = [
        CommentInline,
        # TagInline,
    ]
    list_display = ('titel', 'status', 'datum', 'congres')
    list_filter = ['datum', 'congres', 'tags']
    search_fields = ['titel', 'content', 'woordvoerder', 'indiener']
    date_hierarchy = 'datum'
    filter_vertical = ('tags',)

admin.site.register(Motie, MotieAdmin)
admin.site.register(Tag)
admin.site.register(Congres)
admin.site.register(Comment)
