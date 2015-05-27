from datetime import datetime
from django.utils.timezone import utc

from rest_framework.response import Response
from rest_framework.views import APIView

class TimeList(APIView):
    def get(self, request, format=None):
        return Response(datetime.utcnow().replace(tzinfo=utc))