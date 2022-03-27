from django.urls import path
from django.urls import include
from rest_framework_simplejwt import views as jwt_views
from api.views import GetUserGeolocationData, GeolocationDataViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'api/geolocations', GeolocationDataViewSet, basename='geolocations')

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/get_user_geolocation_data', GetUserGeolocationData.as_view(), name='get_user_geolocation_data'),
    path('', include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)