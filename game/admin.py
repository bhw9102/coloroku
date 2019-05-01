from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from game.models import CardClass


class CardClassAdmin(ImportExportModelAdmin):
    list_display = ('id', 'color_front', 'color_back', 'count',)
    list_display_links = ('id', )


admin.site.register(CardClass, CardClassAdmin)

