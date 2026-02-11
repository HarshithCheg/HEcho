from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Server, ServerMember, ServerInvite


# imp note: views handle http request while signals reacts to DB events.
# kind of like an automatic thing, also need to register signals.py in apps.py
@receiver(post_save, sender=Server)
def owner_as_member(sender, instance, created, **kwargs):
    """ Auto Adds Owner to the server. when a change occurs to database like a 
    a new server created by user, it makes the creator to join as a member to
    the server. """
    if created:
        ServerMember.objects.create(user = instance.owner, server=instance, roles='owner')

@receiver(post_save, sender=Server)
def create_invite(sender, instance, created, **kwargs):
    if created:
        ServerInvite.objects.create(server=instance)