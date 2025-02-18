from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, GroupViewSet, CommentViewSet
from rest_framework.authtoken.views import obtain_auth_token

# Создаем router и регистрируем ViewSet'ы
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    # Все пути из router (posts, groups)
    path('', include(router.urls)),

    # Токен-авторизация
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Вложенные маршруты для комментариев
    path('posts/<int:post_id>/comments/',
         CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='comment-list'),
    path('posts/<int:post_id>/comments/<int:pk>/',
         CommentViewSet.as_view(
             {'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
              'delete': 'destroy'}), name='comment-detail'),
]
