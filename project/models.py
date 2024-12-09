from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paid_expenses")

    def __str__(self):
        return f"{self.description} - ${self.amount}"


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="budgets", default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="budgets")
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        '''Calculate remaining_budget if not set or if total_budget changes'''
        if not self.pk or self.remaining_budget != self.total_budget:
            self.remaining_budget = self.total_budget
        super().save(*args, **kwargs)

    def __str__(self):
      return f"User: {self.user.username} | Category: {self.category} | Budget: ${self.total_budget}"
