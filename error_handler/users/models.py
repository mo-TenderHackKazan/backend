from django.contrib.auth.models import AbstractUser
from django.db.models import BooleanField


class User(AbstractUser):
    """
    Default custom user model for Tender Error Handler.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    #: First and last name do not cover name patterns around the globe
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    is_site_admin = BooleanField(default=False)
