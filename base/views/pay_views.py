from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from stripe.api_resources import tax_rate
from base.models import Item, Order
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
import json
from django.contrib import messages


# stripeのAPIキー
stripe.api_key = settings.STRIPE_API_SECRET_KEY
 
#  支払い完了画面
class PaySuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/success.html'
 
    def get(self, request, *args, **kwargs):
        # checkout_sessionで処理された注文IDを取得
        order_id = request.GET.get('order_id')

        # 注文が見つからない場合はエラーメッセージを表示(複数ある場合も)
        orders = Order.objects.filter(user=request.user,pk=order_id)
        if len(orders) != 1:
            messages.error(request, '注文が見つかりません。')
            return super().get(request, *args, **kwargs)

        # 最新のOrderオブジェクトを取得し、注文確定に変更
        order = orders[0]

        # すでに注文確定されている場合はエラーメッセージを表示
        if order.is_confirmed:
            messages.error(request, 'すでに注文確定されています。')
            return super().get(request, *args, **kwargs)

        order.is_confirmed = True  # 注文確定
        order.save()
 
        # カート情報削除
        if 'cart' in request.session:
            del request.session['cart']
 
        return super().get(request, *args, **kwargs)
 
# 支払い失敗画面
class PayCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/cancel.html'
 
    def get(self, request, *args, **kwargs):
        # ログインユーザーの仮注文を取得
        orders = Order.objects.filter(user=request.user,is_confirmed=False)

        for order in orders:
            # 在庫数と販売数を元の状態に戻す
            for elem in json.loads(order.items):
                item = Item.objects.get(pk=elem['pk'])
                item.sold_count -= elem['quantity']
                item.stock += elem['quantity']
                item.save()
 
        # 仮注文を削除
        orders.delete()
 
        return super().get(request, *args, **kwargs)
 
# 消費税
tax_rate = stripe.TaxRate.create(
    display_name='消費税',
    description='消費税',
    country='JP',
    jurisdiction='JP',
    percentage=settings.TAX_RATE * 100,
    inclusive=False,  # 外税を指定（内税の場合はTrue）
)
 
# 商品情報
def create_line_item(unit_amount, name, quantity):
    return {
        'price_data': {
            'currency': 'JPY',
            'unit_amount': unit_amount,
            'product_data': {'name': name, }
        },
        'quantity': quantity,
        'tax_rates': [tax_rate.id]
    }
 
# プロフィールの情報が欠如していないかチェックする関数
def check_profile_filled(profile):
    if profile.name is None or profile.name == '':
        return False
    elif profile.zipcode is None or profile.zipcode == '':
        return False
    elif profile.prefecture is None or profile.prefecture == '':
        return False
    elif profile.city is None or profile.city == '':
        return False
    elif profile.address1 is None or profile.address1 == '':
        return False
    return True

# 支払い処理
class PayWithStripe(LoginRequiredMixin, View):
 
    def post(self, request, *args, **kwargs):
        # プロフィールが埋まっているかどうか確認
        if not check_profile_filled(request.user.profile):
            messages.error(request, '配送のためプロフィールを埋めてください。')
            return redirect('/profile/')
 
        # カートが空であればトップページに飛ばす
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            messages.error(request, 'カートが空です。')
            return redirect('/')
 
        items = []  # Orderモデル用に追記
        line_items = []
        for item_pk, quantity in cart['items'].items():
            item = Item.objects.get(pk=item_pk)
            line_item = create_line_item(
                item.price, item.name, quantity)
            line_items.append(line_item)
 
            # Orderモデル用に追記
            items.append({
                'pk': item.pk,
                'name': item.name,
                'image': str(item.image),
                'price': item.price,
                'quantity': quantity,
            })
 
            # 在庫をこの時点で引いておく、注文キャンセルの場合は在庫を戻す
            # 販売数も加算しておく
            item.stock -= quantity
            item.sold_count += quantity
            item.save()
 
        # 仮注文を作成（is_confirmed=Flase)
        order = Order.objects.create(
            user=request.user,
            uid=request.user.pk,
            items=json.dumps(items),
            shipping=serializers.serialize("json", [request.user.profile]),
            amount=cart['total'],
            tax_included=cart['tax_included_total']
        )
 
        checkout_session = stripe.checkout.Session.create(
            customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.MY_URL}/pay/success/?order_id={order.pk}',
            cancel_url=f'{settings.MY_URL}/pay/cancel/?order_id={order.pk}',
        )
        return redirect(checkout_session.url)