from django.contrib import admin
from .models import *

# Register your models here.


#news admin
class NewsObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'guid', 'type', 'title_pl', 'link', 'description_pl', 'pub_date', 'image', 'created_at', 'updated_at', 'title_eng', 'description_eng', 'translated')
    list_display_links = ('id', 'guid', 'type', 'title_pl', 'link', 'description_pl', 'pub_date', 'image', 'created_at', 'updated_at', 'title_eng', 'description_eng', 'translated')
    list_filter = ('type', 'translated')
    search_fields = ('type', 'title_pl', 'link', 'description_pl', 'pub_date', 'image', 'title_eng', 'description_eng')
    list_per_page = 25

admin.site.register(NewsObject, NewsObjectAdmin)
