from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (User,Workouts,Trackings,Excercise)
from  django import forms
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
class UserCreationForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('email',)
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    add_form = UserCreationForm
    list_display = ("email",'is_active',)
    ordering = ("username",)
    

    fieldsets = (
        (None, {'fields': ('email', 'password','username','is_superuser','is_active')}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password','username','is_superuser', 'is_staff', 'is_active')}
            ),
        )

    filter_horizontal = ()

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Workouts)
admin.site.register(Trackings)
admin.site.register(Excercise)
