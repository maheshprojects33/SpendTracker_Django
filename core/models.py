from django.db import models
from django.conf import settings



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
# 1 user will have 1 category
# 1 category will have many user
class Category(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name

class CashOut(models.Model):
    PAYMENT_MODE = [
        ("phone_pay", "Phone Pay"),
        ("cash", "Cash"),
        ("card_pay", "Card Pay"),
        ("cheque_pay", "Cheque Pay"),
        ("others", "Others"),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField()
    pay_to = models.CharField(max_length=128)
    remarks = models.CharField(max_length=128)
    date = models.DateField()
    mode = models.CharField(max_length=10, choices=PAYMENT_MODE, default='phone_pay')
    modified_at = models.DateTimeField(auto_now=True)