from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Member

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        models = Member
        fields = UserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Member
        fields = UserChangeForm.Meta.fields