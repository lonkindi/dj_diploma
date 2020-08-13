from django.contrib import admin
from mptt.admin import MPTTModelAdmin, DraggableMPTTAdmin
from .models import Product, Section, Order, Article, Review, ArticleRelation, OrderRelation


class RelationshipInlineArticle(admin.TabularInline):
    model = ArticleRelation

class RelationshipInlineOrder(admin.TabularInline):
    model = OrderRelation

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
    inlines = [RelationshipInlineOrder]
    list_display = ('date', 'number', 'user', 'product_count')
    ordering = ['-date']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [RelationshipInlineArticle]
    list_display = ('caption',)



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

