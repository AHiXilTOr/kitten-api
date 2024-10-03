from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Breed(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Kitten(models.Model):
    color = models.CharField(max_length=100)
    age = models.PositiveIntegerField()  # Возраст в месяцах
    description = models.TextField()
    breed = models.ForeignKey(Breed, related_name='kittens', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='kittens', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.breed.name} - {self.color}'
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kitten = models.ForeignKey('Kitten', related_name='ratings', on_delete=models.CASCADE)
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    class Meta:
        unique_together = ('user', 'kitten')

    def __str__(self):
        return f'{self.user.username} - {self.kitten.color} - {self.score}'
