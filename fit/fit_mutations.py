import graphene
from .fit_inputschemas import UserInputs,WorkOutInputs,FriendsInputs,ExcerciseInputs,TrackInputs,TrackUpdateInputs
from .fit_getschemas import UserGet,WorkOutGet,TrackingsGet,FriendsGet,ExcerciseGet
from .models import User,Workouts,Trackings,Friends,Excercise
from graphql import GraphQLError
from datetime import datetime, timedelta,date
import pytz
from django.db.models import F,Q
from django.utils import timezone


class UserCreate(graphene.Mutation):
    user=graphene.Field(UserGet)
    class Arguments:
        userdata=UserInputs(required=True)
    
    @classmethod
    def mutate(cls,root,info,userdata=None,**kwargs):
        if userdata.password != userdata.confirmpassword:
            return GraphQLError('Password and Confirm password not match')
        user=User.objects.create(username=userdata.username,email=userdata.email)
        user.set_password(userdata.password)
        user.save()
        return UserCreate(user=user)

class WorkOutCreate(graphene.Mutation):
    workout=graphene.Field(WorkOutGet)
    class Arguments:
        workoutdata=WorkOutInputs(required=True)

    @classmethod
    def mutate(cls,root,info,workoutdata):
        workout=Workouts.objects.create(name=workoutdata.name,description=workoutdata.description,user=info.context.user)
        workout.save()
        return WorkOutCreate(workout=workout)            


class FriendsCreate(graphene.Mutation):
    friend=graphene.Field(FriendsGet)
    message=graphene.String()
    
    class Arguments:
        frienddata=FriendsInputs(required=True)

    @classmethod
    def mutate(cls,root,info,frienddata):
        user=User.objects.get(username__icontains=frienddata.name)
        exist=info.context.user.friends.filter(userfriend=user).exists()
        if user and not exist :
            frdobj=Friends.objects.create(user=info.context.user,userfriend=user)
            return FriendsCreate(friend=frdobj)
        friend=Friends.objects.get(user=info.context.user,userfriend=user.id)
        return FriendsCreate(friend=friend,message=f"User already your friend {friend.userfriend.username}")

class ExcerciseCreate(graphene.Mutation):
    exercise=graphene.Field(ExcerciseGet)
    message=graphene.String()
    class Arguments:
        exercisedata=ExcerciseInputs(required=True)

    @classmethod
    def mutate(cls,root,info,exercisedata):
        workout=Workouts.objects.get(id=exercisedata.workoutid)
        if workout :
            obj=Excercise.objects.create(workout=workout,exercise=exercisedata.exercise,reps=exercisedata.reps,sets=exercisedata.sets)
            return ExcerciseCreate(exercise=obj,message=f"Exercise Create {obj.exercise}")

class TrackingCreate(graphene.Mutation):
    trackings=graphene.Field(TrackingsGet)
    message=graphene.String()
    status=graphene.Boolean()
    incompleteworkout=graphene.List(WorkOutGet)
    class Arguments:
        trackingsdata=TrackInputs(required=True)

    @classmethod
    def mutate(cls,root,info,trackingsdata):
        user=info.context.user
        utctime=datetime.now(tz=timezone.utc).date()
        # Q(user=user,track__time__contains=utctime,pk=trackingsdata.workout)|
        incompleteworkout=Workouts.objects.filter(Q(user=user,track__started =True)).last()
        if not incompleteworkout :
            print(incompleteworkout)
            workoutobj=Workouts.objects.get(id=trackingsdata.workout)
            d =timedelta(days=0)
            track=Trackings.objects.create(workout=workoutobj,started=trackingsdata.start,duration=d)
            track.save()
            return TrackingCreate(trackings=track,message=f" Workout {workoutobj.name} Started" ,status=True)
        return TrackingCreate(incompleteworkout=incompleteworkout,message=f"Complete this previous workout",status=True)

class TrackingUpdate(graphene.Mutation):
    trackings=graphene.Field(TrackingsGet)
    message=graphene.String()
    class Arguments:
        trackingsdata=TrackUpdateInputs(required=True)

    @classmethod
    def mutate(cls,root,info,trackingsdata):
        user=info.context.user
        try:
            workouts=Workouts.objects.get(user=user,track__started =True)
        except Exception as e:
            print(e)
            workouts=[]
        if workouts:
            track=Trackings.objects.filter(workout=workouts.id,started=True).last()
            startedtime=track.time
            currenttime =datetime.now().replace(tzinfo=pytz.UTC)
            calduration=currenttime-startedtime
            track.duration=calduration
            track.started=False
            track.save()
            return TrackingUpdate(trackings=track,message="updated")
        return {"message":"workout is not started"}


