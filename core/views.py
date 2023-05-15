from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView,
    CreateView,
    ListView,
    View,
    UpdateView,
    DeleteView,
)
from .forms import *
from django.urls import reverse_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CashIn
from django.contrib import messages
from django.conf import settings


from django.db.models import Sum
import locale


# Home View
class HomeView(LoginRequiredMixin, ListView):
    model = CashIn
    template_name = "index.html"
    context_object_name = "dashboard"

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        return qs.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Getting Current Logged In User
        user = self.request.user

        # To get total of amount from model=CashIn => amount of loggedin user
        total = self.get_queryset().aggregate(Sum("amount")).get("amount__sum") or 0
        # To format total returned value in Lakh
        locale.setlocale(locale.LC_ALL, "en_IN")
        formatted_total = locale.format_string("%d", total, grouping=True)
        context["total_cash_in"] = formatted_total

        # To get total of amount from model=CashOut => amount of loggedin user
        cash_out_total = self.get_cash_out_total()
        # To format total returned value in Lakh
        locale.setlocale(locale.LC_ALL, "en_IN")
        formatted_cash_out_total = locale.format_string(
            "%d", cash_out_total, grouping=True
        )
        context["total_cash_out"] = formatted_cash_out_total

        # To get the remaining balnce from cash-in and cash-out
        balance = total - cash_out_total
        # To format total returned value in Lakh
        locale.setlocale(locale.LC_ALL, "en_IN")
        formatted_balance = locale.format_string("%d", balance, grouping=True)
        context["balance"] = formatted_balance
        context["balance_num"] = balance

        # To get transaction histroy of Cash-in
        context["cash_in_items"] = CashIn.objects.filter(user=user).order_by(
            "-date", "-modified_at"
        )[:5]

        # To get transaction histroy of Cash-out
        cash_out = self.get_cash_outflow_items()
        context["cash_out_items"] = cash_out

        # To get total number of Cash-in and Cash-out
        context["cash_in_count"] = len(CashIn.objects.filter(user=user))
        context["cash_out_count"] = len(CashOut.objects.filter(user=user))

        return context

    # Function to Access CashOut
    def get_cash_out_total(self):
        qs = CashOut.objects.filter(user=self.request.user)
        total = qs.aggregate(Sum("amount")).get("amount__sum") or 0
        return total

    # Function to get all entry of CashOut
    def get_cash_outflow_items(self):
        qs = CashOut.objects.filter(user=self.request.user)
        items = qs.all().order_by("-date", "-modified_at")[:5]
        return items


# Cash In and Cash Out View
# CASH IN
class CashInDetail(LoginRequiredMixin, View):
    template_name = "reports/cash_in_detail.html"

    def get(self, requset, *args, **kwargs):
        user = self.request.user
        inflow_items = CashIn.objects.filter(user=user).order_by(
            "-date", "-modified_at"
        )
        return render(requset, self.template_name, {"inflow_items": inflow_items})


# CASH OUT
class CashOutDetail(LoginRequiredMixin, View):
    template_name = "reports/cash_out_detail.html"

    def get(self, request, *args, **kwargs):
        user = self.request.user
        outflow_items = CashOut.objects.filter(user=user).order_by(
            "-date", "-modified_at"
        )
        return render(request, self.template_name, {"outflow_items": outflow_items})


# CRUD Operation for Cash In
# CREATE
class CashInFlow(LoginRequiredMixin, CreateView):
    model = CashIn
    form_class = CashInFLowForm
    template_name = "forms/cash_in_form.html"
    success_url = "/cash-in-detail/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        amount = form.cleaned_data['amount']
        if amount <= 0 :
            messages.error(self.request, "Amount Must Be Greater Than 0")
            return self.form_invalid(form)
        else:
            messages.success(self.request, "Record Has Been Added Successfully")
            return super().form_valid(form)


# UPDATE
class CashInUpdate(LoginRequiredMixin, UpdateView):
    model = CashIn
    form_class = CashInFLowForm
    template_name = "forms/cash_in_form.html"
    success_url = _("cash-in-detail")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Record Has Been Updated Successfully")
        return response


# DELETE
class CashInDelete(LoginRequiredMixin, DeleteView):
    model = CashIn
    template_name = "forms/delete_cash_in.html"
    success_url = _("cash-in-detail")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Record Has Been Deleted Successfully")
        return response


# CRUD Operation for Cash Out
# CREATE
class CashoutFlow(LoginRequiredMixin, CreateView):
    model = CashOut
    form_class = CashOutFlowForm
    template_name = "forms/cash_out_form.html"
    success_url = _("cash-out-detail")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(user=self.request.user)
        return context
    
    
    def form_valid(self, form):
        amount = form.cleaned_data.get("amount")
        mode = form.cleaned_data.get("mode")
        pay_to = form.cleaned_data.get("pay_to")
        category = form.cleaned_data.get("category")
        remarks = form.cleaned_data.get("remarks")
        date = form.cleaned_data.get("date")

        if amount <= 0:
            messages.error(self.request, "Amount Must Be Greater Than 0")
            return self.form_invalid(form)
        else:
            # Save the data to the database
            cash_out = form.save(commit=False)
            cash_out.user = self.request.user
            cash_out.save()

            messages.success(self.request, "Record Has Been Added Successfully")
        return super().form_valid(form)


# UPDATE
class CashOutUpdate(LoginRequiredMixin, UpdateView):
    model = CashOut
    form_class = CashOutFlowForm
    template_name = "forms/cash_out_form.html"
    success_url = _("cash-out-detail")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Record Has Been Updated Successfully")
        return response


# DELETE
class CashOutDelete(LoginRequiredMixin, DeleteView):
    model = CashOut
    template_name = "forms/delete_cash_out.html"
    success_url = _("cash-out-detail")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Record Has Been Deleted Successfully")
        return response


# CRUD Operation for Category
# VIEW
class CategoryView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryAddForm
    success_url = _("category")

    def get(self, request, *args, **kwargs):
        categories = Category.objects.filter(user=self.request.user).order_by("name")
        return render(
            self.request, "reports/category_detail.html", {"categories": categories}
        )


# CREATE
class CategoryAdd(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryAddForm
    template_name = "forms/add_category.html"
    success_url = _("category")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = form.cleaned_data["name"].title()

        category_list = Category.objects.filter(user=form.instance.user)
        if form.cleaned_data["name"].title() not in [
            category.name for category in category_list
        ]:
            response = super().form_valid(form)
            messages.success(self.request, "New Category Added Successfully")
            return response
        else:
            messages.error(self.request, "Category With This Name Is Already Exists")
            return redirect("category")


# UPDATE
class CategoryUpdate(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryAddForm
    template_name = "forms/add_category.html"
    success_url = _("category")

    def form_valid(self, form):
        category_list = Category.objects.all()
        if form.cleaned_data["name"] not in [
            category.name for category in category_list
        ]:
            response = super().form_valid(form)
            messages.success(self.request, "Category Has Been Updated Successfully")
            return response
        else:
            messages.error(self.request, "Category With This Name Is Already Exists")
            return redirect("category")


# DELETE
class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = "forms/delete_category.html"
    success_url = _("category")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Category Has Been Deleted Successfully")
        return response


# Statement View
class Statement(HomeView):
    template_name = "reports/statement.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        credit_items = CashIn.objects.filter(user=self.request.user).order_by(
            "-date", "-modified_at"
        )

        debit_items = CashOut.objects.filter(user=self.request.user).order_by(
            "-date", "-modified_at"
        )
        context["debit_items"] = debit_items

        new_statement = list(credit_items) + list(debit_items)
        new_statement = sorted(new_statement, key=lambda x: (x.date, x.modified_at))

        balance = 0
        for statement in new_statement:
            if isinstance(statement, CashIn):
                balance += statement.amount
            else:
                balance -= statement.amount
            statement.balance = balance

        context["statements"] = new_statement

        return context


# Search Logics
class SearchView(LoginRequiredMixin, View):
    pass


# This will be added later
# Calculator
class CalculatorView(LoginRequiredMixin, TemplateView):
    template_name = "calculator/calculator.html"


# Todo
class TodoView(LoginRequiredMixin, TemplateView):
    template_name = "todo/todo.html"
