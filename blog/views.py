from django.shortcuts import render,get_object_or_404

from rest_framework.generics import CreateAPIView,UpdateAPIView,RetrieveAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView

from blog.serializers import UserSerializer,ProfileSerializer,PostSerializer,CommentSerializer

from rest_framework.views import APIView

from rest_framework import authentication,permissions

from blog.models import Profile,Post

from django.contrib.auth.models import User

from rest_framework.response import Response

# Create your views here.

class UserCreateView(CreateAPIView):
    
    serializer_class=UserSerializer
    
class ProfileUpdateView(UpdateAPIView,RetrieveAPIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=ProfileSerializer
    
    def get_object(self):
        
        profile_instance=Profile.objects.get(owner=self.request.user)
        
        return profile_instance
    
class UserDetailView(RetrieveAPIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    serializer_class=UserSerializer
    
    def get_object(self):
        
        user_instance=User.objects.get(username=self.request.user.username)
        
        return user_instance
    
class PostListCreateView(ListCreateAPIView):
    
    queryset=Post.objects.all()
    
    serializer_class=PostSerializer
   
    authentication_classes=[authentication.TokenAuthentication]
   
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self,serializer):
        
        serializer.save(owner=self.request.user)
        
    def get_serializer_context(self):
        
        context=super().get_serializer_context()
        
        context['user']=self.request.user
        
        return context
        
class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    
    serializer_class=PostSerializer
    
    queryset=Post.objects.all()
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def get_serializer_context(self):
        
        context=super().get_serializer_context()
        
        context['user']=self.request.user
        
        return context
        
    
class CommentCreateView(CreateAPIView):
    
    serializer_class=CommentSerializer
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        
        id=self.kwargs.get('pk')
        
        post_instance=get_object_or_404(Post,id=id)
        
        serializer.save(owner=self.request.user,post_object=post_instance)
        
class PostLikeView(APIView):
    
    authentication_classes=[authentication.TokenAuthentication]
    
    permission_classes=[permissions.IsAuthenticated]
    
    def post(self,request,*args,**kwargs):
        
        id=kwargs.get('pk')
        
        post_object=get_object_or_404(Post,id=id)
        
        if request.user in post_object.liked_by.all():
            
            post_object.liked_by.remove(request.user)
            
            return Response(data={'message':'like removed'})
            
        else:
        
            post_object.liked_by.add(request.user)
        
            return Response(data={'message':'liked'})
    
