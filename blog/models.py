from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save

class Profile(models.Model):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="userprofile")

    adress=models.TextField(null=True)

    phone=models.CharField(max_length=15,null=True)

    GENDER_CHOICES=(
        ("male","male"),
        ("female","female")
    )

    gender=models.CharField(max_length=20,choices=GENDER_CHOICES,default="male")

    picture=models.ImageField(upload_to="profilepics",null=True,blank=True,default="profilepics/default.png")
    
    bio=models.CharField(max_length=100,null=True)
    
def create_profile(sender,instance,created,**kwargs):
    
    if created:
        
        Profile.objects.create(owner=instance)
        
post_save.connect(create_profile,User)

class Post(models.Model):

    caption=models.CharField(max_length=200)

    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="blogs")
    
    picture=models.ImageField(upload_to="postpictures",null=True,blank=True)

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)
    
    liked_by=models.ManyToManyField(User,related_name="posts")
    
    def comment_count(self):
        
        return self.post_comments.all().count()
    
    def comments(self):
        
        return self.post_comments.all()

    def __str__(self):
        
        return self.caption
    
class Comment(models.Model):

    message=models.CharField(max_length=200)

    owner=models.ForeignKey(User,on_delete=models.CASCADE)

    post_object=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="post_comments")

    created_at=models.DateTimeField(auto_now_add=True)

    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        
        return self.message
    
