from django.contrib.auth.decorators import permission_required
from django.urls import path
from . import views
from django.views.generic import TemplateView



urlpatterns = [
    #path('login/', views.UserFormView.as_view(), name='login'),           # To make login work correctly 
    path('<int:pk>', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('', views.EmployeeListView.as_view(), name='employee'),
    path('create/', views.EmployeeCreateView, name='create'),
    path('new/', views.ProfileCreateView, name='new_profile'),
    path('profile/', views.Profile, name='profile'),
    path('orgch/', views.EmpOrgnView.as_view(), name='orgchart'),
    path('invoice/', views.EmpInvoiceView.as_view(), name='invoice'),
    path('<int:id>/edit/', views.EmployeeUpdateView, name='update'),
    path('<int:id>/delete/', views.EmployeeDeleteView, name='delete'),
]