from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from session.models import Player, Session, PlayerSession, Card


class PlayerAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', )
    list_display_links = ('id', 'name', )


class SessionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'state', )
    list_display_links = ('id', 'name', 'state', )


class PlayerSessionAdmin(ImportExportModelAdmin):
    list_display = ('id', 'player', 'session', 'score', 'state', )
    list_display_links = ('id', 'score', )


class CardAdmin(ImportExportModelAdmin):
    list_display = ('id', 'session', 'location', 'player_session', )
    list_display_links = ('id', )


admin.site.register(Player, PlayerAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(PlayerSession, PlayerSessionAdmin)
admin.site.register(Card, CardAdmin)
