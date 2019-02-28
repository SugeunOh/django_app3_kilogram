from django.db import models
from django.conf import settings
# Create your models here.

def user_path(instance, filename): # instance는 Photo 클래스의 객체, filename은 업로드할 파일의 파일이름
    from random import choice   # string으로 나온 결과에서 하나의 문자열만 뽑아냄
    import string               # 무작위 문자열을 뽑아내기 위한 용도
    arr = [choice(string.ascii_letters) for _ in range(8)] # 무작위로 8글자를 뽑아줌
    pid = ''.join(arr)          # 파일 아이디생성
    extension = filename.split('.')[-1] # 파일이름으로부터 확장자명가져오기
    # ex) honux/asfqqwer.png
    return '%s/%s.%s' % (instance.owner.username, pid, extension)


class Photo(models.Model):
    image = models.ImageField(upload_to=user_path)      # upload_to로 어디에 업로드할지 지정할 수 있음.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL) # 하나의 사진은 한명의 사용자에게 속해야 하므로. 1:N의 관계
    thumbnail_image = models.ImageField(blank=True)      # blank가 True이면 폼 입력시 꼭 입력하지 않아도 된다는 의미
    comment = models.CharField(max_length=255)
    pub_date = models.DateTimeField(auto_now_add=True)  # 사용자가 입력하지 않고 업로드 하는 순간 자동으로 세팅이 됨.


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL) # 현 계정의 사용자를 가져올 수 있음.
    nickname = models.CharField(max_length=64)
    profile_photo = models.ImageField(blank=True)                 # 값을 채워넣지 않아도 되는 속성.


