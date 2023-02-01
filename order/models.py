from datetime import timedelta

from django.db import models

from cart.models import Position


class Order(models.Model):
    # Delivery methods
    SELF_DELIVERY = "SELF"
    DOOR_DELIVERY = "DOOR"

    DELIVERY_METHODS = [
        (SELF_DELIVERY, "Self-delivery"),
        (DOOR_DELIVERY, "Door delivery"),
    ]

    # Payments methods
    PREPAYMENT = "PRE"
    UPON_RECEIPT = "PAY"

    PAYMENT_METHODS = [
        (PREPAYMENT, "Prepayment"),
        (UPON_RECEIPT, "Upon receipt"),
    ]

    # Payment status
    PENDING_PAYMENT = "PENDING"
    SUCCESSFULLY_PAID = "SUCCESS"
    UPON_RECEIPT = "UPON_RECEIPT"

    PAYMENT_STATUS = [
        (PENDING_PAYMENT, "Pending payment"),
        (SUCCESSFULLY_PAID, "Successfully paid"),
        (UPON_RECEIPT, "Payment upon receipt"),
    ]

    # Here will be delivery statuses.
    # Need to discuss it with BA team.

    positions = models.ManyToManyField(Position, related_name="order")
    date = models.DateTimeField(auto_now_add=True)
    delivery_method = models.CharField(choices=DELIVERY_METHODS, max_length=15)
    payment_method = models.CharField(choices=PAYMENT_METHODS, max_length=20)
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20)
    address = models.TextField(null=True)
    post_index = models.IntegerField(null=True)

    @property
    def expiration_date(self) -> date:
        """
        Returns the expiration date of the order.
        The order will be automatically reset when the deadline for payment in the day expires.
        """
        return self.date + timedelta(days=1)

    @property
    def numb_of_positions(self) -> int:
        return self.positions.count()

    @property
    def total_price(self):
        positions_for = self.positions
        amounts = [i.amount for i in positions_for.all()]
        prices = [i.product.price for i in positions_for.all()]
        return sum([i * j for i, j in zip(amounts, prices)])

    class Meta:
        ordering = ["date"]

    def __str__(self) -> str:
        return f"{self.id} order"
