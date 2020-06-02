from rest_framework import filters
from datetime import timedelta, datetime


class StatusFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(**{"status": 1})


class PeriodFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'period' in request.query_params:
            period = request.GET.get('min_lat')
            if period == 'daily':
                return queryset.filter(**{"pub_date": datetime.today()})
            elif period == 'weekly':
                return queryset.filter(**{"pub_date__gt": datetime.today() - timedelta(days=7)})
            else:
                return queryset.filter(**{"pub_date__gt": datetime.today() - timedelta(days=30)})


class CoordinateLatFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'min_lat' in request.query_params and 'max_lat' in request.query_params:
            # Values
            _min_lat = float(request.GET.get('min_lat'))
            _max_lat = float(request.GET.get('max_lat'))
            # Contains
            lat_lte = 'lat__lte'
            lat_gte = 'lat__gte'
            # Query
            if _min_lat and _max_lat:
                return queryset.filter(**{lat_gte: _min_lat, lat_lte: _max_lat})
            elif _min_lat and _max_lat is None:
                return queryset.filter(**{lat_gte: _min_lat})
            elif _max_lat and _min_lat is None:
                return queryset.filter(**{lat_lte: _max_lat})
        return queryset


class CoordinateLngFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'min_lng' in request.query_params and 'max_lng' in request.query_params:
            # Values
            _min_lng = float(request.GET.get('min_lng'))
            _max_lng = float(request.GET.get('max_lng'))
            # Contains
            lng_lte = 'lng__lte'
            lng_gte = 'lng__gte'
            # Query
            if _min_lng and _max_lng:
                return queryset.filter(**{lng_gte: _min_lng, lng_lte: _max_lng})
            elif _min_lng and _max_lng is None:
                return queryset.filter(**{lng_gte: _min_lng})
            elif _max_lng and _min_lng is None:
                return queryset.filter(**{lng_lte: _max_lng})
        return queryset
