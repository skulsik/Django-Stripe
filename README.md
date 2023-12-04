# Django-Stripe

Приложение Django-Stripe, предназначено для создания двух сервисов состоящих из:
 - backend части - реализовано приложение на Django, в котором есть произвольные продукты для покупки. Покупка осуществляется посредством Stripe API, так же для внутренних методов используется currencylayer API(курс валют).
 - frontend части - реализовано приложение на Django и JS(Stripe API), так же для визуализации использовался bootstrap.

Приложение содержит:
 - Django-модель `Item` с полями: `name`, `description`, `price`, `currency`. 
 - Django-модель `Order` c полями: `date_time`, `comment`, `discount`, `tax`, `items`.
Добавление, модификация и удаление продуктов и заказов может быть осуществлено через панель администратора.

API данного веб-приложения содержит два ключевых метода:

1. `GET /buy/{id}`, c помощью которого можно получить Stripe Session Id для оплаты выбранного `Item`. При выполнении этого метода c бэкенда с помощью python библиотеки `stripe` должен выполняться запрос `stripe.checkout.Session.create(...)` и полученный `session.id` выдаваться в результате запроса.
2.	`GET /item/{id}`, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном `Item` и кнопка `Buy`. По нажатию на кнопку `Buy` должен происходить запрос на `/buy/{id}`, получение `session_id` и далее с помощью JS библиотеки `Stripe` происходить редирект на Checkout форму `stripe.redirectToCheckout(sessionId=session_id)`

## Реализовано

1. [x] Запуск используя Docker
2. [x] Использование environment variables
3. [x] Просмотр Django Моделей в Django Admin панели
4. [ ] Запуск приложения на удаленном сервере, доступном для тестирования
5. [x] Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
6. [x] Поля Discount, Tax, у модели Order и связь с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме. 
7. [x] Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
8. [ ] Реализовать не Stripe Session, а Stripe Payment Intent.

## Пример

API метод для получения HTML c кнопкой на платежную форму от Stripe для Item с id=1:

```sh
curl -X GET http://localhost:8000/item/1
```

Результат - HTML c инфой и кнопкой:

```html
<html>
  <head>
    <title>Buy Item 1</title>
  </head>
  <body>
    <h1>Item 1</h1>
    <p>Description of Item 1</p>
    <p>1111</p>
    <button id="buy-button">Buy</button>
    <script type="text/javascript">
      var stripe = Stripe('pk_test_a9nwZVa5O7b0xz3lxl318KSU00x1L9ZWsF');
      var buyButton = document.getElementById(buy-button');
      buyButton.addEventListener('click', function() {
        // Create a new Checkout Session using the server-side endpoint 
        // Redirect to Stripe Session Checkout
        fetch('/buy/1', {method: 'GET'})
        .then(response => return response.json())
        .then(session => stripe.redirectToCheckout({ sessionId: session.id }))
      });
    </script>
  </body>
</html>
```

## Запуск проекта руками:
 - Необходимо клонировать проект по ссылке git@github.com:skulsik/Django-Stripe.git
 - В корне проекта необходимо создать виртуальное окружение (папка env): python3 -m venv env
 - Зайти в виртуальное окружение, ввести в консоли: source env/bin/activate 
 - Установить библиотеки из файла requirements.txt: pip install -r requirements.txt
 - Создать фаил .env и прописать в него свои настройки, по шаблону файла .env.sample
 - Зарегистрироваться на stripe.com и currencylayer.com, получить ключи доступа к API для тестирования
 - Создать миграции командой: python3 manage.py makemigrations
 - Применить миграции командой: python3 manage.py migrate
 - Создать супер пользователя: python3 manage.py createsuperuser
 - Запустить сервер с проектом: python manage.py runserver
 - Наслаждаться заполнением контента и тестами сайта

## Запуск проекта Docker:
 - Необходимо клонировать проект по ссылке git@github.com:skulsik/Django-Stripe.git
 - Выполнить команду: docker-compose up -d --build
 - Наслаждаться заполнением контента и тестами сайта

## Использование

В случае контейнеризации, супер пользователь создается автоматически.
Данные доступа, к админ-панели.
```
Username: admin
Email address: admin@pochta.com
Password: admin
```
