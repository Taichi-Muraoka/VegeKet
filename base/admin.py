from django.contrib import admin
from base.models import Item, Category, Tag
from django.contrib.auth.models import Group
 
# タグの新規登録や追加を楽にするための記述
class TagInline(admin.TabularInline):
    model = Item.tags.through
    
 # タグの新規登録や追加を楽にするための記述
class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']
 
 
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.unregister(Group)
