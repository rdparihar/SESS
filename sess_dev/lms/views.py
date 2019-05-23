from django.contrib.auth.models import User
from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, TemplateView
import datetime
from ems.models import EmpProfile
from ems.views import ProfileCreateView
from .forms import lmsCreateForm,lmsViewForm,lmsUpdateForm,lmsApproveForm
from .models import lms_details

class lmsList(LoginRequiredMixin, ListView):
    model = lms_details
    login_url = '/login/'
    template_name = "lms/lms_list.html"
    context_object_name = 'lms' 
    

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            print(context)
            emp_id = self.request.session.get('emp_id')
            print (emp_id)
            context['EmpUser_list'] = EmpProfile.objects.all()
            context['User_detail'] = User.objects.all()
            context['lms'] = lms_details.objects.filter(emp_id = emp_id)
            
                
           
            context['lms_approved']=lms_details.objects.all().filter(emp_id = emp_id,ls_status = 'A')
            y = datetime.datetime.now().year 
            print(context)
            context['year_range'] = range(y-3, y+2)
            

          
            if self.request.GET.get('q'):
                q = self.request.GET.get('q')
                emp_id = self.request.session.get('emp_id')
                print(emp_id)
                
                context['lms'] = self.model.objects.filter(emp_id = emp_id).filter(ls_date__icontains = q)
                if q is '0':
                    context['year'] = 'All'
                    return context

                context['year'] = q
                return context
            return context

class lmsCreate(LoginRequiredMixin, CreateView):
    model = lms_details
    login_url = '/login/'
    form_class = lmsCreateForm
    success_url = reverse_lazy('lmsList')
    template_name = "lms/lms_create.html"

class lmsUpdate(LoginRequiredMixin, UpdateView):
    model = lms_details
    login_url = '/login/' 
    form_class = lmsUpdateForm
    template_name = "lms/lms_update.html"
    success_url = reverse_lazy('lmsList')

class lmsDelete(LoginRequiredMixin, DeleteView):
    model = lms_details
    login_url = '/login/' 
    template_name = "lms/lms_delete.html"
    success_url = reverse_lazy('lmsList')

class lmsApprove(LoginRequiredMixin, ListView):
    model = lms_details
    login_url = '/login/' 
    form_class = lmsApproveForm
    template_name = "lms/lms_approve.html"
    context_object_name = 'lms'
    queryset = lms_details.objects.filter(ls_status = 'P')

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['EmpUser_list'] = EmpProfile.objects.all()
        context['User_detail'] = User.objects.all()
        return context

    def post(self, request, *args, **kwargs):        
            d = dict(request.POST.items())            
            try:
                ky = list(d.keys())[0]
                d.pop(ky)
                for key, value in d.items():  
                    print ("Id is : " + key)
                    print ("status is :" + value)
                    self.model.objects.filter(id=key).update(ls_status=value)
                
                return  HttpResponseRedirect("/lms/approve/")

            except ValueError:
                print ("Value Eror")
