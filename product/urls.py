from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from store.views import ProductViewSet, auth

router = SimpleRouter()
router.register(r'product', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', auth),
    url('', include('social_django.urls', namespace='social'))
]

urlpatterns += router.urls
