from rest_framework import viewsets
from .models import Tag
from .serializers import TagSerializer


# Create your views here.

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer

    def get_queryset(self):
        tag_type = self.request.query_params.get('tag_type')
        if tag_type:
            return self.queryset.filter(tag_type=tag_type)
        return self.queryset

