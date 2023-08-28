from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExportChannelsView

router = DefaultRouter()
router.register(r'exportChannel', ExportChannelsView, basename='Export')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
