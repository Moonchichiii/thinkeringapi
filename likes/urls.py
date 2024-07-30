from rest_framework.routers import DefaultRouter
from .views import LikeViewSet

app_name = 'likes'

router = DefaultRouter()
router.register(r'', LikeViewSet, basename='like')

urlpatterns = router.urls
