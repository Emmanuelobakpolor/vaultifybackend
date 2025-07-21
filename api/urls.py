from django.urls import path
from .views import get_user_data, register_admin, get_all_admin, login_admin, ServiceListView, ProviderListCreateView, ServiceWithProvidersView, ProviderRetrieveUpdateDestroyView, get_range_view_admins, get_paradise_admins, delete_admin, get_paradise_and_range_view_admins, get_update_admin_by_id, ServiceProvidersByEstateView, AlertListCreateView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/registerAdmin', register_admin, name='register_admin'),
    path('admin/login', login_admin, name='login_admin'),
    path('admin/getAllAdmin', get_all_admin, name='get_all_admin'),
    path('admin/getRangeViewData', get_range_view_admins, name='get_range_view_admins'),
    path('admin/getParadiseData', get_paradise_admins, name='get_paradise_admins'),
    path('admin/getParadiseAndRangeViewAdmins', get_paradise_and_range_view_admins, name='get_paradise_and_range_view_admins'),
    path('admin/deleteAdmin/<int:id>', delete_admin, name='delete_admin'),
    path('admin/getAdminById/<int:id>', get_update_admin_by_id, name='get_update_admin_by_id'),
    path('admin/getUserData', get_user_data, name='get_user_data'),  # ✅ Add this line
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Removed is_auth endpoint as per user request
    path('services/', ServiceListView.as_view(), name='service-list'),
    path('services-with-providers/', ServiceWithProvidersView.as_view(), name='services-with-providers'),
    path('providers/', ProviderListCreateView.as_view(), name='provider-list-create'),
    path('providers/<int:pk>/', ProviderRetrieveUpdateDestroyView.as_view(), name='provider-detail'),
    path('services-by-estate/', ServiceProvidersByEstateView.as_view(), name='services-by-estate'),
    path('alerts/', AlertListCreateView.as_view(), name='alert-list-create'),
]


