from django.contrib import admin

from posts.models import Post


class PostAdmin(admin.ModelAdmin):

    list_display = ('title', 'owner_name', 'publication_date')
    search_fields = ('name', 'owner_name')

    fieldsets = (
        ("Name and description", {
            'fields': ('title', 'short_description', 'body'),
            'classes': ('wide',)
        }),
        ('Author', {
            'fields': ('owner',),
            'classes': ('wide',)
        }),
        ('Image', {
            'fields': ('image_url',),
            'classes': ('wide',)
        }),
        ('Categories', {
            'fields': ('categories',),
            'classes': ('wide',)
        })
    )

    def owner_name(self, post):
        return "{0} {1}".format(post.owner.first_name, post.owner.last_name)
    owner_name.admin_order_field = 'owner'
    owner_name.short_description = 'Autor'


admin.site.register(Post, PostAdmin)

