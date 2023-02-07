from .models import Order, OrderedDrug
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from notifications_app.tasks import create_notification
from django.db.transaction import on_commit
from .tasks import set_drug_quantity, reset_drug_quantity
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=Order)
def set_drugs_quantities(instance, **kwargs):
    if instance.status == "PE":
        on_commit(lambda: set_drug_quantity.delay(instance.id))


@receiver(post_save, sender=Order)
def notify_approving(instance, **kwargs):
    sender = User.objects.get(is_super_user=1)
    if instance.status == "CO":
        data = {
            "sender_id": sender.id,
            "receiver_id": instance.user.id,
            "options": {
                "message": f"the admin has approved your order",
                "order_id": instance.id,
            },
        }
        on_commit(lambda: create_notification.delay(**data))


@receiver(post_delete, sender=OrderedDrug)
def rollback_quantity(instance, **kwargs):
    on_commit(lambda: reset_drug_quantity.delay(instance.id))


@receiver(post_save, sender=Order)
def send_notification(instance, created, **kwargs):
    admin = User.objects.get(is_super_user=1)
    if created:
        data = {
            "sender_id": instance.user.id,
            "receiver_id": admin.id,
            "options": {
                "message": f"the user {instance.user.full_name} asks order",
                "order_id": instance.id,
            },
        }
        on_commit(lambda: create_notification.delay(**data))
