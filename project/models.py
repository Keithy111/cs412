from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal


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
    name = models.CharField(max_length=150, unique=True)
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

    def save(self, *args, **kwargs):
        '''
        Calculate remaining_budget based on total expenses in the category
        during the budget period
        '''
        # Calculate total expenses for this budget's category and profile
        total_expenses = Expense.objects.filter(
            category=self.category,
            profile=self.profile,
            date__gte=self.start_date,
            date__lte=self.end_date
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')

        # Calculate remaining budget
        self.remaining_budget = max(self.total_budget - total_expenses, Decimal('0.00'))

        super().save(*args, **kwargs)

    def __str__(self):
        return f"User: {self.profile.user.username} | Category: {self.category} | Budget: ${self.total_budget}"

    @property
    def is_overspent(self):
        return self.remaining_budget <= 0
    
    def __str__(self):
        return f"User: {self.profile.user.username} | Category: {self.category} | Budget: ${self.total_budget}"