from django.contrib import admin

from main_app.models import Label, Artist, Album


# Register your models here.

@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'headquarters', 'market_share']
    list_filter = ['market_share']
    search_fields = ['name']
    readonly_fields = ['created_at']


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'awards']
    list_filter = ['awards']
    search_fields = ['name', 'nationality']
    readonly_fields = ['created_at']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'release_date', 'description', 'type', 'is_hit', 'label']
    list_filter = ['is_hit', 'type']
    search_fields = ['title', 'label__name']
    readonly_fields = ['created_at']
