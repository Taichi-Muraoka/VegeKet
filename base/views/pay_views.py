from django.shortcuts import redirect
from django.views.generic import View, TemplateView
from django.conf import settings
from stripe.api_resources import tax_rate
from base.models import Item
import stripe
from django.contrib.auth.mixins import LoginRequiredMixin

# stripeのAPIキー
stripe.api_key = settings.STRIPE_API_SECRET_KEY
 
#  支払い完了画面
class PaySuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/success.html'
 
    def get(self, request, *args, **kwargs):
        # 最新のOrderオブジェクトを取得し、注文確定に変更
 
        # カート情報削除
        del request.session['cart']
 
        return super().get(request, *args, **kwargs)
 
# 支払い失敗画面
class PayCancelView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/cancel.html'
 
    def get(self, request, *args, **kwargs):
        # 最新のOrderオブジェクトを取得
 
        # 在庫数と販売数を元の状態に戻す
 
        # is_confirmedがFalseであれば削除（仮オーダー削除）
 
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
            return redirect('/profile/')
        
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            return redirect('/')
 
        line_items = []
        for item_pk, quantity in cart['items'].items():
            item = Item.objects.get(pk=item_pk)
            line_item = create_line_item(
                item.price, item.name, quantity)
            line_items.append(line_item)
 
        checkout_session = stripe.checkout.Session.create(
            # customer_email=request.user.email,
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=f'{settings.MY_URL}/pay/success/',
            cancel_url=f'{settings.MY_URL}/pay/cancel/',
        )
        return redirect(checkout_session.url)