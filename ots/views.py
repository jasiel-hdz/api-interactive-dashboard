from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
from ots.models import OTS
from django.db.models import Sum, Avg
from .serializers import OTSSummaryDaySerializer, OTSDetailSerializer, OTSSummaryWeekSerializer
from builtins import round
from collections import defaultdict

class OTSDayView(APIView):
    def post(self, request):
        # Get the dates from the request body (FormData)
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')

        # Validate that both dates are provided
        if not start_date or not end_date:
            return Response({
                'detail': 'Both start_date and end_date are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validate that the dates are in the correct format (YYYY-MM-DD)
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                'detail': 'Invalid date format. Use YYYY-MM-DD.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Filter the OTS records based on the date range
        ots_records = OTS.objects.filter(
            period_start_date__gte=start_date,  # Filter from the start date
            period_start_date__lte=end_date     # Filter until the end date
        )

        # Perform aggregations to get the sum of ots_count and the average of watcher_count
        ots_count_sum = ots_records.aggregate(Sum('ots_count'))['ots_count__sum'] or 0
        ots_count_avg = ots_records.aggregate(Avg('ots_count'))['ots_count__avg'] or 0
        watcher_count_avg = ots_records.aggregate(Avg('watcher_count'))['watcher_count__avg'] or 0
        watcher_count_total = ots_records.aggregate(Sum('watcher_count'))['watcher_count__sum'] or 0

        # Calculate the number of OTS records
        ots_count = ots_records.count()

        # Serialize the OTS records
        ots_data = OTSDetailSerializer(ots_records, many=True).data
        
        # Round the average values to 1 decimal place
        ots_count_avg = round(ots_count_avg, 1)
        watcher_count_avg = round(watcher_count_avg, 1)
        
        # Prepare the data for the summary
        data = {
            'ots_count_sum': ots_count_sum,
            'ots_count_avg': ots_count_avg,
            'watcher_count_avg': watcher_count_avg,
            'watcher_count_total': watcher_count_total,
            'ots_count': int(ots_count),
            'ots': ots_data  # Here we pass the serialized data
        }

        # Pass the data to the summary serializer correctly
        serializer = OTSSummaryDaySerializer(data=data)

        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'detail': 'Error serializing data'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
class OTSWeekView(APIView):
    def post(self, request):
        # Get the date from the request
        day_date = request.data.get('day_date')

        if not day_date:
            # Return an error if the date is missing
            return Response({"error": "Date is missing"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert the date from string to datetime format
            day_date = datetime.fromisoformat(day_date)

            # Calculate the start of the current week (Monday)
            start_of_week = day_date - timedelta(days=day_date.weekday())
            start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)

            # Calculate the end of the week (Sunday, 6 days after Monday)
            end_of_week = start_of_week + timedelta(days=6)
            end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

            # Filter OTS records based on the date range (Monday to Sunday)
            ots_records = OTS.objects.filter(
                period_start_date__gte=start_of_week,
                period_start_date__lte=end_of_week
            )

            # Create a list to store the ots_count and watcher_count for each day of the week
            daily_counts = [ {'ots_count': 0, 'watcher_count': 0} for _ in range(7) ]  # Initialize list for 7 days

            # Calculate the ots_count and watcher_count for each day of the week
            for record in ots_records:
                day_of_week = record.period_start_date.weekday()  # Monday=0, Sunday=6
                daily_counts[day_of_week]['ots_count'] += record.ots_count
                daily_counts[day_of_week]['watcher_count'] += record.watcher_count

            # Perform aggregations for total and average counts
            aggregates = ots_records.aggregate(
                ots_count_sum=Sum('ots_count'),
                ots_count_avg=Avg('ots_count'),
                watcher_count_avg=Avg('watcher_count'),
                watcher_count_total=Sum('watcher_count')
            )

            # Extract values, setting defaults to 0 if any are None
            ots_count_sum = aggregates.get('ots_count_sum') or 0
            ots_count_avg = round(aggregates.get('ots_count_avg') or 0, 1)
            watcher_count_avg = round(aggregates.get('watcher_count_avg') or 0, 1)
            watcher_count_total = aggregates.get('watcher_count_total') or 0

            # Count the number of records
            ots_count = ots_records.count()

            # Prepare the data for the response
            data = {
                'ots_count_sum': ots_count_sum,
                'ots_count_avg': ots_count_avg,
                'watcher_count_avg': watcher_count_avg,
                'watcher_count_total': watcher_count_total,
                'ots_count': int(ots_count),
                'watcher_count': watcher_count_total,
                'days': daily_counts
            }

            # Pass the data to the serializer
            serializer = OTSSummaryWeekSerializer(data=data)

            # Check if the serializer is valid
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": serializer.errors}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValueError:
            # Handle invalid date format error
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)