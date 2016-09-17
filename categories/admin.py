from django.contrib import admin
from categories.models import Category


class CategoryAdmin(admin.ModelAdmin):

    list_display = ('name', 'description', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')

    fieldsets = (
        ("Name and description", {
            'fields': ('name', 'description',),
            'classes': ('wide',)
        }),
        ('Status', {
            'fields': ('active',),
            'classes': ('wide',)
        }),
    )


admin.site.register(Category, CategoryAdmin)
