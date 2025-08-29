from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return f"Category: {self.name}"
    
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    sku = models.CharField(max_length=100, unique=True)     # Stock Keeping Unit
    unit = models.CharField(max_length=50, default="pcs")   # can be kg, mtr, according to item
    description = models.TextField(blank=True, null=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    # quantity_available = 
    class Meta:
        ordering = ['-updated_on']

    def __str__(self):
        return f"Item: {self.name}, ({self.sku} from category: {self.category})"
    
class Stock(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name="stocks")
    quantity_available = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item.name} - {self.quantity_available} {self.item.unit}"