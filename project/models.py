from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Sum

# Create your models here.

class Profile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='project_profile')
    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name


class Expense(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="expenses")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField()
    paid_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="paid_expenses")

    def __str__(self):
        return f"{self.description} - ${self.amount}"


class Budget(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="budgets")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name="budgets")
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_expenses = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), editable=False)

    def calculate_total_expenses(self):
        """
        Calculate total expenses for this budget's category and profile
        within the budget period.
        """
        expenses = Expense.objects.filter(
            category=self.category,
            profile=self.profile,
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        return expenses

    def update_budget_metrics(self):
        """
        Update total expenses and remaining budget.
        """
        # Calculate total expenses
        self.total_expenses = self.calculate_total_expenses()
        
        # Calculate remaining budget
        self.remaining_budget = max(self.total_budget - self.total_expenses, Decimal('0.00'))

    def save(self, *args, **kwargs):
        """
        Override save method to update budget metrics before saving.
        """
        self.update_budget_metrics()
        super().save(*args, **kwargs)

    @property
    def is_overspent(self):
        return self.remaining_budget <= 0
    
    def __str__(self):
        return f"User: {self.profile.user.username} | Category: {self.category} | Budget: ${self.total_budget}"