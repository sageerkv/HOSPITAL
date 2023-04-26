from django.contrib import admin
from . models import Departments,Doctors,Booking,CustumUser

# Register your models here.

admin.site.register(Departments)
admin.site.register(Doctors)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','p_name')
    list_per_page = 10
    
admin.site.register(Booking,BookingAdmin)
admin.site.register(CustumUser)