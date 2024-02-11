from rest_framework import serializers
from .models import Item, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    category_name = serializers.SerializerMethodField(read_only=True)  # Indicate read-only
    tag_names = serializers.SerializerMethodField(read_only=True)  # Indicate read-only

    class Meta:
        model = Item
        fields = ['id', 'name', 'sku', 'category', 'tags', 'stock_status', 'available_stock', 'created_at', 'updated_at', 'category_name', 'tag_names']

    def get_category_name(self, obj):
        return obj.category.name

    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]

