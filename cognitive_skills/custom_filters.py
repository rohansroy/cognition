from django.contrib.admin import SimpleListFilter
from .models import Worker

class CompletedTestsFilter(SimpleListFilter):
    """
    This filter is being used in django admin panel in worker model.
    """
    title = 'Completed All Tests'
    parameter_name = 'worker__completed_all_tests'

    def lookups(self, request, model_admin):
        return (
            ('True', 'Complete'),
            ('False', 'Incomplete')
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value().lower() == 'business':
            return queryset.filter(user__email__regex=self.SOCIAL_EMAIL_REGEX)
        elif self.value().lower() == 'non_business':
            return queryset.filter().exclude(user__email__regex=self.SOCIAL_EMAIL_REGEX)