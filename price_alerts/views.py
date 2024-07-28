from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from .serializers import AlertSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

# price_alerts/views.py

from django.http import HttpResponse



def home(request):
    return HttpResponse("Welcome to the Price Alert System!")

# price_alerts/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from .models import Alert
from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from .models import Alert
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .tasks import listen_price_updates

listen_price_updates.delay()

from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from .serializers import AlertSerializer
from .tasks import check_price_task

class AlertCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = AlertSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            check_price_task.delay(serializer.data['crypto'], serializer.data['target_price'], request.user.email)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class AlertListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')
        if status:
            alerts = Alert.objects.filter(user=request.user, status=status)
        else:
            alerts = Alert.objects.filter(user=request.user)
        serializer = AlertSerializer(alerts, many=True)
        return Response(serializer.data)


class AlertListView(View):
    def get(self, request):
        status = request.GET.get('status')
        if status:
            alerts = Alert.objects.filter(user=request.user, status=status)
        else:
            alerts = Alert.objects.filter(user=request.user)
        data = list(alerts.values())
        return JsonResponse(data, safe=False)
    
@method_decorator(csrf_exempt, name='dispatch')
class AlertDeleteView(View):
    def delete(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            alert_id = data.get('id')
            alert = Alert.objects.get(id=alert_id, user=request.user)
            alert.delete()
            return JsonResponse({'message': 'Alert deleted successfully'}, status=200)
        except Alert.DoesNotExist:
            return JsonResponse({'error': 'Alert not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


class TokenObtainPairView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class AlertCreateView(generics.CreateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

class AlertDeleteView(generics.DestroyAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

class AlertListView(generics.ListAPIView):
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        status = self.request.query_params.get('status', None)
        if status:
            return Alert.objects.filter(user=user, status=status)
        return Alert.objects.filter(user=user)
