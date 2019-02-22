from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CreateUserForm(UserCreationForm): # id, pw만 입력받은 UserCreationForm을 확장시킬것이므로 상속받음
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2") # 입력받을 필드순서 지정

    def save(self, commit=True):  # save메소드 오버라이
        user = super(CreateUserForm, self).save(commit=False) # 기존의 id와 pw를 저장. commit이 Flase인 이유는 2번 저장하는것 방지.
        user.email = self.cleaned_data["email"]               # user 객체에 email 값 추가.
        if commit:
            user.save()              # 객체에 대한 모든 정보를 DB에 저장.
        return user