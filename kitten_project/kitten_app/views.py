from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Kitten, Breed, Rating
from .serializers import KittenSerializer, BreedSerializer, RatingSerializer
from rest_framework.permissions import IsAuthenticated
from django.views.generic import FormView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied, NotFound

# Вьюсет для пород котов
class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

# Вьюсет для котят
class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated]

    # Сохранение котенка с владельцем
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # Получение котят только для аутентифицированного пользователя
    def get_queryset(self):
        return Kitten.objects.filter(owner=self.request.user) if self.request.user.is_authenticated else Kitten.objects.none()

    # Обновление котенка только для его владельца
    def perform_update(self, serializer):
        if serializer.instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете изменять этого котенка.")
        serializer.save()

    # Удаление котенка только для его владельца
    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied("Вы не можете удалить этого котенка.")
        instance.delete()

    # Переопределение метода, чтобы обрабатывать ошибки при получении котят
    def retrieve(self, request, *args, **kwargs):
        try:
            kitten = self.get_object()
            serializer = self.get_serializer(kitten)
            return Response(serializer.data)
        except NotFound:
            return Response({'error': 'Котенок не найден.'}, status=status.HTTP_404_NOT_FOUND)

# Вьюсет для оценок котят
class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    # Сохранение оценки с пользователем
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Получение оценок только для котят владельца
    def get_queryset(self):
        return Rating.objects.filter(kitten__owner=self.request.user) if self.request.user.is_authenticated else Rating.objects.none()

# Вьюха для логина
class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)

        # Генерация JWT токенов
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return JsonResponse({
            'success': True,
            'message': 'Успешный вход в систему',
            'access_token': access_token,
            'refresh_token': refresh_token
        })

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

# Вьюха для регистрации
class RegisterView(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    # Обработка успешной регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class CustomLogoutView(LogoutView):
    http_method_names = ["get", "post", "options"]  # Добавил GET по умолчанию

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
