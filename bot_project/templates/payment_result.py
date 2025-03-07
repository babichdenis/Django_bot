{% extends 'base.html' %}

{% block content %}
<div class="container">
    <h1 class="mb-4">Результат оплаты</h1>

    {% if payment_success %}
    <div class="alert alert-success" role="alert">
        <h4 class="alert-heading">Оплата прошла успешно!</h4>
        <p>Ваш заказ №{{ order.id }} успешно оплачен. Спасибо за покупку!</p>
        <hr>
        <p class="mb-0">Мы отправим вам уведомление, когда заказ будет готов к отправке.</p>
    </div>
    {% else %}
    <div class="alert alert-danger" role="alert">
        <h4 class="alert-heading">Оплата не прошла.</h4>
        <p>При обработке вашего платежа произошла ошибка. Пожалуйста, попробуйте еще раз.</p>
        <hr>
        <p class="mb-0">
            <a href="/order-payment/{{ order.id }}" class="alert-link">Попробовать снова</a>
        </p>
    </div>
    {% endif %}

    <a href="/" class="btn btn-primary">Вернуться на главную</a>
</div>
{% endblock %}
