from django.shortcuts import render
from django.views.generic.base import TemplateView

# Create your views here.

class IndexView(TemplateView): # 제네릭의 TemplateView는 아무기능 없이 템플릿만 표시해 주는 뷰에서 사용
    template_name = 'kilogram/index.html'