from django.contrib import admin
from apps.confidencechronograms.models import Chronogram, Task, Cliente, Funcionario, Comentario

class FuncAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cargo', 'endereco', 'fone1', 'bloqueado')
    list_filter = ('nome',)
    search_fields = ['nome', 'bloqueado']

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nome', 'razao_social', 'endereco', 'fone1', 'bloqueado')
    list_filter = ('nome',)
    search_fields = ['nome', 'bloqueado']


class ChronogramAdmin(admin.ModelAdmin):
    list_display = ('construction', 'client', 'total_time', 'address', 'total_price', 'date_added')
    list_filter = ('construction', 'client',)
    search_fields = ['client', 'construction']


class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_text', 'price', 'start_date', 'end_date', 'date_added')
    list_filter = ('start_date',)
    search_fields = ['task_text', 'start_date']

class Comentario_Admin(admin.ModelAdmin):    
    list_display = ('nome_cliente','assunto', 'dt_entrada')
    search_fields = ['nome_cliente']


admin.site.register(Chronogram, ChronogramAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Funcionario, FuncAdmin)
admin.site.register(Cliente, ClientAdmin)
admin.site.register(Comentario, Comentario_Admin)