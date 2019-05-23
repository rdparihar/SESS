from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic,View 
from django.views.generic import TemplateView
from .forms import UserForm, ProfileForm
from tms.models import TimeRecords
from ems.models import EmpProfile
from lms.models import lms_details

class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "ems/employee_list.html"
    login_url = '/login/'     
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['EmpProfile_list'] = EmpProfile.objects.all()
        return context

    def get_queryset(self):
        if self.request.GET.get('q'):
            try:
                first_name = self.request.GET.get('q')
            except :
                first_name = ''
            if (first_name != ''):
                object_list = self.model.objects.filter(first_name__icontains = first_name)
            else:
                object_list = self.model.objects.all()
        else:
            object_list = self.model.objects.all().exclude(is_superuser = 1)
        return object_list

class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = "ems/employee_detail.html"
    login_url = '/login/'
  
    def get_context_data(self, **kwargs):
        context = super(EmployeeDetailView, self).get_context_data(**kwargs)
        emp_id = self.request.session.get('emp_id')  
        context['tags'] = TimeRecords.objects.all().filter(emp_id = emp_id)
        return context

@login_required(login_url='/login/')
def EmployeeCreateView(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.set_password(obj.password)
        obj.save()
        return redirect('/employee/') 

    context = { 'form' : form }
    template = "ems/registration_form.html"
    return render(request, template, context )

@login_required(login_url='/login/')
def EmployeeUpdateView(request, id):
    obj = get_object_or_404(User, id=id)
    form = UserForm(request.POST or None, instance=obj)
    context = { 'form' : form }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        return HttpResponseRedirect("/employee/{num}".format(num=obj.id))
    template = "ems/employee_update.html"
    return render(request, template, context )

@login_required(login_url='/login/')
def EmployeeDeleteView(request, id=None):
    emp = get_object_or_404(User, id=id) 
    if request.method == "POST":
        emp.delete()
        return HttpResponseRedirect("/employee/")
    context = { "emp" : emp }
    template = "ems/delete-view.html"
    return render(request, template, context )

@login_required(login_url='/login/')
def Profile(request):
    template = "ems/profile.html"
    emp_id = request.session.get('emp_id')
    username = request.session.get('username')
    emp = get_object_or_404(User, username=username)
    lms=lms_details.objects.all().filter(emp_id = emp_id)
    context = { "emp" : emp, "lms" : lms }
    return render(request, template, context )

@login_required(login_url='/login/')
def ProfileCreateView(request):
    username = request.session.get('username')
    form = ProfileForm(request.POST or None)
    context = { 'form' : form }
    userid = User.objects.values("id").get(username=username)
    try:
        userid_1 = EmpProfile.objects.values("emp_con_primary").get(username_id=userid['id'])
        return redirect("/")

    except EmpProfile.DoesNotExist:
        if form.is_valid():
            obj = form.save(commit=False)
            obj.username_id = userid['id']
            obj.save()
            return redirect("/")

    context = { 'form' : form }
    template = "create_profile_form.html"
    return render(request, template, context )

#-------------------------------------NOT IN USE--------------------------------------#
# #Envoice
class EmpInvoiceView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "ems/employee_invoice.html"
    login_url = '/login/'
    context_object_name = 'user'    
 
class EmpOrgnView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "ems/employee_chart.html"
    login_url = '/login/'

    def get_queryset(self):
        if self.request.GET.get('q'):
            try:
                first_name = self.request.GET.get('q')
            except :
                first_name = ''
            if (first_name != ''):
                object_list = self.model.objects.filter(first_name__icontains = first_name)
            else:
                object_list = self.model.objects.all()
        else:
            object_list = self.model.objects.all().exclude(is_superuser = 1)
        return object_list


