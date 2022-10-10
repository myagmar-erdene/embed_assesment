import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics

from django.utils import timezone
from django.http import Http404, HttpResponseServerError
from django.db.models import Count
from django.contrib.auth import login, logout

from .serializers import \
    RegisterSerializer, \
    UserSerializer, \
    UserUpdateSerializer, \
    UserDetailedSerializer, \
    CountrySerializer, \
    CountryCreateSerializer, \
    CountryUpdateSerializer, \
    CitySerializer, \
    CityCreateSerializer, \
    CityUpdateSerializer, \
    InterestSerializer, \
    InterestCreateSerializer, \
    InterestUpdateSerializer, \
    UserInterestSerializer, \
    UserInterestCreateSerializer, \
    PostSerializer, \
    PostCreateSerializer, \
    PostUpdateSerializer, \
    SubscriptionSerializer

from .models import Country, City, Interest, UserInterest, Post, Subscription

from .token_generator import create_or_update_auth_token

from django.contrib.auth import get_user_model
User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    This view is used for to register a new User.

    It contains the following validations:
    1. Checks if the username is already taken.
    2. Checks if the two passwords match each other
    3. Checks if the password is strong enough to match the certain criteria
    such as: to be at least 10 characters long, to consist of at least 1
    uppercase, 1 lowercase letter, 1 number and 1 special character.

    If the registration succeeds, then a new Authentication Token is issued
    for each user.
    """
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer


class LoginView(APIView):
    """
    This view is used for to log in the specific User into the site using its
    username and password.

    It validates if the users given username and password do match with
    each other.

    If the login succeeds, then a new Authentication Token is issued
    for each user.
    """
    permissions_classes = (AllowAny, )

    def post(self, request):
        content = {'message': 'Login success'}
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        # Creating a new token each time when the User logs in
        _ = create_or_update_auth_token(user=user)
        return Response(content, status.HTTP_200_OK)


class LogoutView(APIView):
    """
    This view is used for to log out the specific User from the site.

    On logout the Authentication Token is removed from each user and
    the new Authentication Token is issued on their next login.
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        content = {'message': 'Logout success'}
        request.user.auth_token.delete()
        logout(request)
        return Response(content, status.HTTP_200_OK)


class UserProfileView(APIView):
    """
    This view is used for to show and/or update the User's profile details.

    Using the PUT method the users are able to update the following fields:
    1. First name
    2. Last name
    3. email
    4. country
    5. city
    6. biography
    7. birth_date
    8. The list of interests
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CountriesView(APIView):
    """
    This view is used for to:

    1. Retrieve all available Countries list
    2. Add a new Country
    3. Update the existing Country's name
    4. Remove the specific Country
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CountryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        country = Country.objects.get(id=request.data.get('id'))
        serializer = CountryUpdateSerializer(
            country, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        country = Country.objects.get(id=request.data.get('id'))
        country.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CitiesView(APIView):
    """
    This view is used for to:

    1. Retrieve all available Cities with their Countries list
    2. Add a new City
    3. Update the existing City's name
    4. Remove the specific City
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        cities = City.objects.select_related(
            'country'
        ).all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CityCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        city = City.objects.get(id=request.data.get('id'))
        serializer = CityUpdateSerializer(
            city, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        city = City.objects.get(id=request.data.get('id'))
        city.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class InterestsView(APIView):
    """
    This view is used for to:

    1. Retrieve all available Interests list
    2. Add a new Interest
    3. Update the existing Interest's name
    4. Remove the specific Interest
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        interests = Interest.objects.all()
        serializer = InterestSerializer(interests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InterestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        interest = Interest.objects.get(id=request.data.get('id'))
        serializer = InterestUpdateSerializer(
            interest, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        interest = Interest.objects.get(id=request.data.get('id'))
        interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserInterestsView(APIView):
    """
    This view is used for to:

    1. Retrieve all available UserInterests list
    2. Add a new Interest to specific User
    3. Update the existing specific User's Interest's name
    4. Remove the specific User's specific Interest
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id=None):
        if user_id:
            user_interests = UserInterest.objects.filter(user=user_id)
        else:
            user_interests = UserInterest.objects.all()

        serializer = UserInterestSerializer(user_interests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserInterestCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        user_interest = UserInterest.objects.get(id=request.data.get('id'))
        serializer = UserInterestCreateSerializer(
            user_interest, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        user_interest = UserInterest.objects.get(id=request.data.get('id'))
        user_interest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostsView(APIView):
    """
    This view is used for to:

    1. Retrieve the list of all Posts the specific User currently has by
    filtering them by the given title, text, start_date and end_date
    parameters
    2. Create a new Post
    3. Update the existing Post
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        title = request.GET.get('title')
        text = request.GET.get('text')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        posts = Post.objects.select_related(
            'user'
        ).filter(
            user__id=request.user.id
        ).order_by('-created_datetime')

        if title:
            posts = posts.filter(title__icontains=title)

        if text:
            posts = posts.filter(text__icontains=text)

        if start_date and end_date:
            posts = posts.filter(created_datetime__gte=start_date)
            posts = posts.filter(created_datetime__lte=end_date)

        elif start_date and not end_date:
            posts = posts.filter(created_datetime__gte=start_date)

        elif not start_date and end_date:
            posts = posts.filter(created_datetime__lte=end_date)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostCreateSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request):
        post = Post.objects.get(id=request.data.get('id'))
        serializer = PostUpdateSerializer(
            post, data=request.data, partial=True, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserSubscriptionsView(APIView):
    """
    This view is used for to:

    1. Retrieve the list of all Subscriptions the specific User currently has
    by filtering them by the given usernames list, title, text, start_date
    and end_date parameters
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        usernames = request.GET.getlist('username')
        title = request.GET.get('title')
        text = request.GET.get('text')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        subscriptions = Subscription.objects.select_related(
            'user',
            'subscribed_to_user'
        ).prefetch_related(
            'subscribed_to_user__posts'
        ).filter(
            user=request.user.id
        ).order_by('-created_datetime')

        # Making sure that the list of usernames to have up to 10 usernames
        if usernames and isinstance(usernames, list) and len(usernames) <= 10:
            subscriptions = subscriptions.filter(
                subscribed_to_user__username__in=usernames
            )

        if title:
            subscriptions = subscriptions.filter(
                subscribed_to_user__posts__title__icontains=title
            )

        if text:
            subscriptions = subscriptions.filter(
                subscribed_to_user__posts__text__icontains=text
            )

        if start_date and end_date:
            subscriptions = subscriptions.filter(
                subscribed_to_user__posts__created_datetime__gte=start_date
            )
            subscriptions = subscriptions.filter(
                subscribed_to_user__posts__created_datetime__lte=end_date
            )

        elif start_date and not end_date:
            subscriptions = subscriptions.filter(
                subscribed_to_user__posts__created_datetime__gte=start_date
            )

        elif not start_date and end_date:
            subscriptions = subscriptions.filter(
                subscribed_to_user__posts__created_datetime__lte=end_date
            )

        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class ManageUserSubscriptionsView(APIView):
    """
    This view is used for to:

    1. Subscribe to a new User
    2. Unsubscribe from the previously subscribed User
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get_user_object(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            logging.error(
                msg='Subscribing to User.DoesNotExist',
                stacklevel=logging.CRITICAL
            )
            raise Http404
        except User.MultipleObjectsReturned:
            logging.error(
                msg='Subscribing to User.MultipleObjectsReturned',
                stacklevel=logging.CRITICAL
            )
            raise HttpResponseServerError

    def get_subscription_object(self, user_id, subscribed_to_user_id):
        try:
            return Subscription.objects.get(
                user_id=user_id,
                subscribed_to_user_id=subscribed_to_user_id
            )
        except Subscription.DoesNotExist:
            logging.error(
                msg='Subscription.DoesNotExist',
                stacklevel=logging.CRITICAL
            )
            raise Http404
        except Subscription.MultipleObjectsReturned:
            logging.error(
                msg='Subscription.MultipleObjectsReturned',
                stacklevel=logging.CRITICAL
            )
            raise HttpResponseServerError

    def post(self, request, subscribed_to_user_id):
        content = {
            'message': 'It is forbidden to have more than 100 Subscriptions'
        }

        user = request.user

        # If the current User's total count of Subscription is more than 100
        if Subscription.objects.filter(user=user.id).count() >= 100:
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        subscribe_to_user = self.get_user_object(user_id=subscribed_to_user_id)

        # If the current User's tries to Subscribe to itself
        if user.id == subscribe_to_user.id:
            content = {
                'message': 'It is forbidden to Subscribe to yourself'
            }
            return Response(content, status=status.HTTP_403_FORBIDDEN)

        Subscription.objects.create(
            user=user,
            subscribed_to_user=subscribe_to_user,
            created_datetime=timezone.now()
        )

        content = {
            'message': f'The User: {user.username} successfully Subscribed '
                       f'to the User: {subscribe_to_user.username}'
        }

        return Response(content, status=status.HTTP_201_CREATED)

    def delete(self, request, subscribed_to_user_id=None):
        user = request.user
        subscribed_to_user = self.get_user_object(user_id=subscribed_to_user_id)

        subscription = self.get_subscription_object(
            user_id=user,
            subscribed_to_user_id=subscribed_to_user.id
        )
        subscription.delete()

        content = {
            'message': f'The User: {user.username} successfully Unsubscribed '
                       f'from the User: {subscribed_to_user.username}'
        }

        return Response(content, status=status.HTTP_201_CREATED)


class UserSubscribersView(APIView):
    """
    This view is used for to retrieve the list of Subscribers the specific
    User currently has.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        subscriptions = Subscription.objects.filter(
            subscribed_to_user=request.user.id
        )
        serializer = SubscriptionSerializer(subscriptions, many=True)
        return Response(serializer.data)


class UserProfileDetailsView(APIView):
    """
    This view is used for to retrieve the total number of Posts, Subscriptions
    and Subscribers the specific User currently has.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        return Response(
            {
                'total_posts_count': Post.objects.filter(
                    user=request.user.id
                ).count(),
                'total_subscriptions_count': Subscription.objects.filter(
                    user=request.user.id
                ).count(),
                'total_subscribers_count': Subscription.objects.filter(
                    subscribed_to_user=request.user.id
                ).count(),
            }
        )


class UsersView(APIView):
    """
    This view is used for to retrieve the User Profiles Info, how many
    subscribers they currently have and their last 5 posts.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        users = User.objects.filter(is_staff=False).exclude(id=request.user.id)
        serializer = UserDetailedSerializer(users, many=True)
        return Response(serializer.data)


class TopTwentyUsersView(APIView):
    """
    This view is used for to retrieve the top 20 most popular User
    Profiles Info, how many subscribers they currently have and their
    last 5 posts.
    """
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        # Filtering the top twenty users with the most subscribers and posts
        top_twenty_users = User.objects.filter(
            is_staff=False
        ).annotate(
            number_of_subscribers=Count('subscribers')
        ).annotate(
            number_of_posts=Count('posts')
        ).order_by('-subscribers').order_by('-number_of_posts')[:20]
        serializer = UserDetailedSerializer(top_twenty_users, many=True)
        return Response(serializer.data)

