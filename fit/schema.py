from .fit_getschemas import UserGet,WorkOutGet,TrackingsGet,FriendsGet,ExcerciseGet
from .fit_mutations import UserCreate,WorkOutCreate,FriendsCreate,ExcerciseCreate,TrackingCreate,TrackingUpdate
import graphene
import graphql_jwt
from .models import User,Friends,Workouts,Excercise,Trackings
from graphql import GraphQLError
from django.db.models import Avg,Sum,Subquery
from django.db.models import F,Q



class LoggedinUser(graphene.ObjectType):
    loggedin_user=graphene.Field(UserGet)

    def resolve_loggedin_user(root,info):
        print(root,"root")
        if info.context.user.is_authenticated:
            return info.context.user
        return GraphQLError("Not authenticated")

class UserQuery(graphene.ObjectType):
    user=graphene.List(UserGet,id=graphene.ID())
    def resolve_user(self, info,id=None):
        if id:
           user=User.objects.filter(pk=id)
           print(User.objects.get(pk=id).user.all())
           return user
        return User.objects.all()

class FriendsQuery(graphene.ObjectType):
    friends=graphene.List(FriendsGet)
    friendscount=graphene.Int()

    def resolve_friends(root,info):
        user=info.context.user
        friends=Friends.objects.filter(user=user)
        return friends
    
    def resolve_friendscount(root,info):
        return info.context.user.friends.all().count()


class WorkoutQuery(graphene.ObjectType):
    workout=graphene.List(WorkOutGet)

    def resolve_workout(root,info):
        user=info.context.user
        workouts=Workouts.objects.filter(Q(user=user,track__started =True)).annotate(totalduration=Sum("track__duration"))
        if not workouts:
            workouts=Workouts.objects.filter(user=user).annotate(totalduration=Sum("track__duration"))

        return workouts
    
class ExerciseQuery(graphene.ObjectType):
    exercise=graphene.List(ExcerciseGet,id=graphene.String())

    def resolve_exercise(root,info,id=None):
        user=info.context.user
        if id:
            workouts=Workouts.objects.get(id=id).exercise.all()
            return workouts
        workouts=Workouts.objects.filter(user=user.id)
        exercises=Excercise.objects.filter(workout__in=(obj.id for obj in workouts))
        return exercises

class TrackingsQuery(graphene.ObjectType):
    trackings=graphene.List(TrackingsGet,id=graphene.String())
    
    def resolve_trackings(root,info,id=None):
        user=info.context.user
        if id:
            trackings=Trackings.objects.filter(workout_id=id)
            return trackings
        trackings=Trackings.objects.filter(workout__in=(obj.id for obj in user.workouts.all()))
        return trackings







class Mutation(graphene.ObjectType):
    user_create=UserCreate.Field()
    workout_create=WorkOutCreate.Field()
    friends=FriendsCreate.Field()
    excercise=ExcerciseCreate.Field()
    trackings_create=TrackingCreate.Field()
    trackings_update=TrackingUpdate.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

class Query(UserQuery,LoggedinUser,WorkoutQuery,FriendsQuery,ExerciseQuery,TrackingsQuery):
    pass

schema=graphene.Schema(query=Query,mutation=Mutation)
