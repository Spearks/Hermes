from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExportChannelsView, SystemActionsView

router = DefaultRouter()
router.register(r'exportChannel', ExportChannelsView, basename='Export')
router.register(r'adminActions', SystemActionsView, basename='Actions')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
