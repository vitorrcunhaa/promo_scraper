from django.contrib import admin

from match.models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "price",
        "link",
        "coupon",
        "date_match_found",
        "user",
        "image",
    )

