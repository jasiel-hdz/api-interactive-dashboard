from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from datetime import datetime, timedelta
from .models import Viewer
from django.db.models import Sum, Avg
from .serializers import ViewersSerializer
from builtins import round
from collections import defaultdict, Counter

class ViewersDayView(APIView):
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

        # Filter the Viewer records based on the date range
        viewer_records = Viewer.objects.filter(
            period_start_date__gte=start_date,  # Filter from the start date
            period_start_date__lte=end_date     # Filter until the end date
        )
        
        # Perform aggregations for the required fields
        avg_age = viewer_records.aggregate(Avg('age_value'))['age_value__avg'] or 0
        avg_dwell_time = viewer_records.aggregate(Avg('dwell_time_in_tenths_of_sec'))['dwell_time_in_tenths_of_sec__avg'] or 0
        avg_attention_time = viewer_records.aggregate(Avg('attention_time_in_tenths_of_sec'))['attention_time_in_tenths_of_sec__avg'] or 0
        
        # Count emotions
        emotion_counts = Counter({
            'very_happy': 0,
            'happy': 0,
            'neutral': 0,
            'unhappy': 0,
            'very_unhappy': 0
        })

        # Iterate over the Viewer records to count the emotions
        for viewer in viewer_records:
            emotions = {
                'very_happy': viewer.very_happy,
                'happy': viewer.happy,
                'neutral': viewer.neutral,
                'unhappy': viewer.unhappy,
                'very_unhappy': viewer.very_unhappy
            }
            # Identificar la emoción más alta
            predominant_emotion = max(emotions, key=emotions.get)
            emotion_counts[predominant_emotion] += 1
        
        # Total count
        total_male = viewer_records.filter(gender=1).count()
        total_female = viewer_records.filter(gender=2).count()

        # Round the average values to 1 decimal place
        avg_age = round(avg_age, 1)
        avg_dwell_time = round(avg_dwell_time / 10, 1)  # Convert to seconds
        avg_attention_time = round(avg_attention_time / 10, 1)  # Convert to seconds

        # Total number of Viewer records within the date range
        total_viewers = viewer_records.count()

        # Agrupar los viewers por hora redondeada
        viewers_by_hour = defaultdict(int)

        for viewer in viewer_records:
            period_start_time = viewer.period_start_time
            if period_start_time:
                # Redondear la hora a 0 minutos y 0 segundos
                rounded_hour = period_start_time.replace(minute=0, second=0).strftime('%H:%M:%S')
                viewers_by_hour[rounded_hour] += 1

        # Crear una lista con los resultados por hora
        viewers_by_hour_list = [{
            'hour': hour,
            'total_viewers': total
        } for hour, total in viewers_by_hour.items()]

        # Prepare the data for the response
        data = {
            'avg_age': avg_age,
            'avg_dwell_time_in_seconds': avg_dwell_time,
            'avg_attention_time_in_seconds': avg_attention_time,
            'total_viewers': total_viewers,
            'total_male': total_male,
            'total_female': total_female,
            'very_happy': emotion_counts['very_happy'],
            'happy': emotion_counts['happy'],
            'neutral': emotion_counts['neutral'],
            'unhappy': emotion_counts['unhappy'],
            'very_unhappy': emotion_counts['very_unhappy'],
            'viewers': viewers_by_hour_list  # Solo los datos agrupados por hora
        }
        
        # Return the response with the calculated averages
        return Response(data, status=status.HTTP_200_OK)
    
class ViewersWeekView(APIView):
    def post(self, request):
            pass