from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title

admin.site.empty_value_display = '-пусто-'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'year',
                    'description', 'category')
    search_fields = ('name', 'year', 'genre', 'category')
    list_filter = ('year',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'text',
                    'author', 'score', 'pub_date')
    search_fields = ('title', 'author')
    list_filter = ('pub_date', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'comment', 'text', 'author', 'pub_date')
    search_fields = ('comment', 'author')
    list_filter = ('pub_date', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
