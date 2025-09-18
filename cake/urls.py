from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CakeViewSet, OrderViewSet, RegisterView, LoginView, IngredientViewSet, LogoutView, UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="SweetCraft API",
        default_version='v1',
        description="Tortlar va buyurtmalar API hujjati",
        contact=openapi.Contact(email="admin@sweetcraft.uz"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('cakes', CakeViewSet)
router.register('orders', OrderViewSet)
router.register('ingredients', IngredientViewSet)
router.register('all_users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
