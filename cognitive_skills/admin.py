import csv
from django.contrib import admin
from cognitive_skills.models import Test, Result
from django.http import HttpResponse


class TestAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('slug',)
        return []

    def get_prepopulated_fields(self, request, obj=None):
        if obj:
            return {}
        return {"slug": ("name",)}

class ResultAdmin(admin.ModelAdmin):
    search_fields = ('worker_id',)
    actions = ("export_as_csv",)
    list_display = ('worker_id', 'test', 'correct', 'incorrect', 'total', 'pctCorrect',)

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        # field_names = [field.name for field in meta.fields]
        field_names = ['worker_id', 'test', 'correct', 'incorrect', 'total', 'pctCorrect']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response
    
    export_as_csv.short_description = "Export CSV"

admin.site.register(Test, TestAdmin)
admin.site.register(Result, ResultAdmin)