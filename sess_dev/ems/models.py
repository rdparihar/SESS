from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse 
from django.dispatch import receiver
from django.contrib.auth.models import User

class EmpProfile(models.Model):
    #username = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.ForeignKey(User, on_delete=models.CASCADE, )

    emp_id = models.AutoField(primary_key=True, verbose_name = 'Employee ID')
    emp_dob = models.DateField(null=False, blank=False, verbose_name = 'Date of Birth')
    emp_doj = models.DateField(null=False, blank=False, verbose_name = 'Date of Joining')
    emp_dot = models.DateField(null=True, blank=True, verbose_name = 'Date of Termination')
    emp_con_primary = models.CharField(max_length=10, verbose_name = 'Primary contact number')
    emp_con_secondary = models.CharField(max_length=10, verbose_name = 'Secondary contact number')
    emp_designation = models.CharField(max_length=200, verbose_name = 'Employee designation')
    emp_department = models.CharField(max_length=50, verbose_name = 'Employee Department')

    class Meta:
        verbose_name = 'Emp Profile'
        verbose_name_plural = 'Emp Profile'
        ordering = ["-emp_id"]

    def __str__(self):
         return str(self.username)


















# def create_profile(sender,**kwargs ):
#     if kwargs['created']:
#         user_profile=UserProfile.objects.create(user=kwargs['instance'])


# post_save.connect(create_profile,sender=User)

# #@receiver(post_save, sender=User)
# #def create_emp_profile(sender, instance, created, **kwargs):
# def create_emp_profile(sender, **kwargs):

#     print("if ke oopar")
#     print(sender)
#     print(kwargs['instance'])
#     print(kwargs['created'])

#     if kwargs['created']:
#         print("if ke andar")

#         EmpProfile.objects.create(username=instance)
#    # instance.empprofile.save()

# post_save.connect(create_emp_profile, sender=User)
    
