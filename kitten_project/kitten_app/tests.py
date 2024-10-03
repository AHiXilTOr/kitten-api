import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import Kitten, Breed, Rating
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.mark.django_db
def test_create_kitten():
    client = APIClient()
    
    # Создаем пользователя
    user = User.objects.create_user(username='testuser', password='12345')
    breed = Breed.objects.create(name='Siamese')

    # Получаем JWT токен для пользователя
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Добавляем токен в заголовок Authorization
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Выполняем POST-запрос для создания котенка
    response = client.post('/api/kittens/', {
        'color': 'white',
        'age': 6,
        'description': 'Playful kitten',
        'breed': breed.id
    })

    assert response.status_code == 201
    assert Kitten.objects.count() == 1
    print("Test 'test_create_kitten' passed.")

@pytest.mark.django_db
def test_create_rating():
    client = APIClient()
    
    # Создаем пользователя и котенка
    user = User.objects.create_user(username='testuser', password='12345')
    breed = Breed.objects.create(name='Siamese')
    kitten = Kitten.objects.create(color='white', age=6, description='Kitten', breed=breed, owner=user)

    # Получаем JWT токен для пользователя
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    # Добавляем токен в заголовок Authorization
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    # Выполняем POST-запрос для создания оценки
    response = client.post('/api/ratings/', {
        'kitten': kitten.id,
        'score': 5
    })

    assert response.status_code == 201
    assert Rating.objects.count() == 1
    assert Rating.objects.first().score == 5
    print("Test 'test_create_rating' passed.")
