from django.contrib import admin
from confidence_chronograms.models import Chronogram, Task

class ChronogramAdmin(admin.ModelAdmin):
    list_display = ('construction', 'client', 'total_time', 'address', 'total_price', 'usuario', 'date_added')
    list_filter = ('client', 'total_time')

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_text', 'price', 'start_date', 'end_date', 'duration', 'date_added')
    list_filter = ('start_date',)


admin.site.register(Chronogram, ChronogramAdmin)
admin.site.register(Task, TaskAdmin)
