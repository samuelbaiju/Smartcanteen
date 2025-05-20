

# Create your models here.
from django.db import models

class MenuItem(models.Model):
    name = models.CharField(max_length=255)  # Ensure this field is required
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)  # Optional field
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User

class Bill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)# Link to the user who placed the order
    items = models.ManyToManyField('MenuItem', through='BillItem')  # Link to the items in the bil
    table_number = models.IntegerField(null=True, blank=True)  # Table number
    payment_method = models.CharField(max_length=20)  # Payment method (e.g., cash, UPI)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Total bill amount
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the bill was created

    def __str__(self):
        return f"Bill #{self.id} - {self.user.username} - ₹{self.total_amount}"
    
class BillItem(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.item.name} (x{self.quantity})"