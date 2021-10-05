from django.db.models.signals import pre_save 
from django.contrib.auth.models import User 

#This function uses django signals it gets fired off every time a model is saved
def updateUser(sender, instance, **kwargs):
    user = instance
    if user.email != '' :
        user.username = user.email      #This makes the data stored in the username field the same as the data stored in the email field
        
#The above solution is a quick fix their are other ways of doing this like overriding the user model

pre_save.connect(updateUser, sender=User) #This sends the signal