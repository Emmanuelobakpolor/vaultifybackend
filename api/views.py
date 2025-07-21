from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Admin, Service, Provider, Alert
from .serializers import AdminSerializer, ServiceSerializer, ProviderSerializer, ServiceWithProvidersSerializer, AlertSerializer
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt

from rest_framework.permissions import AllowAny

# Removed is_auth view as per user request

from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_data(request):
    try:
        admin = request.user
        serializer = AdminSerializer(admin)
        return Response({'success': True, 'userData': serializer.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])
def register_admin(request):
    if request.method == 'POST':
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save()
            return Response(AdminSerializer(admin).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login_admin(request):
    data = request.data
    adminEmail = data.get('adminEmail')
    adminPassword = data.get('adminPassword')
    try:
        admin = Admin.objects.filter(adminEmail=adminEmail).first()
        if admin and adminPassword and check_password(adminPassword, admin.adminPassword):
            refresh = RefreshToken.for_user(admin)
            serializer = AdminSerializer(admin)
            return Response({
                'success': True,
                'userData': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response({'success': False, 'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'success': False, 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_all_admin(request):
    admins = Admin.objects.all()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_range_view_admins(request):
    admins = Admin.objects.filter(adminRole="Range-view admin")
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_paradise_admins(request):
    admins = Admin.objects.filter(adminRole="Paradise admin")
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data)

from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def get_paradise_and_range_view_admins(request):
    current_role = request.query_params.get('currentRole', None)
    if current_role == "Super-admin":
        admins = Admin.objects.filter(adminRole__in=["Paradise admin", "Range-view admin"])
    elif current_role == "Range-view admin":
        admins = Admin.objects.filter(adminRole="Range-view admin")
    elif current_role == "Paradise admin":
        admins = Admin.objects.filter(adminRole="Paradise admin")
    else:
        admins = Admin.objects.none()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data)

class ServiceListView(ListAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

from rest_framework.views import APIView

class ServiceWithProvidersView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceWithProvidersSerializer(services, many=True)
        return Response(serializer.data)

from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

class ProviderListCreateView(ListCreateAPIView):
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()  # Default queryset

    def get_queryset(self):
        service_name = self.request.query_params.get('service_name')
        admin_id = self.request.query_params.get('admin_id')
        queryset = Provider.objects.all()
        if service_name:
            queryset = queryset.filter(service__name=service_name)
        if admin_id:
            queryset = queryset.filter(admin__id=admin_id)
        return queryset

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        service_name = data.get('service_name')
        admin_id = data.get('admin_id')
        if not service_name:
            return Response({"error": "service_name is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not admin_id:
            return Response({"error": "admin_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            service = Service.objects.get(name=service_name)
        except Service.DoesNotExist:
            return Response({"error": "Service not found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            admin = Admin.objects.get(id=admin_id)
        except Admin.DoesNotExist:
            return Response({"error": "Admin not found"}, status=status.HTTP_400_BAD_REQUEST)
        data['service_id'] = service.id
        data['admin'] = admin.id
        if 'service' in data:
            del data['service']
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProviderRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response

class ServiceProvidersByEstateView(APIView):
    def get(self, request):
        services = Service.objects.all()
        response_data = []
        for service in services:
            providers = Provider.objects.filter(service=service)
            estate_dict = {}
            for provider in providers:
                try:
                    estate = provider.admin.adminRole
                except Exception:
                    estate = "Unknown"
                if estate not in estate_dict:
                    estate_dict[estate] = []
                estate_dict[estate].append({
                    "id": provider.id,
                    "provider_name": provider.provider_name,
                    "email": provider.email,
                    "phone": provider.phone,
                    "location": provider.location,
                    "availability": provider.availability,
                    "service": provider.service.name,
                })
            response_data.append({
                "service_id": service.id,
                "service_name": service.name,
                "estates": estate_dict
            })
        return Response(response_data)

@api_view(['DELETE'])
def delete_admin(request, id):
    try:
        admin = get_object_or_404(Admin, id=id)
        admin.delete()
        return Response({'message': 'Admin deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def get_update_admin_by_id(request, id):
    try:
        admin = get_object_or_404(Admin, id=id)
        if request.method == 'GET':
            serializer = AdminSerializer(admin)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = AdminSerializer(admin, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class AlertListCreateView(ListCreateAPIView):
    queryset = Alert.objects.all().order_by('-created_at')
    serializer_class = AlertSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estate = self.request.query_params.get('estate', None)
        role = self.request.query_params.get('role', None)
        if estate:
            queryset = queryset.filter(estate__iexact=estate)
        if role:
            queryset = queryset.filter(role__iexact=role)
        return queryset
