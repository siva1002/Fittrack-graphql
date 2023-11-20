import graphene

class UserInputs(graphene.InputObjectType):
    username=graphene.String(required=True)
    friend=graphene.ID(required=False)
    email=graphene.String(required=True)
    password=graphene.String(required=True)
    confirmpassword=graphene.String(required=True)

class WorkOutInputs(graphene.InputObjectType):
    name=graphene.String(required=True)
    description=graphene.String(required=True)

class FriendsInputs(graphene.InputObjectType):
    name=graphene.String(required=True)

class ExcerciseInputs(graphene.InputObjectType):
    exercise=graphene.String(required=True)
    reps=graphene.Int()
    sets=graphene.Int()
    duration=graphene.Int()
    workoutid=graphene.Int()

class TrackInputs(graphene.InputObjectType):
    start=graphene.Boolean()
    workout=graphene.Int()
    
class TrackUpdateInputs(graphene.InputObjectType):
    workout=graphene.Int()


class FriendRequestStatusInputs(graphene.InputObjectType):
    id=graphene.String()
    status=graphene.String()