from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from api.models import Item, Order
from services.payment import GetPaymentLink
from services.utils import summ_price


class ItemDetail(APIView):
    """
        Получение элемента из БД по id, посредством Get
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/item_detail.html'

    def get(self, request, pk) -> Response:
        item = get_object_or_404(Item, pk=pk)
        object_dict = {
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'currency': item.currency,
            'pk': pk,
        }
        return Response(object_dict)


class BuyView(APIView):
    """
        Получение элемента из БД по id, посредством Get.
        Возврат session id.
    """
    def get(self, request, pk) -> Response:
        item = get_object_or_404(Item, pk=pk)
        payment_link = GetPaymentLink(name=item.name, price=item.price, currency=item.currency)
        session: str = payment_link.get_session_id
        return Response(session)


class OrderDetail(APIView):
    """
        Заказ. Получение элемента из БД по id, посредством Get
    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/order_detail.html'

    def get(self, request, pk) -> Response:
        order = get_object_or_404(Order, pk=pk)
        items = list(order.items.all())
        total_price = summ_price(items)
        comment: str = "нет"
        if order.comment:
            comment = order.comment
        object_dict = {
            'date_time': order.date_time,
            'comment': comment,
            'discount': order.discount,
            'tax': order.tax,
            'items': items,
            'total_price': total_price,
            'pk': pk,
        }

        return Response(object_dict)


class BuyOrderView(APIView):
    """
        Получение элемента из БД по id, посредством Get.
        Возврат session id.
    """
    def get(self, request, pk) -> Response:
        order = get_object_or_404(Order, pk=pk)
        items = list(order.items.all())
        total_price = summ_price(items)
        payment_link = GetPaymentLink(
            name='Итого к оплате',
            price=total_price,
            currency='RUB',
            discount=order.discount
        )
        session: str = payment_link.get_session_id
        return Response(session)
