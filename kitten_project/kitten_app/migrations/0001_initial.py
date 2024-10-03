import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def create_initial_data(apps, schema_editor):
    Breed = apps.get_model('kitten_app', 'Breed')

    breeds = ['Сиамская', 'Британская', 'Персидская']
    for breed_name in breeds:
        Breed.objects.create(name=breed_name)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Breed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Kitten',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('breed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kittens', to='kitten_app.breed')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kittens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(create_initial_data), 
    ]
