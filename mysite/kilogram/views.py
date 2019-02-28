from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm # 장고의 기본적인 회원가입 폼. id, password만 확인한다는 한계점.
from django.core.urlresolvers import reverse_lazy
from .forms import CreateUserForm, UploadForm
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.views.generic.detail import DetailView
from django.views import View
from .forms import UserForm, ProfileForm
# Create your views here.

@login_required   # 메소드에만 적용가능
def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES) # 대용량인 이미지를 처리해야 하므로 두 매개변수를 넘겨줘야함.
        if form.is_valid():
            photo = form.save(commit=False) # photo객체를 가져오긴 하나 DB에 아직 저장하진 않음
            photo.owner = request.user      # request.user는 로그인한 사용자
            form.save()
            return redirect('kilogram:index')


    form = UploadForm()
    return render(request, 'kilogram/upload.html', {'form' : form})


class IndexView(ListView):
    # model = Photo 이렇게 해주면 사용자를 안가리고 모든 photo객체가 넘어가게 되므로 아래와 같이 쿼리를 지정해줌.
    context_object_name = 'user_photo_list' # 템플릿에 전달되는 이름
    paginate_by = 2 # 사진을 몇개씩 보여줄 것인지 지정.

    def get_queryset(self):
        user = self.request.user    # 로그인되어있는 사용자
        return user.photo_set.all().order_by('-pub_date')


'''
class CreateUserView(CreateView):  # 제네릭의 CreateView는 폼하고 연결돼서, 혹은 모델하고 연결돼서 새로운 데이터를 넣을 때 사용.
    template_name = 'registration/signup.html'     # 회원가입 할 때 띄울 폼 템플릿
    #form_class = UserCreationForm # id, pw만 받는 폼 클래스
    form_class = CreateUserForm    # id, email, pw 까지 받는 사용자 정의 폼 클래스
    success_url = reverse_lazy('create_user_done') # 성공하면 어디로 갈지, create_user_done은 url name
    # 여기서 reverse가 아닌 reverse_lazy를 사용하는 이유: 제네릭뷰 같은경우 타이밍 문제 때문에 reverse_lazy를 사용해야함


class RegisteredView(TemplateView): # 회원가입이 완료된 경우
    template_name = 'registration/signup_done.html'
'''


class ProfileView(DetailView):
    context_object_name = 'profile_user' # model로 지정해준 User모델에 대한 객체와 로그인한 사용자랑 명칭이 겹쳐버리기 때문에 이를 지정해줌.
    model = User
    template_name = 'kilogram/profile.html'


class ProfileUpdateView(View): # 간단한 View클래스를 상속 받았으므로 get함수와 post함수를 각각 만들어줘야한다.
    # 프로필 편집에서 보여주기위한 get 메소드
    def get(self, request):
        user = get_object_or_404(User, pk=request.user.pk)  # 로그인중인 사용자 객체를 얻어옴
        user_form = UserForm(initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
        })

        if hasattr(user, 'profile'):  # user가 profile을 가지고 있으면 True, 없으면 False (회원가입을 한다고 profile을 가지고 있진 않으므로)
            profile = user.profile
            profile_form = ProfileForm(initial={
                'nickname': profile.nickname,
                'profile_photo': profile.profile_photo,
            })
        else:
            profile_form = ProfileForm()

        return render(request, 'kilogram/profile_update.html', {"user_form": user_form, "profile_form": profile_form})

    # 프로필 편집에서 실제 수정(저장) 버튼을 눌렀을 때 넘겨받은 데이터를 저장하는 post 메소드
    def post(self, request):
        u = User.objects.get(id=request.user.pk)        # 로그인중인 사용자 객체를 얻어옴
        user_form = UserForm(request.POST, instance=u)  # 기존의 것의 업데이트하는 것 이므로 기존의 인스턴스를 넘겨줘야한다. 기존의 것을 가져와 수정하는 것

        # User 폼
        if user_form.is_valid():
            user_form.save()

        if hasattr(u, 'profile'):
            profile = u.profile
            profile_form = ProfileForm(request.POST, request.FILES, instance=profile) # 기존의 것 가져와 수정하는 것
        else:
            profile_form = ProfileForm(request.POST, request.FILES) # 새로 만드는 것

        # Profile 폼
        if profile_form.is_valid():
            profile = profile_form.save(commit=False) # 기존의 것을 가져와 수정하는 경우가 아닌 새로 만든 경우 user를 지정해줘야 하므로
            profile.user = u
            profile.save()

        return redirect('kilogram:profile', pk=request.user.pk) # 수정된 화면 보여주기