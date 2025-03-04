from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, PaymentStatusLog


@receiver(post_save, sender=Payment)
def log_payment_status_change(sender, instance, **kwargs):
    if instance.tracker.has_changed('status'):
        PaymentStatusLog.objects.create(
            payment=instance,
            old_status=instance.tracker.previous('status'),
            new_status=instance.status
        )

