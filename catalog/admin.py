from django.contrib import admin

from catalog.models import Product, Category, Manufacturer, Rating


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "slug",
        "category",
        "price",
        "brand",
        "amount",
        "is_in_stock",
    )
    list_filter = (
        "category",
        "brand",
        "price",
        "amount",
    )
    empty_value_display = "undefined"

@admin.register(Rating)
class RaitingAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "slug",
        "rating_set",
        "average_rating",

    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_subcategory",
        "parent_title",
    )


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "country",
    )
    list_filter = (
        "country",
    )
    empty_value_display = "undefined"

