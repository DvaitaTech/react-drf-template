from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    This allows us to add custom fields while maintaining all built-in user functionality.
    """
    # Add custom fields here
    phone_number = models.CharField(
        _('phone number'),
        max_length=15,
        blank=True,
        help_text=_('User\'s phone number')
    )
    date_of_birth = models.DateField(
        _('date of birth'),
        null=True,
        blank=True,
        help_text=_('User\'s date of birth')
    )
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pictures/',
        null=True,
        blank=True,
        help_text=_('User\'s profile picture')
    )
    bio = models.TextField(
        _('bio'),
        max_length=500,
        blank=True,
        help_text=_('User\'s biography')
    )
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Whether the user has verified their email')
    )
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        help_text=_('When the user was created')
    )
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
        help_text=_('When the user was last updated')
    )

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']

    def __str__(self):
        return self.email or self.username

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Return the short name for the user.
        """
        return self.first_name
