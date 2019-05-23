from django.contrib.auth.decorators import login_required
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.db import IntegrityError
from django.forms import formset_factory
from django.views import generic
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from datetime import timedelta
import datetime
from .models import TimeRecords,TimeMenus
from .models import ProjectName
from .forms import CreateTimeSheetForm
import xlwt, xlrd, os
from xlrd import open_workbook
from xlutils.copy import copy
import traceback
from shutil import copyfile
# Create your views here. from sess_dev.timesheets.models import TimeRecords,TimeMenus

proj_name = "Project Name"
#proj_name=ProjectName.objects.values_list('project_name', flat=True).get(pk=1)
today = datetime.datetime.now()

def days_between_ends(start_date,end_date):
    delta = end_date - start_date         # timedelta
    for i in range(delta.days + 1):
        yield start_date + timedelta(i)

def timeSheetMenu(request):
    time_menus=TimeMenus.objects.all()
    context={'proj_name':proj_name,'time_menus':time_menus}
    return render(request,'tms/index.html', context)

def timeEntryApprove(request):
    emp_id = request.session.get('emp_id')
    context = dict()
    time_records = TimeRecords.objects.all()
    # emp_id = 2002
    # time_records = TimeRecords.objects.all().filter(emp_id = emp_id)
    current_week = timezone.now().isocalendar()[1]
    current_records = [time_record for time_record in time_records if time_record.get_week() == current_week]
    context['current_records'] = current_records
    context['c_week'] = current_week

    if request.method == 'POST':
        emp_id = request.POST['eid']
        time_records = TimeRecords.objects.all().filter(emp_id = emp_id)
        current_week = timezone.now().isocalendar()[1]
        current_records = [time_record for time_record in time_records if time_record.get_week() == current_week]
        context['current_records'] = current_records
        return render(request, 'tms/timesheets_approve.html', context)
   

    return render(request, 'tms/timesheets_approve.html', context)

@login_required(login_url='/login/')
def timeEntryList(request):
    emp_id = request.session.get('emp_id')
    context = dict()
    
   
    # time_records = TimeRecords.objects.all()
    time_records = TimeRecords.objects.all().filter(emp_id = emp_id)
    current_week = timezone.now().isocalendar()[1]
    current_records = [time_record for time_record in time_records if time_record.get_week() == current_week]
    c_week = current_week
    x_week = current_week
    y_week = current_week

    if request.method == 'POST':
        try:
            week = request.POST['week']

            if week == 'selected':
                week_sel = request.POST['week-selected']
                week_no = week_sel[6:8]
                print(week_no)
                
                week_no = int(week_no)
                current_records = [time_record for time_record in time_records if
                                    time_record.get_week() == week_no ]
                # try:
                #     gotdata = current_records[0]                
                #     c_week = current_records[0].get_week()
                #     x_week = current_records[0].get_week()
                # except IndexError:
                #     gotdata = 'null'
                #     c_week = week_no 

            # if week == 'next-week':
            #     week_no = request.POST.get('week_no')
            #     week_no = int(week_no)
            #     current_records = [time_record for time_record in time_records if
            #                         time_record.get_week() == week_no + 1]
            #     try:
            #         gotdata = current_records[0]
                    
            #         c_week = current_records[0].get_week()
            #         x_week = current_records[0].get_week()
            #     except IndexError:
            #         gotdata = 'null'
            #         c_week = week_no 
            #         x_week = ''
            
            # if week == 'last-week':
            #     week_no = request.POST.get('week_no')
            #     week_no = int(week_no)
            #     if not c_week:
            #         c_week = week_no
            #     current_records = [time_record for time_record in time_records if
            #                         time_record.get_week() == week_no - 1]
            #     try:
            #         gotdata = current_records[0]
            #         c_week = current_records[0].get_week()
            #         y_week = current_records[0].get_week()
            #     except IndexError:
            #         gotdata = 'null'
            #         c_week = week_no 
            #         y_week = ''
        except :
            request.method = 'GET'
            return timeEntryList(request)
            
    context['current_records'] = current_records
    context['c_week'] = c_week
    context['x_week'] = x_week
    context['y_week'] = y_week

    return render(request, 'tms/list.html', context)

def timeEntryCreate(request):
    emp_id = request.session.get('emp_id')
    
    if request.method == 'POST':
        hours=request.POST['hours']
        task_description=request.POST['task-description']
        try :
            request.POST['task-period']
            start_date=request.POST['start_date']
            end_date=request.POST['end_date']
            start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
            date_list=list(days_between_ends(start_date, end_date))
            for date_element in date_list:
                try:
                    tms_create = TimeRecords(emp_id=emp_id,ts_date=date_element,ts_effort=hours,ts_desc=task_description,ts_status='P')
                    tms_create.save()
                except IntegrityError:
                    dup_msg="The Time Sheet for "+ str(date_element) + " is already present"
                    messages.warning(request, dup_msg)
            messages.success(request, "Time logged successfully")
            return redirect(timeEntryList)
        except Exception:            
            date = request.POST['date']
            print ("you didnot check period")
            try:
                tms_create = TimeRecords(emp_id=emp_id,ts_date=date,ts_effort=hours,ts_desc=task_description,ts_status='P')
                tms_create.save() 
                messages.success(request, "Time logged successfully")
                return redirect(timeEntryList)
            except IntegrityError:
                dup_msg="The Time Sheet for "+ date + " is already present"
                messages.warning(request, dup_msg)
                return redirect(timeEntryList)
            
# # one if duplicate insertaion 
#             traceback.print_exc()
#         #except:
            
#             # date =request.POST['date']
#             # print ("you didnot check period")
#             # tms_create = TimeRecords(emp_id=emp_id,ts_date=date,ts_effort=hours,ts_desc=task_description,ts_status='P')
#             # tms_create.save()
#             # messages.success(request, "Submitted") 
#             # return timeEntryList(request)  
#             # messages.warning(request, "Something went wrong") 
#             return render(request, 'timesheets/list.html')
       
# this is working for the GET request
    else:
        print("failed")
        return timeEntryList(request)

    return render(request, 'tms/list.html')

@login_required(login_url='/login/')
def timeEntryUpdate(request, id):
    emp_id = request.session.get('emp_id')
    obj = get_object_or_404(TimeRecords, id=id)
    form = CreateTimeSheetForm(request.POST or None, instance=obj)
    context = {
        'form' : form
    }
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Time Entry Updated")
        return HttpResponseRedirect("/tms/")
    template = "tms/update.html"
    return render(request, template, context )

@login_required(login_url='/login/')
def timeEntryDelete(request, id):
    emp_id = request.session.get('emp_id')
    obj = get_object_or_404(TimeRecords, id=id) 
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Time Entry Deleted")
        return HttpResponseRedirect("/tms/")
    context = {
        "id" : obj,
    }
    template = "tms/delete.html"
    return render(request, template, context )
    
    ############################### export

def timeEntryExport(request):
    emp_id = request.session.get('emp_id')
    if request.method == 'GET':
        exp_week=request.GET['exp_week']
        start_date="2018 " + exp_week
        start_date=datetime.datetime.strptime(start_date + ' 0', "%Y %W %w")
        start_date=start_date + timedelta(1)
        end_date=start_date + timedelta(7)
        rows = TimeRecords.objects.all().filter(emp_id = emp_id,ts_date__range=(start_date, end_date)).values_list('ts_date', 'ts_effort', 'ts_desc')
  
        src = os.path.dirname(os.path.realpath(__file__)) + '/static/ts.xls'
        dst=  os.path.dirname(os.path.realpath(__file__)) + '/temp/ts.xls'
        copyfile(src, dst)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename= "' + dst + '"'

        # start_date=str(start_date.strftime('%d-%m-%y'))
        # end_date=str(end_date.strftime('%d-%m-%y'))
        # sheet_name=start_date+"_"+end_date

        rb = xlrd.open_workbook(dst)
        wb = copy(rb)
        ws = wb.get_sheet(0)
        
        # xf_index = wb.cell_xf_index(0, 0)
        # saved_style = wb[xf_index]

        font_style = xlwt.XFStyle()
        font_style.font.bold = True
        date_style = xlwt.easyxf(num_format_str='DD-MM-YYYY')
        font_style = xlwt.XFStyle()

        row_num=20
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                if isinstance(row[col_num], datetime.date):
                    ws.write(row_num, 1, row[col_num], date_style)
                else:
                    ws.write(row_num, 1, row[col_num], font_style)

        wb.save(response)        
        return response