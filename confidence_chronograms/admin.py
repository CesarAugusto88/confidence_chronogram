from django.contrib import admin
from confidence_chronograms.models import Chronogram, Task, Funcionario, Cliente

class FuncAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'endereco', 'fone1', 'bloqueado')
    list_filter = ('nome',)
    search_fields = ['nome', 'bloqueado']

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nome', 'razao_social', 'endereco', 'fone1', 'bloqueado')
    list_filter = ('nome',)
    search_fields = ['nome', 'bloqueado']


class ChronogramAdmin(admin.ModelAdmin):
    list_display = ('construction', 'client', 'total_time', 'address', 'total_price', 'usuario', 'date_added')
    list_filter = ('construction', 'client',)
    search_fields = ['client', 'construction']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_text', 'price', 'start_date', 'end_date', 'date_added')
    list_filter = ('start_date',)
    search_fields = ['task_text', 'start_date']


admin.site.register(Chronogram, ChronogramAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Funcionario, FuncAdmin)
admin.site.register(Cliente, ClientAdmin)