import graphene
from .fit_inputschemas import (UserInputs, WorkOutInputs, FriendsInputs, 
                               ExcerciseInputs, TrackInputs, TrackUpdateInputs,
                               FriendRequestStatusInputs, CreateChallengeInputs)
from .fit_getschemas import UserGet, WorkOutGet, TrackingsGet, FriendsGet, ExcerciseGet
from .models import User, Workouts, Trackings, Friends, Excercise,Challenges
from graphql import GraphQLError
from datetime import datetime, timedelta, date
import pytz
from django.db.models import Q,Subquery,F
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class UserCreate(graphene.Mutation):
    user = graphene.Field(UserGet)

    class Arguments:
        userdata = UserInputs(required=True)

    @classmethod
    def mutate(cls, root, info, userdata=None, **kwargs):
        if userdata.password != userdata.confirmpassword:
            return GraphQLError('Password and Confirm password not match')
        user = User.objects.create(
            username=userdata.username, email=userdata.email)
        user.set_password(userdata.password)
        user.save()
        return UserCreate(user=user)


class WorkOutCreate(graphene.Mutation):
    workout = graphene.Field(WorkOutGet)

    class Arguments:
        workoutdata = WorkOutInputs(required=True)

    @classmethod
    def mutate(cls, root, info, workoutdata):
        workout = Workouts.objects.create(
            name=workoutdata.name, description=workoutdata.description, user=info.context.user,category=workoutdata.category)
        workout.save()
        return WorkOutCreate(workout=workout)


class FriendsCreate(graphene.Mutation):
    friend = graphene.Field(FriendsGet)
    message = graphene.String()

    class Arguments:
        frienddata = FriendsInputs(required=True)

    @classmethod
    def mutate(cls, root, info, frienddata):
        user = User.objects.get(username__iexact=frienddata.name)
        exist = info.context.user.following.filter(userfriend=user).exists()
        channel_layer = get_channel_layer()
        if user and not exist:
            frdobj = Friends.objects.create(
                user=info.context.user, userfriend=user)
            async_to_sync(channel_layer.group_send)(str(user.id), {
                "type": "sendMessage", "message": f"User sent friend creation request {info.context.user.username}"})
            return FriendsCreate(friend=frdobj)
        async_to_sync(channel_layer.group_send)(str(user.id), {
            "type": "sendMessage", "message": f"User sent friend creation request {info.context.user.username}"})
        friend = Friends.objects.get(
            user=info.context.user, userfriend=user.id)
        return FriendsCreate(friend=friend, message=f"User already your friend {friend.userfriend.username}")


class ExcerciseCreate(graphene.Mutation):
    exercise = graphene.Field(ExcerciseGet)
    message = graphene.String()

    class Arguments:
        exercisedata = ExcerciseInputs(required=True)

    @classmethod
    def mutate(cls, root, info, exercisedata):
        workout = Workouts.objects.get(id=exercisedata.workoutid)
        if workout and 'workout' in workout.category:
            obj = Excercise.objects.create(
                workout=workout, exercise=exercisedata.exercise, reps=exercisedata.reps, sets=exercisedata.sets,duration=exercisedata.duration)
            return ExcerciseCreate(exercise=obj, message=f"Exercise Create {obj.exercise}")
        return ExcerciseCreate(exercise={},message=f'Creating exercise is not applicable for non "Workout" category workout')


class TrackingCreate(graphene.Mutation):
    trackings = graphene.Field(TrackingsGet)
    message = graphene.String()
    status = graphene.Boolean()
    # prev = graphene.Field(WorkOutGet)

    class Arguments:
        trackingsdata = TrackInputs(required=True)

    @classmethod
    def mutate(cls, root, info, trackingsdata):
        user = info.context.user
        utctime = datetime.now(tz=timezone.utc).date()
        # Q(user=user,track__time__contains=utctime,pk=trackingsdata.workout)|
        incompleteworkout = Workouts.objects.prefetch_related("track").filter(
            Q(user=user, track__started=True)).last()
        if not incompleteworkout:
            workoutobj = Workouts.objects.get(id=trackingsdata.workout)
            d = timedelta(days=0)
            track = Trackings.objects.create(
                workout=workoutobj, started=trackingsdata.start, duration=d)
            track.save()
            return TrackingCreate(trackings=track, message=f" Workout {workoutobj.name} Started", status=True)
        return TrackingCreate(message=f"Complete this previous workout", status=True)


class TrackingUpdate(graphene.Mutation):
    trackings = graphene.Field(TrackingsGet)
    message = graphene.String()
    status=graphene.Int()

    class Arguments:
        trackingsdata = TrackUpdateInputs(required=True)

    @classmethod
    def mutate(cls, root, info, trackingsdata):
        user = info.context.user
        try:
            workouts = Workouts.objects.get(user=user, track__started=True)
        except Exception as e:
            print(e)
            workouts = []
        if workouts:
            track = Trackings.objects.filter(
                workout=workouts.id, started=True).last()
            startedtime = track.time
            currenttime = datetime.now().replace(tzinfo=pytz.UTC)
            calduration = currenttime-startedtime
            track.duration = calduration
            track.started = False
            track.save()
            return TrackingUpdate(trackings=track, message="updated",status=200)
        return {"message": "workout is not started"}


class AcceptOrRejectFriendRequest(graphene.Mutation):
    status=graphene.String()
    class Arguments:
        requestdata=FriendRequestStatusInputs(required=True)

    @classmethod
    def mutate(cls, root, info, requestdata):
        request=Friends.objects.get(id=requestdata.id)
        if request:
            request.requeststatus="Accepted" if "accept" in requestdata.status else "Rejected"
            request.accepted=True if "accept" in requestdata.status else False
            request.save()
        return AcceptOrRejectFriendRequest(status=requestdata.status)
        

class RemoveFollower(graphene.Mutation):
    message=graphene.String()
    class Arguments:
        id=graphene.String()
    
    @classmethod
    def mutate(cls, root, info, id):
        user=info.context.user
        obj=Friends.objects.get(user=user,userfriend=id)
        if obj:
            obj.delete()
        return RemoveFollower(message={"message":f"Unfollowed user {obj.username}"})

class CreateChallenge(graphene.Mutation):
    message=graphene.String()
    class Arguments:
        cha=CreateChallengeInputs()

    @classmethod
    def mutate(cls, root, info, cha):
        user=info.context.user
        workout=user.workouts.get(id=cha.workout)
        challengeuser=User.objects.prefetch_related('challenges').get(pk=cha.user)
        exist=challengeuser.challenges.filter(challenge=cha.workout).exists()
        if workout and not exist:
            createchallenge=Challenges.objects.create(user=challengeuser,challenge=workout,challengeduser=user)
            createchallenge.save()
            return CreateChallenge(message=f"{workout.name} challenged for user {challengeuser.username}")
        return CreateChallenge(message=f"{workout.name} already challenged {challengeuser.username}")

