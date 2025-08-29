from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("general_manager", "General Manager"),
        ("inventory_manager", "Inventory Manager"),
        ("sales_manager", "Sales Manager"),
        ("user", "User"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

    class Meta:
        ordering = ["role", "id"]

    def __str__(self):
        return f"{self.role}: {self.username}"
    