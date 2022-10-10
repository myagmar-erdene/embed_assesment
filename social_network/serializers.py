from django.utils import timezone

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .token_generator import create_or_update_auth_token
from .models import UserInterest, Country, City, Interest, Post, Subscription

from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True,
                                     validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', )

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        # I personally think that the Users should get an Authentication Token
        # issued for the first time when they log in, due to security reasons!

        # _ = create_or_update_auth_token(user=user)
        return user


class UserInterestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False,
                                              queryset=User.objects.all())

    class Meta:
        model = UserInterest
        fields = ('id', 'user', 'interest', )
        depth = 1


class UserInterestCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=User.objects.all()
    )
    interest = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Interest.objects.all()
    )

    class Meta:
        model = UserInterest
        fields = ('id', 'user', 'interest', )


class UserInterestForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ('id', 'interest', )
        depth = 1


class UserSerializer(serializers.ModelSerializer):
    interests = UserInterestForUserSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'biography',
            'country',
            'city',
            'birth_date',
            'interests'
        )


class UserInterestUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = UserInterest
        fields = ('id', 'interest', )


class UserUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    interests = UserInterestUpdateSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'biography',
            'country',
            'city',
            'birth_date',
            'interests'
        )

    def update(self, instance, validated_data):
        user_interests = validated_data.pop('interests')

        # Updating the User instance
        instance.first_name = validated_data.get('first_name', instance.first_name)  # noqa
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.country = validated_data.get('country', instance.country)
        instance.city = validated_data.get('city', instance.city)
        instance.biography = validated_data.get('biography', instance.biography)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)  # noqa
        instance.save()

        # Creating a new UserInterest instances and gathering the
        # UserInterest instances which should not be deleted
        keep_user_interests = []
        for user_interest in user_interests:
            if 'id' in user_interest.keys():
                if UserInterest.objects.filter(id=user_interest['id']).exists():
                    keep_user_interests.append(user_interest['id'])
                else:
                    continue
            else:
                user_interest_instance = UserInterest.objects.create(
                    interest=user_interest['interest'],
                    user=instance
                )
                keep_user_interests.append(user_interest_instance.id)

        # Deleting the removed UserInterest instances
        for user_interest in instance.interests.all():
            if user_interest.id not in keep_user_interests:
                user_interest.delete()

        return instance


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', )


class CountryCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = ('id', 'name', )


class CountryUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = ('id', 'name', )


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'country', 'is_capital', )
        depth = 1


class CityCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    country = serializers.PrimaryKeyRelatedField(many=False,
                                                 queryset=Country.objects.all())

    class Meta:
        model = City
        fields = ('id', 'country', 'name', 'is_capital', )


class CityUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    country = serializers.PrimaryKeyRelatedField(many=False,
                                                 queryset=Country.objects.all())

    class Meta:
        model = City
        fields = ('id', 'country', 'name', 'is_capital', )


class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'name', )


class InterestCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Interest
        fields = ('id', 'name', )


class InterestUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Country
        fields = ('id', 'name', )


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'title', 'text', 'created_datetime', 'created_by',
            'modified_datetime', 'modified_by'
        )


class PostCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializer(required=False)
    created_datetime = serializers.DateTimeField(required=False)
    created_by = serializers.IntegerField(required=False)
    modified_datetime = serializers.DateTimeField(required=False)
    modified_by = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'title', 'text', 'created_datetime', 'created_by',
            'modified_datetime', 'modified_by'
        )

    def create(self, validated_data):
        user = self.context.get("request").user
        validated_data['user'] = user
        validated_data['created_datetime'] = timezone.now()
        validated_data['created_by'] = user.id
        return Post.objects.create(**validated_data)


class PostUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializer(required=False)
    created_datetime = serializers.DateTimeField(required=False)
    created_by = serializers.IntegerField(required=False)
    modified_datetime = serializers.DateTimeField(required=False)
    modified_by = serializers.IntegerField(required=False)

    class Meta:
        model = Post
        fields = (
            'id', 'user', 'title', 'text', 'created_datetime', 'created_by',
            'modified_datetime', 'modified_by'
        )

    def update(self, instance, validated_data):
        user = self.context.get("request").user

        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.modified_datetime = timezone.now()
        instance.modified_by = user.id
        instance.save()
        return instance


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    subscribed_to_user = UserSerializer()

    class Meta:
        model = Subscription
        fields = ('id', 'user', 'subscribed_to_user', 'created_datetime', )


class UserDetailedSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, source='last_five_posts')
    interests = UserInterestForUserSerializer(many=True)
    posts_count = serializers.SerializerMethodField()
    subscriptions_count = serializers.SerializerMethodField()
    subscribers_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'username',
            'email',
            'biography',
            'country',
            'city',
            'birth_date',
            'posts',
            'interests',
            'posts_count',
            'subscriptions_count',
            'subscribers_count'
        )

    def get_posts_count(self, instance):
        return Post.objects.filter(user=instance.id).count()

    def get_subscriptions_count(self, instance):
        return Subscription.objects.filter(user=instance.id).count()

    def get_subscribers_count(self, instance):
        return Subscription.objects.filter(subscribed_to_user=instance.id).count()  # noqa
