from django.db import models
from django.core.exceptions import ValidationError

class Customer(models.Model):
    name = models.CharField(max_length=200, blank=False)
    mobile_no = models.CharField(max_length=20, blank=False, default="")
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(models.Model):
    name = models.CharField(max_length=200, blank=False)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    quantity = models.PositiveIntegerField(blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', blank=False)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.customer.name}"

    def total_amount(self):
        return sum(item.total_price() for item in self.items.all())

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=False)
    quantity = models.PositiveIntegerField(blank=False)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def total_price(self):
        return self.product.selling_price * self.quantity

    def clean(self):
        if self.quantity is None:
            raise ValidationError("Quantity cannot be null.")
        if self.product is None or self.product.quantity is None:
            raise ValidationError("Product quantity cannot be null.")
        if self.quantity > self.product.quantity:
            raise ValidationError(f"Insufficient stock for {self.product.name}")

    def save(self, *args, **kwargs):
        self.clean()
        if not self.pk:
            self.product.quantity -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)
