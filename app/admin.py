from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Product, Section, Order, Article, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


class SectionMPTTModelAdmin(MPTTModelAdmin):
    mptt_level_indent = 140

admin.site.register(Section, DraggableMPTTAdmin)
# @admin.register(Section)
# class SectionAdmin(admin.ModelAdmin):
#     pass

@admin.register(Order)
class ProductOrder(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

