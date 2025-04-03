"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    # トップページ
    path('', views.IndexListView.as_view()),

    # 管理画面
    path('admin/', admin.site.urls),


    # --------------------
    # アカウント関連ルート
    # --------------------

    # ログイン
    path('login/', views.Login.as_view()),

    # ログアウト
    path('logout/', LogoutView.as_view()),

    # サインアップ
    path('signup/', views.SignUpView.as_view()),

    # アカウント情報
    path('account/', views.AccountUpdateView.as_view()),

    # プロフィール編集
    path('profile/', views.ProfileUpdateView.as_view()),

    # --------------------
    # 注文履歴関連ルート
    # --------------------

    # 注文履歴一覧
    path('orders/<str:pk>/', views.OrderDetailView.as_view()),

    # 注文履歴個別
    path('orders/', views.OrderIndexView.as_view()),


    # --------------------
    # アイテム関連ルート
    # --------------------

    # アイテム個別の詳細ページ
    path('items/<str:pk>/', views.ItemDetailView.as_view()),


    # --------------------
    # カート関連ルート
    # --------------------

    # カートページ
    path('cart/', views.CartListView.as_view()),

    # カートへ追加
    path('cart/add/', views.AddCartView.as_view()),

    # カートから削除
    path('cart/remove/<str:pk>/', views.remove_from_cart),


    # --------------------
    # 支払い関連ルート
    # --------------------
    
    # 支払い処理
    path('pay/checkout/', views.PayWithStripe.as_view()),

    # 支払い成功画面
    path('pay/success/', views.PaySuccessView.as_view()),

    # 支払い失敗画面
    path('pay/cancel/', views.PayCancelView.as_view()),
]
