from resource import RLIM_INFINITY
from django.contrib import admin
from .models import Book, Copy, Liberian, Reservee, Loan, Review, Defaulters


# Register your models here.
class AlterReservee(admin.ModelAdmin):
    readonly_fields = ('datecreated',)
class AlterLoan(admin.ModelAdmin):
    readonly_fields = ('dateloaned',)
admin.site.register(Book)
admin.site.register(Copy)
admin.site.register(Reservee)
admin.site.register(Loan)
admin.site.register(Review)
admin.site.register(Liberian)
admin.site.register(Defaulters)