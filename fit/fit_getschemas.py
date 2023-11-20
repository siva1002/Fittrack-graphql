from graphene_django import DjangoObjectType
import graphene
from .models import User,Workouts,Trackings,Friends,Excercise
from datetime import timedelta
import datetime



class UserGet(DjangoObjectType):
    class Meta:
        model=User
        fields=("email","username","id","workouts")

class WorkOutGet(DjangoObjectType):
    class Meta:
        model=Workouts
        fields=("id","name","description","exercise","totalduration")
    totalduration=graphene.String()

    @staticmethod
    def resolve_totalduration(root, info, **kwargs):
        if root.totalduration is not None:
           return str(root.totalduration)
        timedelta(seconds=0)



class TrackingsGet(DjangoObjectType):
    class Meta:
        model=Trackings
        
        fields=("workout","duration")
    
    def resolve_duration(self, info):
        return float(self.duration.total_seconds())/60
    

class FriendsGet(DjangoObjectType):
    class Meta:
        model=Friends
        fields="__all__"
        

class ExcerciseGet(DjangoObjectType):
    class Meta:
        model=Excercise
        fields="__all__"

class TrackingsGet(DjangoObjectType):
    class Meta:
        model=Trackings
        fields=("workout","duration")
    
    def resolve_duration(self, info):
        return float(self.duration.total_seconds())/60