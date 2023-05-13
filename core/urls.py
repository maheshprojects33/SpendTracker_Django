from django.urls import path
from . import views


urlpatterns = [
    path("home/", views.HomeView.as_view(), name="home"),

    path("cash-in/", views.CashInFlow.as_view(), name="cash-in"),
    path("cash-out/", views.CashoutFlow.as_view(), name="cash-out"),

    path("statement/", views.Statement.as_view(), name="statement"),

    path("cash-in-detail/", views.CashInDetail.as_view(), name="cash-in-detail"),
    path("cash-out-detail/", views.CashOutDetail.as_view(), name="cash-out-detail"),

    path("cash-in-update/<int:pk>/", views.CashInUpdate.as_view(), name="cash-in-update"),
    path("cash-in-delete/<int:pk>/", views.CashInDelete.as_view(), name="cash-in-delete"),

    path("cash-out-update/<int:pk>/",views.CashOutUpdate.as_view(), name="cash-out-update"),
    path("cash-out-delete/<int:pk>/",views.CashOutDelete.as_view(),name="cash-out-delete"),
    
    path("category/", views.CategoryView.as_view(), name="category"),
    path("category-add/", views.CategoryAdd.as_view(), name="category-add"),
    path("category-update/<int:pk>/", views.CategoryUpdate.as_view(), name="category-update"),
    path("category-delete/<int:pk>/", views.CategoryDelete.as_view(), name="category-delete"),

    path('calculator/', views.CalculatorView.as_view(), name='calculator'),
    path('todo/', views.TodoView.as_view(), name='todo'),
]
