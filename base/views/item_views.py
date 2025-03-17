from django.shortcuts import render
from django.views.generic import ListView, DetailView
from base.models import Item

# トップページのアイテムリスト
class IndexListView(ListView):
    model = Item
    template_name = 'pages/index.html'

# アイテムの詳細ページ
class ItemDetailView(DetailView):
    model = Item
    template_name = 'pages/item.html'