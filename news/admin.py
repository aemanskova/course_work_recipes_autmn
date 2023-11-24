from django.contrib import admin

from import_export import resources

from news.models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "datetime_created",)
    list_display_links = ("id", "title", "datetime_created",)
    search_fields = (
        "id",
        "title",
    )
    list_filter = (
        "datetime_created",
    )
    date_hierarchy = "datetime_created"
