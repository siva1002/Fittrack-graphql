from .fit_getschemas import UserGet, WorkOutGet, TrackingsGet, FriendsGet, ExcerciseGet
from .fit_mutations import (UserCreate, WorkOutCreate, FriendsCreate,
                            ExcerciseCreate, TrackingCreate, TrackingUpdate,
                            AcceptOrRejectFriendRequest, RemoveFollower,
                            CreateChallenge)
import graphene
import graphql_jwt
from .models import User, Friends, Workouts, Excercise, Trackings
from graphql import GraphQLError
from django.db.models import Avg, Sum, Subquery, Count
from django.db.models import F, Q
from django.db import connection


class LoggedinUser(graphene.ObjectType):
    loggedin_user = graphene.Field(UserGet)

    def resolve_loggedin_user(root, info):
        if info.context.user.is_authenticated:
            return info.context.user
        return GraphQLError("Not authenticated")


class UserQuery(graphene.ObjectType):
    user = graphene.Field(UserGet, id=graphene.ID())

    def resolve_user(self, info, id=None):
        if id:
            user = User.objects.get(pk=id)
            print(user, "queried user")
            return user
        return User.objects.all()


class FollowersFollowingsQuery(graphene.ObjectType):
    friends = graphene.List(FriendsGet, type=graphene.String())
    friendscount = graphene.Int()

    def resolve_friends(root, info, type):
        user = info.context.user
        if 'followers' in type:
            friends = Friends.objects.filter(userfriend=user.id, accepted=True)
        if 'following' in type:
            friends = Friends.objects.filter(user=user.id, accepted=True)
        return friends

    def resolve_friendscount(root, info):
        return info.context.user.friends.all().count()


class NonFriendUsersQuery(graphene.ObjectType):
    nonfriendusers = graphene.List(UserGet)

    def resolve_nonfriendusers(root, info):
        user = info.context.user
        following = [
            i.userfriend.id for i in user.following.filter(accepted=True)]
        non_friend_objs = User.objects.filter(
            ~Q(id__in=following), is_superuser=False,).exclude(id=user.id)
        return non_friend_objs


class FriendRequestQuery(graphene.ObjectType):
    friendsrequests = graphene.List(FriendsGet)

    def resolve_friendsrequests(root, info):
        user = info.context.user
        friends = Friends.objects.filter(
            userfriend=user, accepted=False, requeststatus__icontains="pending")
        return friends


class WorkoutQuery(graphene.ObjectType):
    workout = graphene.List(WorkOutGet)

    def resolve_workout(root, info):
        user = info.context.user
        workouts = Workouts.objects.prefetch_related().filter(Q(user=user, track__started=True)).annotate(totalduration=Sum(
            "track__duration"), count=Count('track', filter=Q(track__started=False)), started=F("track__started"),)
        if not workouts:
            workouts = Workouts.objects.filter(user=user).annotate(totalduration=Sum(
                "track__duration"), count=Count('track', filter=Q(track__started=False)), started=F("track__started"))
        print(workouts)
        return workouts


class ExerciseQuery(graphene.ObjectType):
    exercise = graphene.List(ExcerciseGet, id=graphene.String())

    def resolve_exercise(root, info, id=None):
        user = info.context.user
        if id:
            workouts = Workouts.objects.prefetch_related(
                'exercise').get(id=id).exercise.all()
            return workouts
        workouts = Workouts.objects.prefetch_related(
            'exercise').filter(user=user.id)
        exercises = Excercise.objects.filter(
            workout__in=(obj.id for obj in workouts))
        return exercises


class TrackingsQuery(graphene.ObjectType):
    trackings = graphene.List(TrackingsGet, id=graphene.String())

    def resolve_trackings(root, info, id=None):
        user = info.context.user
        if id:
            trackings = Trackings.objects.filter(workout_id=id)
            return trackings
        trackings = Trackings.objects.filter(
            workout__in=(obj.id for obj in user.workouts.all()))
        return trackings


class Mutation(graphene.ObjectType):
    user_create = UserCreate.Field()
    workout_create = WorkOutCreate.Field()
    createfriendrequest = FriendsCreate.Field()
    excercise = ExcerciseCreate.Field()
    trackings_create = TrackingCreate.Field()
    trackings_update = TrackingUpdate.Field()
    friendrequestupdate = AcceptOrRejectFriendRequest.Field()
    unfollow = RemoveFollower.Field()
    createchallenge=CreateChallenge.Field()

    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(UserQuery, LoggedinUser, WorkoutQuery, FollowersFollowingsQuery, ExerciseQuery, TrackingsQuery, FriendRequestQuery, NonFriendUsersQuery):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
