from django.urls import path
from api.views import ItemDetail, BuyView, OrderDetail, BuyOrderView
from api.apps import ApiConfig

app_name = ApiConfig.name


urlpatterns = [
    path('item/<int:pk>/', ItemDetail.as_view(), name='item_detail'),
    path('buy/<int:pk>/', BuyView.as_view(), name='buy'),
    path('order/<int:pk>/', OrderDetail.as_view(), name='order'),
    path('buy_order/<int:pk>/', BuyOrderView.as_view(), name='buy_order'),
]
