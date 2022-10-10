from django.db import models
from django.contrib.auth.models import AbstractUser


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING,
                                related_name='cities')
    name = models.CharField(max_length=50, unique=True)
    is_capital = models.CharField(max_length=1, default='N')

    class Meta:
        verbose_name_plural = 'cities'

    def __str__(self):
        return self.name


class User(AbstractUser):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING,
                                related_name='users',
                                blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING,
                             related_name='users',
                             blank=True, null=True)
    biography = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def last_five_posts(self):
        return self.posts.all().order_by('-created_datetime')[:5]


class UserInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             related_name='interests')
    interest = models.ForeignKey(Interest, on_delete=models.DO_NOTHING,
                                 related_name='user_interests')

    class Meta:
        unique_together = ('user', 'interest', )

    def __str__(self):
        return f'{self.user.username} - {self.interest.name}'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING,
                             related_name='posts')
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=1000)
    created_datetime = models.DateTimeField()
    created_by = models.BigIntegerField()
    modified_datetime = models.DateTimeField(blank=True, null=True)
    modified_by = models.BigIntegerField(blank=True, null=True)

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.DO_NOTHING,
                             related_name='subscribing',
                             blank=True, null=True)
    subscribed_to_user = models.ForeignKey(User,
                                           on_delete=models.DO_NOTHING,
                                           related_name='subscribers',
                                           blank=True, null=True)
    created_datetime = models.DateTimeField()

    class Meta:
        unique_together = ('user', 'subscribed_to_user', )

    def __str__(self):
        return f'Subscription from: ' \
               f'{self.user.username} , to: ' \
               f'{self.subscribed_to_user.username}'

