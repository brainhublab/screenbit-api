from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest
from django.utils import timezone

from settings import local_settings
from allauth.account.models import EmailAddress
from allauth.account.utils import send_email_confirmation
from social_django.models import UserSocialAuth

from django.core.exceptions import ObjectDoesNotExist

from django.urls import reverse

from screenbit_core.images_compression import compress_image

from screenbit_core.models import Image


def get_serialized_user_cache_key(user_id):
    return 'AUTHENTICATION_SERIALIZED_USER_{}'.format(user_id)


class UserManager(BaseUserManager):
    """
    User manager
    """
    use_in_migrations = True

    def create_user(self, email, password=None):
        """
        Custom create user method
        """
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Custom create staff user method
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Custom create super user method
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Main User model
    """
    # auth fields
    username = None
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    # additional fields
    last_active = models.DateTimeField(default=timezone.now)

    bio = models.TextField(max_length=500, blank=True, null=True)
    phone = models.TextField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    def upload_to(instance, filename):
        """
        Upload path string for user image
        """
        return 'images/users/%s/%s' % (instance.id, filename)

    image = models.ImageField(upload_to=upload_to, blank=True)

    __original_image = None
    __original_email = None

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.__original_email = self.email
        self.__original_image = self.image

    def __str__(self):
        return 'User {} ({})'.format(self.first_name, self.email)

    def get_absolute_url(self):
        return reverse('user-detail', args=[str(self.id)])

    def get_online_status_cache_key(self):
        return 'ONLINE_CHANNELS_COUNT_USER_{}'.format(self.id)

    def set_online_status(self, is_online):
        key = self.get_online_status_cache_key()
        count = cache.get(key)
        difference = 1 if is_online else -1

        if count is None:
            count = 0

        new_count = count + difference

        if new_count == 0:
            cache.delete(key)
            return None

        cache.set(key, new_count)
        return new_count

    @property
    def is_online(self):
        cache_value = cache.get(self.get_online_status_cache_key())
        return cache_value

    @property
    def is_verified_email(self):
        if self.is_staff:
            return True
        return EmailAddress.objects.filter(user=self, verified=True).exists()

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        # invalidate cache
        cache.delete(get_serialized_user_cache_key(self.pk))

        if not self.id or self.image != self.__original_image:
            # image update.
            self.image = compress_image(self.image)

        if self.pk is not None and self.email != self.__original_email:
            email, email_created = EmailAddress.objects.get_or_create(
                user=self, email=self.__original_email)
            email.email = self.email
            email.primary = True
            email.verified = False
            email.save()
            # # Email handler for prodaction
            # request = HttpRequest()
            # request.META['SERVER_NAME'] = settings.local_settings.API_HOST
            # request.META['SERVER_PORT'] = 80
            # email.send_confirmation(request, signup=True)
        self.__original_email = self.email
        self.__original_image = self.image
        super(User, self).save(force_insert, force_update, *args, **kwargs)


@receiver(post_save, sender=UserSocialAuth)
def on_user_social_created(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        email, email_created = EmailAddress.objects.get_or_create(
            user=user, email=user.email)
        if email_created:
            email.primary = True
            email.verified = False
            email.save()
            # # Email handler for prodaction
            # request = HttpRequest()
            # request.META['SERVER_NAME'] = settings.local_settings.API_HOST
            # request.META['SERVER_PORT'] = 80
            # email.send_confirmation(request, signup=True)
