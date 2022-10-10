# DOCUMENTATION

## Here are the examples of testing the endpoints:

### User Registration:

The endpoint: localhost:8000/api/register/

The allowed HTTP methods: POST

Receives the following JSON on request POST:
```json
{
    "username": "randomuser1",
    "password": "123EmbedPassword?!",
    "password2": "123EmbedPassword?!"
}
```

### User Login:

The endpoint: localhost:8000/api/login/

Allowed methods: POST

Receives the similar JSON listed below on request POST:
```json
{
    "username": "randomuser1",
    "password": "123EmbedPassword?!"
}
```

### User Logout:

The endpoint: localhost:8000/api/logout/

The allowed HTTP methods: POST

Receives the specific user Authentication Token in request's header in order to
to log out the user.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e


### Retrieving the User Authentication Token using the username and password:

The endpoint: localhost:8000/api/api-token-auth//

Receives the similar JSON listed below on request POST:
```json
{
    "username": "randomuser1",
    "password": "123EmbedPassword?!"
}
```

### User's Profile:

The endpoint: localhost:8000/api/my-profile/

The allowed HTTP methods: GET, PUT

Receives the specific user Authentication Token in request's header in order to
show and/or update the User's profile details.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

Receives the similar JSON listed below on request PUT:
```json
{
    "first_name": "Karl",
    "last_name": "Urban",
    "email": "karl.urban@gmail.com",
    "country": 1,
    "city": 2,
    "biography": "Born in New Zealand in 1972, Karl Urban started starring in stage, TV and film productions in his home country.",
    "birth_date": "1972-01-01",
    "interests": [
        {
            "id": 9,
            "interest": 1
        },
        {
            "interest": 4
        },
        {
            "interest": 5
        }
    ]
}
```

### Countries List:

The endpoint: localhost:8000/api/countries/

The allowed HTTP methods: GET, POST, PUT, DELETE

Receives the specific user Authentication Token in request's header in order to
show, add, update or delete the predefined Countries.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

Receives the similar JSON listed below on request POST:
```json
{
    "name": "Spain"
}
```

Receives the similar JSON listed below on request PUT:
```json
{
    "id": 1,
    "name": "Spain"
}
```

Receives the similar JSON listed below on request DELETE:
```json
{
    "id": 1
}
```

### Cities List:

The endpoint: localhost:8000/api/cities/

The allowed HTTP methods: GET, POST, PUT, DELETE

Receives the specific user Authentication Token in request's header in order to
show, add, update or delete the predefined Cities.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

Receives the similar JSON listed below on request POST:
```json
{
    "name": "Madrid",
    "country": 1,
    "is_capital": "Y"
}
```

Receives the similar JSON listed below on request PUT:
```json
{
    "id": 2,
    "name": "Barcelona",
    "country": 1,
    "is_capital": "N"
}
```

Receives the similar JSON listed below on request DELETE:
```json
{
    "id": 2
}
```

### Interests List:

The endpoint: localhost:8000/api/interests/

The allowed HTTP methods: GET, POST, PUT, DELETE

Receives the specific user Authentication Token in request's header in order to
show, add, update or delete the predefined Interests.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

Receives the similar JSON listed below on request POST:
```json
{
    "name": "Playing guitar"
}
```

Receives the similar JSON listed below on request PUT:
```json
{
    "id": 1,
    "name": "Playing guitars"
}
```

Receives the similar JSON listed below on request DELETE:
```json
{
    "id": 1
}
```

### User Interests List:

The endpoint: localhost:8000/api/user-interests/

The allowed HTTP methods: GET, POST, PUT, DELETE

Receives the specific user Authentication Token in request's header in order to
show, add, update or delete the User's Interests.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

Receives the similar JSON listed below on request POST:
```json
{
    "user": 1,
    "interest": 1
}
```

Receives the similar JSON listed below on request PUT:
```json
{
    "id": 1,
    "user": 1,
    "interest": 2
}
```

Receives the similar JSON listed below on request DELETE:
```json
{
    "id": 1
}
```

### Posts List:

The endpoint: localhost:8000/api/posts/

The allowed HTTP methods: GET, POST, PUT

Receives the specific user Authentication Token in request's header in order to
show, filter, add and update the User's Posts.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

Receives the similar JSON listed below on request POST:
```json
{
    "title": "The best sporting events in town",
    "text": "In Italy, meanwhile, Napoli mean business"
}
```

Receives the similar JSON listed below on request PUT:
```json
{
    "id": 1,
    "title": "The best gaming events in town",
    "text": "In Italy, meanwhile, Napoli mean business"
}
```

### User Subscription:

The endpoint: localhost:8000/api/my-subscriptions/

The allowed HTTP methods: GET

Receives the specific user Authentication Token in request's header in order to
show and filter the User's Subscriptions.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

### User Subscription Manage:

The endpoint: localhost:8000/api/my-subscriptions-manage/

The allowed HTTP methods: POST, DELETE

Receives the specific user Authentication Token in request's header in order to
add or delete the User's Subscriptions.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

Receives the User ID which user is subscribing to on request POST and DELETE.

### User Subscribers:

The endpoint: localhost:8000/api/my-subscribers/

The allowed HTTP methods: GET

Receives the specific user Authentication Token in request's header in order to
show the User's Subscribers.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

### User Profile Details:

The endpoint: localhost:8000/api/my-profile-details/

The allowed HTTP methods: GET

Receives the specific user Authentication Token in request's header in order to
show the total number of posts, subscriptions and subscribers the User
currently has.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

### Users View:

The endpoint: localhost:8000/api/users/

The allowed HTTP methods: GET

Receives the specific user Authentication Token in request's header in order to
show how many subscribers the User currently has and their last 5 posts.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

### Top 20 Users View:

The endpoint: localhost:8000/api/top-twenty-users/

The allowed HTTP methods: GET

Receives the specific user Authentication Token in request's header in order to
show the top 20 most popular User Profiles, how many subscribers they currently
have and their last 5 posts.

For example: Key: Authorization, Value: Token f0a48e30a284f13a60b5bda123b0a13e

