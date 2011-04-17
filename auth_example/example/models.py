from django.db import models
from django.contrib.auth.models import User
from linkedin_auth.models import LinkedInProfileModel, random_member_id

# Create your models here.

class ExampleUserProfile(LinkedInProfileModel):
    user        = models.OneToOneField(User)
    
    class Meta:
        unique_together     = ('member_id', 'user')
        verbose_name        = 'Example User Profile'
        verbose_name_plural = 'Example User Profiles'
## END UserProfile

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created:
        rand_id         = random_member_id()
        profile, new    = ExampleUserProfile.objects.get_or_create(user=instance, defaults={ 'member_id': rand_id })
## END create_profile