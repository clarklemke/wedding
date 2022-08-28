from django.contrib import admin
from .models import Party, Guest


class GuestInline(admin.TabularInline):
    model = Guest
    fields = (
        "name",
        "attending_canada",
        "attending_france",
        "dietary_restrictions",
    )
    # readonly_fields = ("name", "email")


class PartyAdmin(admin.ModelAdmin):
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


class GuestAdmin(admin.ModelAdmin):
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
