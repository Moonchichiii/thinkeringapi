from rest_framework.routers import DefaultRouter
from .views import RatingViewSet

app_name = 'ratings'

router = DefaultRouter()
router.register(r'', RatingViewSet, basename='rating')

urlpatterns = router.urls
