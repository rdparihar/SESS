from django.db import models

# Create your models here.
class lms_count(models.Model):
    emp_id = models.PositiveIntegerField(verbose_name = 'Employee ID', help_text="Enter The Employee ID")
    ls_total = models.PositiveIntegerField(verbose_name = 'Total Leaves', help_text="Total Leaves")
    ls_availed = models.PositiveIntegerField(verbose_name = 'Availed Leaves', help_text="Availed Leaves")
    ls_balance = models.PositiveIntegerField(verbose_name = 'Balance Leaves', help_text="Balance Leaves")

    class Meta:
        verbose_name = 'Leave Count'
        verbose_name_plural = 'Leave Count'
        ordering = ["emp_id"]

    def __str__(self):
        return str(self.emp_id)

class lms_details(models.Model):
    LEAVE_STATUS = ( ('A', 'APPROVED'), ('P', 'PENDING'), ('R', 'REJECTED') )
    emp_id = models.PositiveIntegerField(verbose_name = 'Employee ID', help_text="Enter The Employee ID")
    ls_date = models.DateField(null=False, blank=False, verbose_name = 'Leave Date')
    ls_reason = models.CharField(max_length=200,verbose_name = 'Reason for taking Leave', help_text="Reason for taking Leave")
    ls_status = models.CharField(max_length=1, choices=LEAVE_STATUS, default='P', verbose_name = 'Leave Status')

    class Meta:
        verbose_name = 'Leave Details'
        verbose_name_plural = 'Leave Details'
        ordering = ["ls_date"]

    def __unicode__(self):
        return self.ls_date
    
