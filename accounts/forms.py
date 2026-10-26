from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from django.utils import timezone

from .levels import LEVEL_NAMES
from .models import Levels, Users
from .validators import email_error, username_error, validate_password_strength


class RegistrationForm(UserCreationForm):
    fishing_level = forms.ChoiceField(
        label="Рівень риболовлі",
        choices=[("", "Оберіть рівень риболовлі"), *LEVEL_NAMES.items()],
    )

    error_messages = {
        **UserCreationForm.error_messages,
        "password_mismatch": "Паролі не збігаються.",
    }

    class Meta(UserCreationForm.Meta):
        model = Users
        fields = ("username", "email")

    def __init__(self, *args, **kwargs):
        self.existing_google_user = kwargs.pop("existing_google_user", None)
        if self.existing_google_user is not None:
            kwargs["instance"] = self.existing_google_user
        # The existing profile model is not Django's AbstractUser and does
        # not define USERNAME_FIELD, so initialize its ModelForm directly.
        ModelForm.__init__(self, *args, **kwargs)
        self.fields["username"].label = "Логін"
        self.fields["email"].label = "Email адреса"
        self.fields["password1"].label = "Пароль"
        self.fields["password1"].help_text = ""
        self.fields["password2"].label = "Підтвердження пароля"
        self.fields["password2"].help_text = ""

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        exclude_user_id = self.existing_google_user.user_id if self.existing_google_user else None
        message = username_error(username, exclude_user_id=exclude_user_id)
        if message:
            raise forms.ValidationError(message)
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if self.existing_google_user and email != self.existing_google_user.email.lower():
            raise forms.ValidationError("Вкажіть email, підтверджений через Google.")
        exclude_user_id = self.existing_google_user.user_id if self.existing_google_user else None
        message = email_error(email, exclude_user_id=exclude_user_id)
        if message:
            raise forms.ValidationError(message)
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password1")
        if password:
            try:
                validate_password_strength(
                    password,
                    cleaned_data.get("username", ""),
                    cleaned_data.get("email", ""),
                )
            except forms.ValidationError as error:
                self.add_error("password1", error)
        return cleaned_data

    def validate_password_for_user(self, user, password_field_name="password2"):
        # Keep the project's existing Ukrainian password rules as the source
        # of truth rather than adding a second, different Django policy.
        return None

    def save(self, commit=True):
        user = self.existing_google_user or ModelForm.save(self, commit=False)
        if self.existing_google_user:
            user.username = self.cleaned_data["username"].strip()
            user.email = self.cleaned_data["email"].strip().lower()
        level_name = LEVEL_NAMES[self.cleaned_data["fishing_level"]]
        user.level, _ = Levels.objects.get_or_create(name=level_name)
        user.password_hash = make_password(self.cleaned_data["password1"])
        user.created_at = timezone.now()
        if commit:
            user.save()
        return user
