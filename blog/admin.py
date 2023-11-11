from django.contrib import admin

from blog.models import Comment, Post, Tag


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title', )}
    list_display = ['title', 'published_at',]


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
