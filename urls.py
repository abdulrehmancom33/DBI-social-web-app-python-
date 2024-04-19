from django.urls import path,include
from . import views
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
urlpatterns = [

    # USER ACCOUNT APIS
    path('authenticate/',views.authenticate.as_view(), name='authenticate'),
    path('register/',views.signUp.as_view(), name='signUp'),
    path('getallusers/',views.UserViewSet.as_view({'get' : 'list'})),
    path('logout/',views.LogoutView.as_view(), name='log'),
    path('forget/',views.Forgetpass.as_view(), name='for'),
    path('changepass/',views.changePassword.as_view(), name='changepass'),
    path('updateuserdetails/',views.updateview.as_view(),name='task_update'),
    
    # DOG FEED APIS
    path('breed/',views.BreedListView.as_view(), name='breed'),
    path('getdogfeeds/',views.Feed_ItemListView.as_view(), name='feed_item'),
    path('getfeeddetails/',views.Feed_Details.as_view(), name='user'),
    path('mydogfeed/',views.Mydogfeeds.as_view(), name='mydog'),
    path('likedog/',views.Likedog.as_view(), name='like'),
    path('dislikedog/',views.DislikeDog.as_view(), name='dislike'),
    path('getlikedfeeds/',views.MyLikedFeeds.as_view(), name="mylikedfeeds"),
    path('sharefeeds/',views.Sharefeed.as_view(), name='share'),
    
    # PREDICTION AND RESULT APIS
    path('predict/',views.Predict.as_view(), name='predicts'),
    path('saveresult/',views.SaveResult.as_view(), name='save'),
    
    # UPLOAD IMAGE API
    path('uploadimage/',views.UploadViewSet.as_view(), name='uploads'),

    # NON USED/ONLY FOR TESTING APIS
    # path('login/', obtain_auth_token, name='api_token_auth'),
    # path('Dogs/',views.DogListView.as_view(), name='dog'),
    # path('Dogs/',views.DogView.as_view(),name='dog'),
    # path('mydogfeeds/',views.mydogfeeds.as_view({'get' : 'list'}))
    # path('sharefeeds/',views.Sharefeeds.as_view(), name='feeds'),
    # path('getdogfeeds/',views.getdogfeeds.as_view(), name='user'),
    # path('likeddog/',views.likeddogViewSet.as_view({'get' : 'list'}))
    # path('checkbreeddetails/',views.checkdetails.as_view(),name='details'),
    # path('predict/',views.predictViewSet1.as_view(), name='predicts'),
    # path('getuserdetails/',views.UserViewSet.as_view(), name='users'),
    # path('getdogfeeds/', views.Feed_ItemView.as_view(), name='feed_item'),
    # path('images/',views.ImageListView.as_view(), name='image'),
    # path('images/', views.ImageView.as_view(), name='image'),
    # path('users/',views.UserListView.as_view(), name='user'),
    # path('users/',views.UserView.as_view(), name='user'),
    # path('editaccount/',views.ProfileUpdateAPI.as_view(), name='edit'),
]
