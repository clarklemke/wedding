from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Guest, Party


class PartyResource(resources.ModelResource):
    class Meta:
        model = Party


class GuestInline(admin.TabularInline):
    model = Guest
    fields = (
        "name",
        "attending_canada",
        "attending_france",
        "dietary_restrictions",
    )
    # readonly_fields = ("name", "email")


class PartyAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "email",
        "save_the_date_sent",
        "save_the_date_viewed",
        "invite_sent",
        "invite_viewed",
    )
    list_filter = (
        "save_the_date_sent",
        "save_the_date_viewed",
        "invite_sent",
        "invite_viewed",
    )
    inlines = [GuestInline]
    readonly_fields = (
        "save_the_date_sent",
        "save_the_date_viewed",
        "invite_sent",
        "invite_viewed",
    )


class GuestAdmin(ImportExportModelAdmin):
    list_display = (
        "name",
        "party",
        "attending_canada",
        "attending_france",
        "dietary_restrictions",
    )
    list_filter = ("attending_canada", "attending_france", "dietary_restrictions")


admin.site.register(Party, PartyAdmin)
admin.site.register(Guest, GuestAdmin)
