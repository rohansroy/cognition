import csv
from django.contrib import admin
from cognitive_skills.models import Test, Result, Worker
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
    search_fields = ('worker__id',)
    actions = ("export_as_csv",)
    list_display = ('worker', 'test', 'correct', 'incorrect', 'total', 'pctCorrect',)
    list_filter = ('test', )

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

class WorkerAdmin(admin.ModelAdmin):
    search_fields = ('id',)
    list_display = ('id', 'completed_all_tests', 'tests_completed', 'total_correct_answers', 'total_answers', 'pctCorrect')
    actions = ('export_as_csv',)
    readonly_fields = ('location', 'time_zone')

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['id', 'age', 'gender', 'city', 'state', 'ethnicity', 'education', 'marital_status', 'orientation', 'employment']
        result_names = [
            field.name for field in Result._meta.get_fields() if field.name in ['test', 'correct', 'total']
        ]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)

        writer = csv.writer(response)
        writer.writerow(field_names + result_names * Test.objects.count())
        for obj in queryset:
            if obj.completed_all_tests:
                results = list(
                    { value['test']:value for value in obj.results.all().order_by('test__name').values('test', 'test__name', 'correct', 'total')}.values()
                )
                result_values = []
                for result in results:
                    result_values += [result['test__name'], result['correct'], result['total']]
                row = writer.writerow([getattr(obj, field) for field in field_names] + result_values)
        
        return response
    export_as_csv.short_description = "Export CSV"

    def completed_all_tests(self, obj):
        return obj.completed_all_tests
    completed_all_tests.boolean = True

admin.site.register(Test, TestAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(Worker, WorkerAdmin)