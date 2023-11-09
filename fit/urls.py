from django.urls import path
from graphene_django.views import GraphQLView
from .views import baseview,logoutview,homeview
from django.views.decorators.csrf import csrf_exempt

from graphql_jwt.middleware import JSONWebTokenMiddleware


urlpatterns = [
    path("graphql",csrf_exempt( GraphQLView.as_view(graphiql=True))),
    path("login",baseview,name="base"),
    path("logout",logoutview),
    path("home",homeview)
]
