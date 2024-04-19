from django.shortcuts import render
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout as d_logout
from .serializers import *
from .models import *
from django.utils.datastructures import MultiValueDictKeyError
# from pprint import pprint
import json
from rest_framework.decorators import api_view
from rest_framework.parsers import FileUploadParser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout
from rest_framework import authentication, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status , generics , mixins,filters,viewsets
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
# from django.contrib.auth.hashers import *
import boto3 from rest_framework.status import (
    HTTP_201_CREATED
)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token. objects.create(user=instance)

#  SIGNUP API
class signUp(APIView):
    
    def post(self, request, format = json):
        print("In Login View")
        
        email = request.data.get("email")
        password = request.data.get("password")
        fullname = request.data.get("full_name")
        city = request.data.get("city")
        country = request.data.get("country")
        resetkey = request.data.get("resetkey")
        # print(email,fullname, password,city,country)
        # print(resetkey)

        if resetkey is None:
            return Response({
                     "Status": "Reset Key is Required",
                      "user" : None
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            resetkey = request.data.get("resetkey").lower()
            print(resetkey)

        serialized = UserSerializer(data=request.data)
        
        if serialized.is_valid():
            user = User.objects.create_user(
                email = email,
                full_name = fullname,
                password = password,
                city = city,
                country = country,
                resetkey = resetkey
            )

            fnl_JSON = {
                "id": user.id,
                "password": user.password,
                "email": user.email,
                "resetkey": user.resetkey,
                "full_name": user.full_name,
                "city": user.city,
                "country": user.country,
                "last_login": "",
                "active": user.active,
                "staff": user.staff,
                "admin": user.admin,
            }

            return Response({
                     "Status": "Success",
                      "user" : fnl_JSON
                } , status=status.HTTP_201_CREATED)
        else:
            for key in serialized._errors:
                return Response({
                     "Status": "%s" % (serialized._errors[key][0]),
                      "user" : None
                }, status=status.HTTP_400_BAD_REQUEST)

# LOGIN API
class authenticate(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    print(UserSerializer.get_attribute)
    def post(self, request, format = json):
        print("In Login View")
        email = request.data.get("email")
        password = request.data.get("password")
        serializer_class = UserSerializer
        
        if email and password:
            users = User.objects.filter(email = email , password = password)
            if users:
                user = User.objects.get(email = email , password = password)

                fnl_JSON = {
                "id": user.id,
                "password": user.password,
                "email": user.email,
                "resetkey": user.resetkey,
                "full_name": user.full_name,
                "city": user.city,
                "country": user.country,
                "last_login": "",
                "active": user.active,
                "staff": user.staff,
                "admin": user.admin,
                }

                return Response({
                     "Status": "Success",
                      "user" : fnl_JSON
                })
            else:
                fnl_JSON = {
                "id": None,
                "password": None,
                "email": None,
                "resetkey": None,
                "full_name": None,
                "city": None,
                "country": None,
                "last_login": "",
                "active": False,
                "staff": False,
                "admin": False,
                }
                return Response({
                    "Status" : "Failure",
                    "user" : fnl_JSON
                })

# LOGOUT API
class LogoutView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        # simply delete the token to force a login
        # request.user.auth_token.delete()
        userid=self.request.data["userid"]
        #userid = self.request.user.id
        try:
            user = User.objects.get(id=userid)
            return Response({
                "Status" : "Success"
            
            })
        except :
            return Response({
                "Status" : "Failure"
            })

# GET BREED API
class BreedListView(generics.ListCreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


# GET FEED DETAIL API
class Feed_Details(APIView):
    def post(self, request, *args, **kwargs):

        feedid=self.request.data["feedid"]
        if  feedid is not None:
            feedsid=Feed_Item.objects.filter(id=feedid)
            if feedsid is not None:
                
                file_serializer = Feed_ItemSerializer(feedsid,many=True)
            #imageid=request.data.get("media_type")
            
                return Response(file_serializer.data)
            else:
                return Response({"detail":"Data not available"})

# GET DOG FEEDS (ALL) API
class Feed_ItemListView(generics.ListCreateAPIView):
    queryset = Feed_Item.objects.all()
    serializer_class = Feed_ItemSerializer

# UPLOAD IMAGE API
class UploadViewSet(APIView):
   def post(self, request, *args, **kwargs):
        serializer_class = ImageSerializer
        mediaurl = self.request.data["fileToUpload"]
        print(mediaurl)
        if mediaurl is not None:
            file_serializer = ImageSerializer(data=request.data)
            
            if file_serializer.is_valid():
                file_serializer.save()
                return Response({
                    "status": "Success",
                    "url": "https://dbi-fyp.herokuapp.com/media/ImageRepository/{}".format(mediaurl),
                    "msg": "Your file was uploaded successfully."
                })
            else:
                return Response({
                    "status": "Faliure",
                    "url": None,
                    "msg": "There was an issue while uploading your file."
                })
        else:
           return Response({
                    "status": "Faliure",
                    "url": None,
                    "msg": "There was an issue while uploading your file."
                })
            
# LIKE DOG API
class Likedog(APIView):
        
    def post(self, request, *args, **kwargs):
        try:
            feedid=self.request.data["feedid"]
            feedsid=Feed_Item.objects.get(id=feedid)
            
            userid=self.request.data["userid"]
            users=User.objects.get(id=userid)
        except :
            return Response({
                "Status":"Failure"
            })
        
        Liked_Dog.objects.create(liked_user=users, liked_feed_item=feedsid)
        print(users)
        if  feedsid and users is not None: 
            return Response({
                "Status":"Success"
            })
        else:
            return Response({
                "Status":"Failure"
            })
            
# DISLIKE DOG API
class DislikeDog(APIView):
    def post(self, request, *args, **kwargs):
            # = Feed_ItemSerializer
        feedid=self.request.data["feedid"]
        userid=self.request.data["userid"]
        #userid = self.request.user.id
        try:
            feedsid=Feed_Item.objects.get(id=feedid)
            users=User.objects.get(id=userid)

        except :
            return Response({
                    "Status":"Failure"
                })
        else:
            print("Nothing went wrong")

        
        #userid= self.request.user.id
        
        Liked_Dog_qs = Liked_Dog.objects.filter(liked_user=users, liked_feed_item=feedsid)

        print(Liked_Dog_qs)

        if len(Liked_Dog_qs) == 0:
            return Response({
                "Status":"Failure"
            })
        if Liked_Dog_qs.exists():
            Liked_Dog.objects.filter(liked_user=users,liked_feed_item=feedsid).delete()
        
        if  feedsid and users is not None:
            return Response({
                "Status":"Success"
            })
        else:
            return Response({
                "Status":"Failure"
            })
# SAVE RESULTS API
class SaveResult(APIView):

    def post(self,request, *args, **kwargs):

        try:
            dogid=self.request.data["dogid"]
            dogsid=Dog.objects.get(id=dogid)
            descript=self.request.data['desc']
            userid=self.request.data["userid"]
            users=User.objects.get(id=userid)

        except :
            return Response({
                "Status":"Failure"
            })
        Feed_Item.objects.create(Feed_user=users, feed_item_dog=dogsid, feed_item_desc=descript, isSaveFeed = True)
        if dogsid and users is not None:
            return Response({
                "Status":"Success"
            })
        else:
            return Response({
                "Status":"Failure"
            })
# GET ALL USERS DETAILS API
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # def get_object(self):
    #     pk = self.kwargs.get("pk")

    #     if pk == "current":
    #         print("Here")
    #         return self.request.user
    #     print("Not Here")
    #     return super(UserViewSet, self).get_object()
       
# GET MY SHARED OR SAVED DOG FEEDS API
class Mydogfeeds(APIView):
    
    def post(self,request, *args, **kwargs):
        
        # dogsid=Dog.objects.get(id=dogid)
        userid=self.request.data["userid"]
        try:
            users=User.objects.get(id=userid)
            # dog=Feed_Item.objects.get(Feed_user=users)
            print(users)
        except:
            return Response({
                "Status":"Failure"
            })
        else:
            print("Nothing went wrong")

        res = Feed_Item.objects.filter(Feed_user=users)
        print(list(res))
        # file_serializer = Feed_ItemSerializer(dog, many=True)
        #imageid=request.data.get("media_type")

        file_serializer = Feed_ItemSerializer(res, many=True)
        if res is not None:
            # dogs=Dog.objects.filter(dog_user=user)
            # print(len(dogs))
            return Response(file_serializer.data)
        else:
            return Response({
                "Status":"No Data Found."
            })

# GET MY LIKED FEEDS API
class MyLikedFeeds(APIView):
    
    def post(self,request, *args, **kwargs):
        
        check = self.request.data["userid"]
        try:
            user= User.objects.get(id=check)
        except :
            return Response({
                "Status":"Failure"
            })
        
        likeddog=Liked_Dog.objects.filter(liked_user_id=user)
        print(likeddog)
        file_serializer = Liked_DogSerializer(likeddog, many=True)
        
        if likeddog is not None:
            return Response(file_serializer.data)
        else:
            return Response({
                "Status":"No Data Found."
            })
            
# SHARE FEED API
class Sharefeed(APIView):
 
    def post(self,request, *args, **kwargs):
        try:
            dogid=self.request.data["dogid"]
            dogsid=Dog.objects.get(id=dogid)
            descript=self.request.data['desc']
            userid=self.request.data["userid"]
            users=User.objects.get(id=userid)
        except :
            return Response({
                "Status":"Failure"
            })

        Feed_Item.objects.create(Feed_user=users, feed_item_dog=dogsid, feed_item_desc=descript, isSaveFeed = False)
        
        if dogsid and users is not None:
            return Response({
                "Status":"Success"
            })
        else:
            return Response({
                "Status":"Failure"
            })

# FORGET PASSWORD API
class Forgetpass(APIView):
    def post(self, request, format = json):
        print("In Login View")
        email = request.data.get("email")
        resetkey = request.data.get("resetkey").lower()
        serializer_class = UserSerializer
        
        if email and resetkey:
            users = User.objects.filter(email = email , resetkey = resetkey)
            if users:
                user = User.objects.get(email = email , resetkey = resetkey)
                print(user.id)
                return Response({
                     "Status": "Success",
                     "userid":user.id 
                })
            else:
                return Response({
                    "Status" : "Faliure",
                    "userid": None 
                })
class changePassword(APIView):
    def post(self, request, format = json):
        print("In Login View")
        userid = request.data.get("userid")
        password = request.data.get("password")
        serializer_class = UserSerializer
        
        if userid and password is not None:
            user = User.objects.filter(id = userid)
            if user:
                # user = User.objects.get(id = userid)
                # print(user.id)
                user.update(password = password )
                return Response({
                     "Status": "Success",
                    #  "userid":user.id 
                })
            else:
                return Response({
                    "Status" : "Faliure",
                    # "userid": None 
                })

# UPDATE USER DETAILS API
class updateview(APIView):
    
    def post(self, request, format = json):
        print("In Login View")
        userid = request.data.get("userid")
        # email = request.data.get("email")
        fullname = request.data.get("fullname")
        # password = request.data.get("password")
        city= request.data.get("city")
        country = request.data.get("country")
        
        serializer_class = UserSerializer
        print(fullname)
        if userid is not None:
            user = User.objects.filter(id = userid)
            try:
                passuser = User.objects.get(id = userid)
            except :
                fnl_JSON = {
                "id": None,
                "password": None,
                "email": None,
                "resetkey": None,
                "full_name": None,
                "city": None,
                "country": None,
                "last_login": "",
                "active": False,
                "staff": False,
                "admin": False,
                }
                return Response({
                        "Status" : "Failure",
                        "user" : fnl_JSON
                })
            
            if user:
                # user = User.objects.get(id = userid)
                # print(user.id)
                # user.update(email = email )
                
                # user.update(password = password )
                
                fulln = ""
                temp_city = ""
                temp_country = ""

                if fullname != "":
                    user.update(full_name = fullname )
                    fulln = fullname
                else:
                    fulln = passuser.full_name
                if city != "":
                    user.update(city = city )
                    temp_city = city
                else:
                    temp_city = passuser.city
                
                if country != "":
                    user.update(country = country )
                    temp_country = country
                else:
                    temp_country = passuser.country

                fnl_JSON = {
                "id": passuser.id,
                "password": passuser.password,
                "email": passuser.email,
                "resetkey": passuser.resetkey,
                "full_name": fulln,
                "city": temp_city,
                "country": temp_country,
                "last_login": "",
                "active": passuser.active,
                "staff": passuser.staff,
                "admin": passuser.admin,
                }
                return Response({
                    "Status" : "Success",
                     "user": fnl_JSON 
                })
            else:
                  fnl_JSON = {
                "id": None,
                "password": None,
                "email": None,
                "resetkey": None,
                "full_name": None,
                "city": None,
                "country": None,
                "last_login": "",
                "active": False,
                "staff": False,
                "admin": False,
                }
            return Response({
                    "Status" : "Failure",
                    "user" : fnl_JSON
            })
        

#  PREDICT DOG API
class Predict(APIView):
    
    # def post(self,request, *args, **kwargs):
    #     bname=self.request.data["breed_name"]
    #     if bname is not None:
    #         breed=Breed.objects.filter(breed_name=bname)
    #         check=Dog.objects.get(dog_image=img)
    #         if breed is not None:
    #             file_serializer=BreedSerializer(breed, many=True)
    #             return Response(file_serializer.data)
    #     else:
    #         return Response({"detail":"Data not available"})
    
    def post(self,request, *args, **kwargs):
        
        #imageid=request.data.get("id")
        #img=Image.objects.get(id=imageid)
        #check=Dog.objects.get(dog_image=img)
        userid=self.request.data["userid"]
        url=self.request.data["media_url"]
        
        try:
            users=User.objects.get(id=userid)
        except:
            return Response({
                    "Status" : "Failure",
                    "Dog" : None
            })

        print(users)

        # sm = boto3.Session().client(service_name="sagemaker-runtime",region_name=settings.AWS_REGION,aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        #        aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY)

        # payload = {"url" : url}

        # response = sm.invoke_endpoint(
        #   EndpointName=settings.AWS_SAGEMAKER_ENDPOINT_NAME,
        #    Body= json.dumps(payload).encode("utf-8"),
        #    ContentType="application/json",
        #     Accept="application/json",
        #     CustomAttributes=""
        # )
        
        # res = response["Body"].read()

        # # For Decoding it back to JSON
        # output = json.loads(res.decode("utf-8"))

        # print(output)



        output = {
                
            "dogId": "96",
            "accuracy": "87.2",
            "Remarks": "The Given Image of Dog is a/an n02109047-Great_Dane",
            "isDog": True,
            "breed_Name": "n02109047-Great_Dane"
         }

        if output["isDog"] == False:
                return Response({
                    "Status" : "The given image is not a dog or has so much Image Noise.",
                    "Dog" : None
            })

        Dog_qs = Dog.objects.filter(dog_user=users, dog_image=url)

        print(Dog_qs)

        if len(Dog_qs) != 0:
            Dog.objects.filter(dog_user=users, dog_image=url).delete()
            print("DELETED")
        else:
            print("NOT DELETED")
        if url and userid and users is not None:
            print(output["dogId"])

            breed=Breed.objects.filter(id=output["dogId"])

            if len(breed) != 0:
                breedObj=Breed.objects.get(id=output["dogId"])
                Dog.objects.create(dog_acc=output["accuracy"], dog_user=users, dog_image=url, dog_breed = breedObj, Remarks = output["Remarks"], isDog = output["isDog"])

                dogObj = Dog.objects.get(dog_acc=output["accuracy"], dog_user=users, dog_image=url, dog_breed = breedObj, Remarks = output["Remarks"], isDog = output["isDog"])

                file_serializer = DogSerializer(dogObj, many=False)

            print(dogObj)
            print(breedObj)

            print(breed)

            if output["isDog"] == False:
                return Response({
                    "Status" : "Failure",
                    "Dog" : None
            })
            else:
                return Response({
                    "Status" : "Success",
                    "Dog" : file_serializer.data
            })
                
        # fnl_JSON = {
        #    "dogId": "95",
        #    "accuracy": "87.2",
        #    "Remarks": "The Given Image of Dog is a/an n02109047-Great_Dane",
        #     "isDog": True,
        #     "breed_Name": "n02109047-Great_Dane"
        #   }

        #   convert into JSON:
        # output = json.dumps(fnl_JSON)
        #   the result is a JSON string:
        # print(output)

#                                                                               ----------: END OF APIS :----------
