from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views import generic
from django.views.generic import TemplateView
from ems.views import ProfileCreateView
from ems.models import EmpProfile
from lms.models import lms_details

class IndexView(View):
    template_name = "home.html"
    def get(self, request):
        return render(request, self.template_name)

def error(request):
    template = "error.html"    
    return render(request, template )

@receiver(user_logged_in)
def sig_user_logged_in(sender, user, request, **kwargs):
    request.session['isLoggedIn'] = True
    request.session['isAdmin'] = user.is_superuser
    request.session['email'] = user.email
    request.session['username'] = user.username
    request.session['username_id'] = user.id
    username  = request.session.get('username')
    userid = User.objects.values("id").get(username=username)
    try:
        emp_id = EmpProfile.objects.values("emp_id").get(username_id=userid['id'])
        emp_id=emp_id['emp_id']
        request.session['emp_id'] = emp_id        
    except:
        pass
  
    isLoggedIn = request.session.get('isLoggedIn',False)
    isAdmin = request.session.get('isAdmin',False)
    email = request.session.get('email','')
    emp_id = request.session.get('emp_id')
    request.session.save()

    return render(
        request,
        'registration/login.html',
        context = {'isLoggedIn':isLoggedIn,'isAdmin':isAdmin,'email':email, 'emp_id':emp_id},
    )

@login_required(login_url='/login/')
def Dashboard(request):
    template = "index.html"
    username  = request.session.get('username')
    userid = User.objects.values("id").get(username=username)
    emp = get_object_or_404(User, username=username)
    context = { "emp" : emp }
    try:
        emp_id = EmpProfile.objects.values("emp_id").get(username_id=userid['id'])
        emp_id=emp_id['emp_id']
        request.session['emp_id'] = emp_id
    except:
        messages.warning(request, "Please create your profile to continue")
        return redirect(ProfileCreateView)
        #return redirect('/employee/new/')
    try:
        lms = lms_details.objects.all().filter(emp_id = emp_id)[:5]
        context.update({"lms" : lms})
    except:
          pass
    try:
        lms_approved = lms_details.objects.all().filter(emp_id = emp_id, ls_status = 'A')
        context.update({"lms_approved" : lms_approved })
    except:
          pass
    return render(request, template, context )























































    # try:
    # #     username  = request.session.get('username')
    # #     print(username)
    # #     userid = User.objects.values("id").get(username=username)
    # #     print(userid)
    # #     emp = get_object_or_404(User, username=username)
    # #   #  emp = User.objects.all().filter(username=username)
    # #     print("emp print ", emp)
    # #     print("emp ka type ha", type(emp))
    # #     print ("req", request.user.id)
    #     emp_id = EmpProfile.objects.values("emp_id").get(username_id=userid['id'])
    #     print("in try")
    #     print ("emp_id", emp_id)
    #     request.session['emp_id'] = emp_id
    #     messages.warning(request, "already exist from try")
    #     lms = get_object_or_404(lms_details, emp_id = emp_id)
      #  print ("lsm ka object aaya h", lms)
        # Context({"person": PersonClass2})


        #emp = get_object_or_404(User, username=username)
        #lms=lms_details.objects.all().filter(emp_id = emp_id)
        #print ("lms is", lms)
        #lms_approved=lms_details.objects.all().filter(emp_id = emp_id, ls_status = 'A')
        #print ("lms_approved is", lms_approved)
        #lms = get_object_or_404(lms_details, emp_id = emp_id)  this not working 
        # context = { "emp" : emp, "lms" : lms , "lms_approved" : lms_approved,}
        # context = { "emp" : emp, }
        # template = "index.html"
        # return render(request, template, context )









    #     print(request.user.id)
    #     request.session['emp_id'] = EmpProfile.objects.filter(username_id__exact = request.user.id).values('emp_id')[0]['emp_id']
    # except:
    #     messages.warning(request, "Please create user profile")
    #     print("in catch")
    #     return redirect('/employee/new/')
    #     print("redirect does not worked catch")

    # emp_id = request.session.get('emp_id')
    # username = request.session.get('username')
    # emp = get_object_or_404(User, username=username)
    # lms=lms_details.objects.all().filter(emp_id = emp_id)
    # print ("lms is", lms)
    # lms_approved=lms_details.objects.all().filter(emp_id = emp_id, ls_status = 'A')
    # print ("lms_approved is", lms_approved)
    # #lms = get_object_or_404(lms_details, emp_id = emp_id)  this not working 
    # context = { "emp" : emp, "lms" : lms , "lms_approved" : lms_approved,}
    # context = { "emp" : emp, }
    
# def get_context_data(self, **kwargs):
#         context = super(EmployeeDetailView, self).get_context_data(**kwargs)
#         context['tags'] = TimeRecords.objects.all().filter(emp_id = 2001)
#         return context
