from django.contrib import admin
from .models import (
    ExeclusiveApplied, NewsLetterModel, PeeksModel, Region, PeeksLists,
    PeeksLocation, PopularPeaks, PeeeksHighlights, PeeeksItenary,
    PeeekIncludeExclude, BookaTour, CommentsTours, ContactUsModel,
    DealsLists, FAQLists, BlogCategory, Blogs, Certificates, InstagramPost, Teams
)


class ExeclusiveAppliedAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'updated_at')
    search_fields = ('email',)


class NewsLetterModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at', 'updated_at')
    search_fields = ('email',)


class PeeksModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


class PeeksListsAdmin(admin.ModelAdmin):
    list_display = ('name', 'peek_type', 'grade', 'rating', 'price', 'created_at')
    list_filter = ('peek_type', 'grade', 'region_peak')
    search_fields = ('name',)
    ordering = ('-created_at',)


class PeeksLocationAdmin(admin.ModelAdmin):
    list_display = ('peek_info', 'location_frame', 'created_at', 'updated_at')
    search_fields = ('peek_info__name',)


class PopularPeaksAdmin(admin.ModelAdmin):
    list_display = ('title', 'offer', 'price', 'popular_last_month', 'created_at')
    list_filter = ('popular_last_month',)
    search_fields = ('title', 'peek_info__name')


class PeeeksHighlightsAdmin(admin.ModelAdmin):
    list_display = ('peek_info', 'created_at', 'updated_at')
    search_fields = ('peek_info__name',)


class PeeeksItenaryAdmin(admin.ModelAdmin):
    list_display = ('peek_info', 'day', 'title', 'created_at', 'updated_at')
    search_fields = ('peek_info__name', 'title')


class PeeekIncludeExcludeAdmin(admin.ModelAdmin):
    list_display = ('peek_info', 'inc_type', 'name', 'created_at', 'updated_at')
    list_filter = ('inc_type',)
    search_fields = ('peek_info__name', 'name')


class BookaTourAdmin(admin.ModelAdmin):
    list_display = ('peek_info', 'name', 'email', 'phone', 'country', 'arrival_time', 'departure_date', 'created_at')
    search_fields = ('peek_info__name', 'name', 'email')
    ordering = ('-created_at',)



class CommentsToursAdmin(admin.ModelAdmin):
    list_display = ('peek_info', 'blogs', 'name', 'email', 'title', 'created_at')
    search_fields = ('peek_info__name', 'blogs__title', 'name', 'email')
    ordering = ('-created_at',)


class ContactUsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at')
    search_fields = ('name', 'email', 'phone')
    ordering = ('-created_at',)


class DealsListsAdmin(admin.ModelAdmin):
    list_display = ('peek_info', 'till', 'percentage', 'created_at', 'updated_at')
    search_fields = ('peek_info__name',)


class FAQListsAdmin(admin.ModelAdmin):
    list_display = ('questions', 'created_at', 'updated_at')
    search_fields = ('questions',)


class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'category__name')
    ordering = ('-created_at',)


class CertificatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'updated_at')
    search_fields = ('name',)


admin.site.register(InstagramPost)

admin.site.register(ExeclusiveApplied, ExeclusiveAppliedAdmin)
admin.site.register(NewsLetterModel, NewsLetterModelAdmin)
admin.site.register(PeeksModel, PeeksModelAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(PeeksLists, PeeksListsAdmin)
admin.site.register(PeeksLocation, PeeksLocationAdmin)
admin.site.register(PopularPeaks, PopularPeaksAdmin)
admin.site.register(PeeeksHighlights, PeeeksHighlightsAdmin)
admin.site.register(PeeeksItenary, PeeeksItenaryAdmin)
admin.site.register(PeeekIncludeExclude, PeeekIncludeExcludeAdmin)
admin.site.register(BookaTour, BookaTourAdmin)
admin.site.register(CommentsTours, CommentsToursAdmin)
admin.site.register(ContactUsModel, ContactUsModelAdmin)
admin.site.register(DealsLists, DealsListsAdmin)
admin.site.register(FAQLists, FAQListsAdmin)
admin.site.register(BlogCategory, BlogCategoryAdmin)
admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Certificates, CertificatesAdmin)

@admin.register(Teams)
class TeamsAdmin(admin.ModelAdmin):
    list_display = ("priority", "name", "position", "thumbnail_preview")
    search_fields = ("name", "position")
    ordering = ("priority",)

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return f'<img src="{obj.thumbnail.url}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />'
        return "No Image"
    thumbnail_preview.allow_tags = True
    thumbnail_preview.short_description = "Thumbnail"