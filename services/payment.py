import stripe
from abc import ABC, abstractmethod
from config import settings


class StripePayment(ABC):
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.stripe = stripe

    @abstractmethod
    def create(self):
        pass


class CreateProduct(StripePayment):
    """ Создает продукт, возвращает id продукта """
    def __init__(self, name: str = 'no name'):
        super().__init__()
        self.name = name
        self.product = object

    def create(self):
        self.product = stripe.Product.create(name=self.name)

    @property
    def get_id(self) -> str:
        return self.product.id


class CreatePrice(StripePayment):
    """ Создает цену, возвращает id цены """
    def __init__(self, price: int = 1, currency: str = 'RUB', product_id: str = ''):
        super().__init__()
        self.price = price
        self.currency = currency
        self.product_id = product_id
        self.price_obj = object

    def create(self):
        self.price_obj = stripe.Price.create(
            unit_amount=self.price * 100,
            currency=self.currency,
            product=self.product_id
        )

    @property
    def get_id(self) -> str:
        return self.price_obj.id


class CreateDiscount(StripePayment):
    """ Создает скидку, возвращает id скидки """
    def __init__(self, discount: int):
        super().__init__()
        self.discount = discount
        self.coupon = object

    def create(self):
        self.coupon = stripe.Coupon.create(
            percent_off=self.discount,
            duration="once",
        )

    @property
    def get_id(self) -> str:
        return self.coupon.id


class CreateCheckoutSession(StripePayment):
    """ Создает сессию, возвращает сессию """
    def __init__(self, price_id: str, discount_id: str):
        super().__init__()
        self.price_id = price_id
        self.discount_id = discount_id
        self.session = object

    def create(self):
        discount = None
        if self.discount_id:
            discount = [{"coupon": self.discount_id}]
        self.session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[
                {
                    "price": self.price_id,
                    "quantity": 1,
                },
            ],
            discounts=discount,
            mode="payment",
        )

    @property
    def get_session(self) -> object:
        return self.session


class GetPaymentLink:
    def __init__(
            self,
            name: str = "no name",
            price: int | float = 1,
            currency: str = "rub",
            discount: int = 0,
            tax: int = 0
    ):
        self.name = name
        self.price = price
        self.currency = currency
        self.discount = discount
        self.tax = tax

    @property
    def get_session_id(self):
        # Создает продукт
        product = CreateProduct(name=self.name)
        product.create()
        product_id = product.get_id

        # Создает цену
        price = CreatePrice(price=self.price, currency=self.currency, product_id=product_id)
        price.create()
        price_id = price.get_id

        # Создает скидку
        discount_id = None
        if self.discount:
            discount = CreateDiscount(discount=self.discount)
            discount.create()
            discount_id = discount.get_id

        # Создает сессию
        checkout_session = CreateCheckoutSession(price_id=price_id, discount_id=discount_id)
        checkout_session.create()
        session = checkout_session.get_session

        return session
