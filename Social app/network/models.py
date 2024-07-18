from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Content(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    post = models.CharField(max_length=150)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    def __str__ (self):
      return f" Post{self.id} by {self.user} on {self.timestamp.strftime('%d %b %Y %H:%M:%S')}"
  
class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following_someone")
    user_followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_being_followed")
    
    def __str__ (self):
      return f"{self.user} is following {self.user_followed}"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_that_is_liking") 
    post = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="content_liking")
    
    def __str__ (self):
      return f"{self.user} has liked {self.post}" 