from django.contrib import admin
from cognitive_skills.models import Test, Result


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
    pass

admin.site.register(Test, TestAdmin)
admin.site.register(Result, ResultAdmin)