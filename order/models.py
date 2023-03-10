from datetime import datetime
from decimal import Decimal

from django.db import models

from order.constants import (DELIVERY_METHODS,
                             PAYMENT_METHODS,
                             PAYMENT_STATUS, DELIVERY_STATUS, WITHOUT_ACTION)

from catalog.models import Pharmacy
from cart.models import Position
from users.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    positions = models.ManyToManyField(Position, related_name="order", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(choices=DELIVERY_METHODS, max_length=15, null=True, blank=True)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=20, null=True, blank=True)
    payment_status = models.CharField(default="Pending payment", choices=PAYMENT_STATUS,
                                      max_length=20, null=True, blank=True, editable=False)
    delivery_status = models.CharField(max_length=50, choices=DELIVERY_STATUS, default=WITHOUT_ACTION, editable=False)

    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name="orders", null=True, blank=True)
    receipt_date = models.DateField(null=True, blank=True)
    receipt_time = models.TimeField(null=True, blank=True)
    stripe_order_id = models.CharField(max_length=50, null=True, blank=True, editable=False)
    stripe_payment_id = models.CharField(max_length=50, null=True, blank=True, editable=False)
    key = models.CharField(max_length=50, null=True, blank=True)

    is_paid = models.BooleanField(default=False, editable=False)
    in_progress = models.BooleanField(default=False, editable=False)

    closed = models.BooleanField(default=False, editable=False)
    address = models.TextField(null=True, blank=True)
    post_index = models.IntegerField(null=True, blank=True)

    def receipt_datetime(self) -> datetime:
        """
        Combines self-delivery order receipt date and time into one object.
        """
        return datetime.combine(
            self.receipt_date, self.receipt_time
        ) if self.receipt_date and self.receipt_time else None

    @property
    def numb_of_positions(self) -> int:
        return self.positions.count()

    @property
    def total_price(self) -> Decimal:
        order_and_positions = self.positions.prefetch_related("product")
        amounts = [i.amount for i in order_and_positions.all()]
        prices = [i.product.price for i in order_and_positions.all()]
        return sum([i * j for i, j in zip(amounts, prices)])

    @property
    def url(self) -> str:
        return "http://127.0.0.1:8000/orders/{}/{}/".format(self.customer.id, self.id)

    class Meta:
        ordering = ["created_at"]

    def __str__(self) -> str:
        return f"{self.id} order"

    def save(self, *args, **kwargs):
        self.key = f"{(hash(self.created_at))}"[1::5]
        super().save(*args, **kwargs)
