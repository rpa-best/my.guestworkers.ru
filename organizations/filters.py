from unfold.contrib.filters.admin import MultipleDropdownFilter
from .models import Organization


class OrganizationFilter(MultipleDropdownFilter):
    title = 'Компания'
    parameter_name = "org__in"
    queryset_lookup = 'workertoorganization__org__in'

    def lookups(self, request, model_admin):
        return [(org.pk, str(org)) for org in Organization.objects.all()]

    def queryset(self, request, queryset):
        if self.value() not in [[''], None, []]:
            # Here write custom query
            return queryset.filter(**{self.queryset_lookup: self.value()})
        return queryset


class WorkerOrganizationFilter(OrganizationFilter):
    queryset_lookup = 'worker__workertoorganization__org__in'
