from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, AgentRequest

class CustomUserCreationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)
    phone_number = forms.CharField(required=False, max_length=15)
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number', 'profile_picture')

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Montserrat styling to fields
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'profile_picture')

class BecomeAgentForm(forms.ModelForm):
    class Meta:
        model = AgentRequest
        fields = ('business_name', 'business_address', 'phone_number', 'reason')
        widgets = {
            'business_address': forms.Textarea(attrs={'rows': 3}),
            'reason': forms.Textarea(attrs={'rows': 4}),
        }

class AgentSignupForm(CustomUserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields