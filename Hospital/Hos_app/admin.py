from django.contrib import admin
from . models import Departments,Doctors,Booking

# Register your models here.

admin.site.register(Departments)
admin.site.register(Doctors)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','p_name','p_phone','p_email','doc_name','Booking_date','Booked_on')
    
admin.site.register(Booking,BookingAdmin)