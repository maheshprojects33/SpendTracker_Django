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
        # self.fields['type'].label = 'Salary Type'


class CashOutFlowForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)

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
        self.fields["amount"].widget.attrs.update({"class": "form-control"})
        self.fields["mode"].widget.attrs.update({"class": "form-control"})
        self.fields["pay_to"].widget.attrs.update({"class": "form-control"})
        self.fields["category"].widget.attrs.update({"class": "form-control custom-select"})
        self.fields["pay_to"].label = "Pay To"
        self.fields["mode"].label = "Payment Mode"

        self.fields["remarks"].widget.attrs.update({"class": "form-control"})
        self.fields["date"].initial = datetime.date.today()


class CategoryAddForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        
    
    
