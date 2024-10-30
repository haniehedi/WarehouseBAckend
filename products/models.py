from django.db import models
from accounts.models import User

class Warehouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Ware(models.Model):
    fifo = 'fifo'
    weighted_mean ='weighted_mean'
    COST_METHOD_CHOICES = [
        (weighted_mean, 'Weighted Mean'),
        (fifo, 'FIFO'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    warehouse = models.ForeignKey(Warehouse, related_name='wares', on_delete=models.CASCADE)
    cost_method = models.CharField(max_length=20, choices=COST_METHOD_CHOICES)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    stock = models.PositiveIntegerField(null=True, blank=True)
    def __str__(self):
        return self.name


class Factor(models.Model):
    TYPE_CHOICES = [
        ('input', 'Input'),
        ('output', 'Output'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ware = models.ForeignKey(Ware, related_name='factors', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.type} - {self.quantity}'


