from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Order


@receiver(pre_save, sender=Order)
def update_product_stock(sender, instance, **kwargs):
    if instance.pk and instance.status_changed_to('completed'):
        for item in instance.items.all():
            item.product.stock -= item.quantity
            item.product.save()


@receiver(post_save, sender=Order)
def create_status_history(sender, instance, created, **kwargs):
    if not created and instance.tracker.has_changed('status'):
        from .models import OrderStatusHistory
        OrderStatusHistory.objects.create(
            order=instance,
            status=instance.status
        )

# @receiver(post_save, sender=Order)
# def send_status_notification(sender, instance, **kwargs):
#     if instance.tracker.has_changed('status'):
#         from .tasks import send_order_status_notification
#         send_order_status_notification.delay(instance.pk)
