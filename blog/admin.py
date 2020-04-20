from django.contrib import admin
from .models import  Post,Comment, Welcome

admin.site.register(Post),

admin.site.register(Welcome)


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'score', 'create_date','approved_comment')
    list_filter = ('create_date', 'approved_comment')
    ordering = ('approved_comment','create_date',)