from django.db import models
from django.utils import timezone
from django.db.models import Sum
from decimal import Decimal

# ===================================================================================================
class Supplier(models.Model):
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=70, default='غير محدد')
    date = models.DateField(default=timezone.now().date())
    type = models.CharField(max_length=30, default='عمولة')
    his_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    on_him_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    num_of_containers = models.PositiveIntegerField(default=0)
    
    @property
    def total(self):
        return self.his_money - self.on_him_money
    
    @property  
    def num_of_containers(self):
        return self.container_set.count()
    
    @property
    def his_money(self):
        # Calculate the sum of total_con_price for all associated containers
        return sum(container.total_con_price for container in self.container_set.all()) or Decimal(0)
    
    def __str__(self):
        return self.name
# ===================================================================================================
class Seller(models.Model):
    name = models.CharField(max_length=30)
    place = models.CharField(max_length=70, default='غير محدد')
    date = models.DateField(default=timezone.now().date())
    total_money = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    on_him = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    @property
    def on_him(self):
        payments = Payment.objects.filter(seller=self)
        total_paid = sum((payment.paid_money + payment.forgive or 0) for payment in payments)
        return self.total_money - total_paid
    @property
    def total_money(self):
        return sum(sale.total_sell_price for sale in self.sale_set.all()) or 0
    
    def __str__(self):
        return self.name
# ===================================================================================================
class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now().date())

    def __str__(self):
        return self.name
# ===================================================================================================
class Container(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    type = models.CharField(max_length=30, default='عمولة')
    num_sold_items = models.PositiveIntegerField(blank=True,null=True)
    num_not_sold_items = models.PositiveIntegerField(blank=True,null=True)
    total_con_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    con_weight = models.PositiveBigIntegerField(editable=False,null=True )
    
    commission = models.PositiveIntegerField( blank=True, null=True, default=0)
    carry = models.PositiveIntegerField( blank=True, null=True,default=0)
    tool_rent = models.PositiveIntegerField( blank=True, null=True,default=0)
        
    @property
    def win(self):
        return self.commission + self.carry + self.tool_rent

    @property
    def total_remaining_count(self):
        return self.main_total_count - self.total_sold_count

    @property
    def total_sold_count(self):
        return self.sale_set.aggregate(total_sold_count=Sum('count'))['total_sold_count'] or 0

    @property
    def total_sale_price(self):
        return self.sale_set.aggregate(total_sale_price=Sum('total_sell_price'))['total_sale_price'] or 0

    @property
    def total_sale_weight(self):
        return self.sale_set.aggregate(total_sale_weight=Sum('weight'))['total_sale_weight'] or 0

    @property
    def weight_difference(self):
        return self.total_sale_weight - self.con_weight

    @property
    def price_difference(self):
        return self.total_sale_price - self.total_con_price
    
    @property
    def total_con_price(self):
        return sum(item.total_item_price for item in self.containeritem_set.all()) or 0

    @property
    def con_weight(self):
        return self.containeritem_set.aggregate(total_weight=Sum('item_weight'))['total_weight'] or 0

    @property
    def main_total_count(self):
        return self.containeritem_set.aggregate(total_count=Sum('count'))['total_count'] or 0

    @property
    def num_of_items(self):
        return self.containeritem_set.count()
    
    # calculate the commission
    def save(self, *args, **kwargs):
        if self.commission is not None:
            commission_decimal = Decimal(self.commission)  # Convert to Decimal
            self.commission = (commission_decimal / 100) * self.total_con_price
        super().save(*args, **kwargs)   

    def __str__(self):
        return f"Container {self.id} - {self.date}"
# ===================================================================================================
class ContainerItem(models.Model):  
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()
    tool = models.CharField(max_length=100, default="صناديق")
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)
    item_weight = models.PositiveIntegerField(default=0)
    total_item_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, editable=False)
    remaining_count = models.PositiveIntegerField(editable=False, null=True)

    @property
    def total_item_price(self):
        if self.item_weight and self.price:
            return self.item_weight * self.price
        return None

    def save(self, *args, **kwargs):
        if self.remaining_count is None:
            self.remaining_count = self.count

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.item.name}"
# ===================================================================================================
class Sale(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.SET_NULL, null=True)
    container = models.ForeignKey(Container, on_delete=models.SET_NULL, null=True)
    container_item = models.ForeignKey(ContainerItem, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField()
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_sell_price = models.DecimalField(max_digits=15, decimal_places=2, editable=False)
    tool = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now().date())
    meal = models.DecimalField(max_digits=15, decimal_places=2, editable=False, null=True)

    def save(self, *args, **kwargs):
        try:
            # Ensure that 'count' is a valid numeric type before performing the subtraction
            count = int(self.count)

            # Update remaining_count in the associated ContainerItem
            container_item = self.container_item
            if container_item:
                container_item.remaining_count = max(0, container_item.remaining_count - count)
                container_item.save()

            # Ensure that 'price' and 'weight' are valid numeric types before performing the multiplication
            price = float(self.price)
            weight = float(self.weight)
            self.total_sell_price = price * weight

            # Calculate meal for the same day
            same_day_sales = Sale.objects.filter(date=self.date).aggregate(total_meal=Sum('total_sell_price'))['total_meal']
            self.meal = same_day_sales or self.total_sell_price

        except (TypeError, ValueError):
            # Handle the case where 'count', 'price', or 'weight' is not a valid numeric type
            self.total_sell_price = 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale {self.id} {self.container_item} by {self.seller}"
# ===================================================================================================
class Payment(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    paid_money = models.DecimalField(max_digits=15, decimal_places=2)
    forgive = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    rest = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    notes = models.CharField(max_length=120, blank=True, null=True )
    total_paid = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    temp_rest = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, editable=False)
    
    def save(self, *args, **kwargs):
        # Set temp_rest to the current value of rest before saving
        self.temp_rest = self.rest
        super().save(*args, **kwargs)

    @property
    def total_paid(self):
        return sum(
            (payment.paid_money + payment.forgive or 0)
            for payment in Payment.objects.filter(seller=self.seller)
        )

    @property
    def rest(self):
        return self.seller.total_money - self.total_paid

    def __str__(self):
        return f"{self.id} - {self.date}"

# ===================================================================================================
class Lose(models.Model):
    amount = models.PositiveIntegerField()
    date = models.DateField(default=timezone.now)
    lose_type = models.CharField(max_length=30, default="غير معروف")

    def __str__(self):
        return f"{self.seller} - {self.date}"
# ===================================================================================================
class ContainerExpense(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    expense_type = models.CharField(max_length=30, default="غير معروف")
    expense_notes = models.CharField(max_length=50)

    def __str__(self):
        return f"Expense for Container {self.container.id} - {self.expense_type}"
