from django.contrib import admin
from moties.models import *

class TagInline(admin.TabularInline):
    model = Motie.tags.through

class CommentInline(admin.TabularInline):
    model = Comment

class MotieAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titel','indiener','woordvoerder','constateringen','overwegingen','uitspraken','toelichting','content','indiendatum']}),
        ('Status', {'fields': ['status', 'congres']}),
        ('Overig', {'fields': ['tags','related']}),
    ]
    inlines = [
        CommentInline,
        # TagInline,
    ]
    list_display = ('titel', 'status', 'datum', 'congres')
    list_filter = ['datum', 'congres', 'tags']
    search_fields = ['titel', 'content', 'woordvoerder', 'indiener']
    date_hierarchy = 'datum'
    filter_horizontal = ('tags', 'related')

admin.site.register(Motie, MotieAdmin)
admin.site.register(Tag)
admin.site.register(Congres)
admin.site.register(Comment)
admin.site.register(Standpunt)
admin.site.register(Programma)
admin.site.register(Resultatenboek)
