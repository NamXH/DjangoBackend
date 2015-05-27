from django.utils import dateparse

def filter_by_date_updated(request, queryset):
    # In future release we can return 304 (not modified) if we want to comply strictly with RFC-2616
    modified_since_header = request.META.get('HTTP_IF_MODIFIED_SINCE')
    if modified_since_header is not None:
        modified_since = dateparse.parse_datetime(modified_since_header)
        return queryset.filter(date_updated__gte=modified_since)
    else:
        return queryset

def check_timestamp(request, current_timestamp):
    temp = request.DATA.get('timestamp')
    try:
        request_timestamp = int(temp)
    except Exception:
        return None
    if request_timestamp is None:
        return None
    else:
        return request_timestamp == current_timestamp