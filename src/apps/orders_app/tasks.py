from celery import shared_task
from .models import Order, OrderedDrug
from drugs_app.models import Drug


@shared_task(name="set_drug_quantity")
def set_drug_quantity(oid):
    instance = Order.objects.get(id=oid)
    ordered_drugs = OrderedDrug.objects.filter(order=instance)
    for o_d in ordered_drugs:
        o_d.drug.set_quantity(-o_d.quantity)
    return "drugs quantities is set successfully"


@shared_task(name="reset_drug_quantity")
def reset_drug_quantity(odid):
    ordered_drug = OrderedDrug.objects.get(id=odid)
    ordered_drug.drug.set_quantity(ordered_drug.quantity)
    return "drug quantity is reset successfully"