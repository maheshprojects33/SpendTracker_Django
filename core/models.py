from django.db import models
from django.conf import settings


# Create your models here.
class CashIn(models.Model):
    PAYMENT_MODE = [
        ("bank_deposit", "Bank Deposit"),
        ("cash", "Cash"),
        ("phone_pay", "Phone Pay"),
        ("other", "Other"),
    ]
    INCOME_TYPE = [
        ("salary", "Salary"),
        ("loan", "Loan"),
        ("rent", "Rent"),
        ("others", "Others"),
    ]
    amount = models.FloatField()
    type = models.CharField(max_length=6, choices=INCOME_TYPE, default="salary")
    mode = models.CharField(max_length=15,choices=PAYMENT_MODE, default="bank_deposite")
    note = models.CharField(max_length=256)
    date = models.DateField()
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)



# 1 user can have only one profile
# 1 user can add many salary, loan, others

class CashOut(models.Model):
    PAYMENT_MODE = [
        ("phone_pay", "Phone Pay"),
        ("cash", "Cash"),
        ("card_pay", "Card Pay"),
        ("cheque_pay", "Cheque Pay"),
        ("others", "Others"),
    ]

    amount = models.FloatField()
    pay_to = models.CharField(max_length=128)
    remarks = models.CharField(max_length=128)
    date = models.DateField()
    mode = models.CharField(max_length=10, choices=PAYMENT_MODE, default='phone_pay')
    category = models.CharField(max_length=20)

    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Category(models.Model):
    name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return self.name
    
