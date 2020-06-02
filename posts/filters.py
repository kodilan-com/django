from rest_framework import filters
from datetime import timedelta, datetime


class StatusFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(**{"status": 1})


class PeriodFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'period' in request.query_params:
            period = request.GET.get('period')

            if period == 'daily':
                return queryset.filter(**{"pub_date": datetime.today()})
            elif period == 'weekly':
                return queryset.filter(**{"pub_date__gt": datetime.today() - timedelta(days=7)})
            else:
                return queryset.filter(**{"pub_date__gt": datetime.today() - timedelta(days=30)})
        else:
            return queryset
