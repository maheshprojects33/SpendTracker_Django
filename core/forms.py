from django import forms
from .models import *
import datetime


class CashInFLowForm(forms.ModelForm):
    class Meta:
        model = CashIn
        exclude = ["modified_at", "user"]
        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "class": "form-control", "format": "%d %b %Y"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["amount"].widget.attrs.update({"class": "form-control"})
        self.fields["mode"].widget.attrs.update({"class": "form-control"})
        self.fields["note"].widget.attrs.update({"class": "form-control"})
        self.fields["type"].widget.attrs.update({"class": "form-control"})

        self.fields["type"].label = "Income Type"
        self.fields["mode"].label = "Income Mode"

        self.fields["date"].initial = datetime.date.today()


class CashOutFlowForm(forms.ModelForm):
    # category = forms.ChoiceField()
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = CashOut
        fields = ["amount", "mode", "pay_to", "category", "remarks", "date"]

        widgets = {
            "date": forms.DateInput(
                attrs={"type": "date", "class": "form-control", "format": "%d %b %Y"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].initial = Category.objects.first()

        self.fields["amount"].widget.attrs.update({"class": "form-control", "placeholder": "Enter Your Payment Amount"})
        self.fields["mode"].widget.attrs.update({"class": "form-control"})
        self.fields["pay_to"].widget.attrs.update({"class": "form-control", "placeholder": "Enter Whom To Pay"})
        self.fields["category"].widget.attrs.update({"class": "form-control"})
        self.fields["remarks"].widget.attrs.update({"class": "form-control", "placeholder": "Enter Your Remarks For Your Payment"})
        self.fields["pay_to"].label = "Pay To"
        self.fields["mode"].label = "Payment Mode"

        self.fields['category'].help_text = "If You Haven't Created Your Category Yet Click on "

        self.fields["date"].initial = datetime.date.today()
    
   
class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
