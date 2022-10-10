from django.contrib import admin
from .models import \
    User, \
    Interest, \
    UserInterest, \
    Country, \
    City, \
    Post, \
    Subscription

admin.site.register(User)
admin.site.register(Interest)
admin.site.register(UserInterest)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Post)
admin.site.register(Subscription)

