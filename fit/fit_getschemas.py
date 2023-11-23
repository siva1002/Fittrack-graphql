from graphene_django import DjangoObjectType
import graphene
from .models import User,Workouts,Trackings,Friends,Excercise,Challenges
from datetime import timedelta
import datetime



class UserGet(DjangoObjectType):
    class Meta:
        model=User
        fields=("email","username","id","workouts","challenges")

class WorkOutGet(DjangoObjectType):
    class Meta:
        model=Workouts
        fields=("id","name","description","exercise","totalduration","count","category","started")
    totalduration=graphene.String()
    count=graphene.String()
    started=graphene.Boolean()


    @staticmethod
    def resolve_totalduration(root, info, **kwargs):
        if hasattr(root, 'totalduration'):
           return str(root.totalduration)
        timedelta(seconds=0)
    
    @staticmethod
    def resolve_count(root, info, **kwargs):
        print(root.__dict__)
        if hasattr(root,'count'):
            return (str(root.count))
        return str(0)
    
    @staticmethod
    def resolve_started(root,info,**kwargs):
        return bool(hasattr(root,'started'))


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
        fields=("workout","duration","started")
    
    def resolve_duration(self, info):
        return float(self.duration.total_seconds())/60
    
class ChallengesGet(DjangoObjectType):
    class Meta:
        model=Challenges
        fields=("challenge","id")