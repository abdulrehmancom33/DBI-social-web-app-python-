from rest_framework import serializers
from .models import *

#from rest_framework import Breed

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model= Breed
        fields= '__all__'



class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model=Image
        fields=  '__all__'
    






class DogSerializer(serializers.ModelSerializer):
 
    dog_breed=BreedSerializer()
    dog_user=UserSerializer()
    class Meta:
        model = Dog
        fields = ('id','dog_acc','dog_image','dog_breed','dog_user', 'Remarks', 'isDog')

class Feed_ItemSerializer(serializers.ModelSerializer):
    
    
    feed_item_dog=DogSerializer()
    

    class Meta:
        model = Feed_Item
        fields = ('id', 'feed_item_desc','feed_item_dog', 'Feed_user', 'isSaveFeed')
        

class Liked_DogSerializer(serializers.ModelSerializer):
    
    

    liked_user=UserSerializer()
    liked_feed_item=Feed_ItemSerializer()
    class Meta:
        model = Liked_Dog
        fields = ('id', 'liked_user','liked_feed_item')








