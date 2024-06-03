from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, SellerProfile

@receiver(post_save, sender=UserProfile)
def create_seller_profile(sender, instance, created, **kwargs):
    if instance.is_seller and not hasattr(instance, 'sellerprofile'):
        SellerProfile.objects.create(user_profile=instance)
    # elif not instance.is_seller and hasattr(instance, 'sellerprofile'):
        # instance.sellerprofile.delete()
