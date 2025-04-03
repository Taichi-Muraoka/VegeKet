from base.forms import UserCreationForm
from django.contrib import admin
from base.models import Item, Category, Tag, User, Profile, Order
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
 

# タグ追加フィールド
class TagInline(admin.TabularInline):
    model = Item.tags.through
 
# アイテム追加フィールド
class ItemAdmin(admin.ModelAdmin):
    # タグの追加フィールドをインラインで追加している
    inlines = [TagInline]
    exclude = ['tags']
 
# プロフィールの登録フィールド
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
 
# ユーザーの登録フィールド
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (None, {'fields': ('is_active', 'is_admin',)}),
    )
 
    list_display = ('username', 'email', 'is_active',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()
 
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'is_active',)}),
    )
 
    add_form = UserCreationForm
 
    # プロフィールの登録フィールドをインラインに追加している
    inlines = (ProfileInline,)
 
admin.site.register(Order)
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
