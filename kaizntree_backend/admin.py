from django.contrib import admin
from .models import Item, Category, Tag

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'stock_status', 'available_stock')
    list_filter = ('category', 'tags', 'stock_status')
    search_fields = ('name', 'sku')
