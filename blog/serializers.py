from django.contrib.auth.models import User

from rest_framework import serializers

from blog.models import Profile,Post,Comment

from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    
    profile=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        
        model=User
        
        fields=["id","username","email","password","profile"]
        
    def get_profile(self,obj):
        
        profile_instance=Profile.objects.get(owner=obj)
        
        serializer_instance=ProfileSerializer(profile_instance,many=False)
        
        return serializer_instance.data
        
    def create(self,validated_data):
        
        return User.objects.create_user(**validated_data)
    
class ProfileSerializer(serializers.ModelSerializer):
    
    owner=serializers.StringRelatedField(read_only=True)
    
    class Meta:
        
        model=Profile
        
        fields="__all__"
        
        read_only_fields=['id','owner']
    
class CommentSerializer(serializers.ModelSerializer):
    
    owner=serializers.StringRelatedField(read_only=True)
    
    post_object=serializers.StringRelatedField(read_only=True)
    
    class Meta:
        
        model=Comment
        
        fields="__all__"
        
        read_only_fileds=['id','owner','post_object','created_at','updated_at']
        

    

class PostSerializer(serializers.ModelSerializer):
    
    owner=serializers.StringRelatedField(read_only=True)
    
    # comments=serializers.SerializerMethodField(read_only=True)
    
    comments=CommentSerializer(read_only=True,many=True)
    
    comment_count=serializers.CharField(read_only=True)
    
    # comment_count=serializers.SerializerMethodField(read_only=True)
    
    like_count=serializers.SerializerMethodField(read_only=True)
    
    liked_by=serializers.StringRelatedField(read_only=True,many=True)
    
    is_liked=serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        
        model=Post
        
        fields="__all__"
        
        read_only_fields=['id','owner','created_at','updated_at']
        
    def get_comments(self,obj):
        
        comment_object=Comment.objects.filter(post_object=obj)
        
        # comment_object=obj.post_comments.all()
        
        serializer_instance=CommentSerializer(comment_object,many=True)
        
        return serializer_instance.data
    
    def get_comment_count(self,obj):
        
        comment_count=obj.post_comments.all().count()
        
        return comment_count
    
    def get_like_count(self,obj):
        
        like_count=obj.liked_by.all().count()
        
        return like_count
    
    def get_is_liked(self,obj):
        
        liked_users=obj.liked_by.all()
        
        user=self.context.get('user')
        
        return user in liked_users
        
