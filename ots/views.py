from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OTS
# from .serializers import OTSSerializerk


class OTSListView(APIView):
    #View to list all OTS records.
    def get(self, request):
        
        ots_records = OTS.objects.all()
        serializer = OTSSerializer(ots_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)