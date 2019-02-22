from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm # 장고의 기본적인 회원가입 폼. id, password만 확인한다는 한계점.
from django.core.urlresolvers import reverse_lazy
from .forms import CreateUserForm
# Create your views here.

class IndexView(TemplateView):     # 제네릭의 TemplateView는 아무기능 없이 템플릿만 표시해 주는 뷰에서 사용
    template_name = 'kilogram/index.html'

class CreateUserView(CreateView):  # 제네릭의 CreateView는 폼하고 연결돼서, 혹은 모델하고 연결돼서 새로운 데이터를 넣을 때 사용.
    template_name = 'registration/signup.html'     # 회원가입 할 때 띄울 폼 템플릿
    #form_class = UserCreationForm # id, pw만 받는 폼 클래스
    form_class = CreateUserForm    # id, email, pw 까지 받는 사용자 정의 폼 클래스
    success_url = reverse_lazy('create_user_done') # 성공하면 어디로 갈지, create_user_done은 url name
    # 여기서 reverse가 아닌 reverse_lazy를 사용하는 이유: 제네릭뷰 같은경우 타이밍 문제 때문에 reverse_lazy를 사용해야함

class RegisteredView(TemplateView): # 회원가입이 완료된 경우
    template_name = 'registration/signup_done.html'