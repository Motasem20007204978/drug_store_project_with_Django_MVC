from django.db import models

# Create your models here.

class QuerySet(models.QuerySet):
    def delete(self):
        self.update(is_active=0)

class Manager(models.Manager):
    def get_queryset(self):
        return QuerySet(model=self.model, using=self._db)

class Drug(models.Model):
    name = models.CharField(max_length=50, unique=True)
    quantity = models.PositiveIntegerField()
    exp_date = models.DateField()
    drug_price = models.DecimalField(max_digits=4, decimal_places=2)
    is_active = models.BooleanField(default=1, editable=False, db_index=True)
    created_at = models.DateTimeField("creation date" ,auto_now_add=True)
    updated_at = models.DateTimeField("updating date", auto_now=True)
    objects = Manager
    
    def set_quantity(self, quantity):
        self.quantity = self.quantity + quantity
        self.save()

    class Meta:
        db_table = "drugs_db"
        