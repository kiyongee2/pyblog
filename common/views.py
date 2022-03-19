from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from common.forms import UserForm


def signup(request):
    # 회원 가입
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()   #db에 저장
            return redirect('aboutme:index')
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, 'common/signup.html', context)



#가입후 자동로그인
# username = form.cleaned_data.get('username')
# password = form.cleaned_data.get('password')
# user = authenticate(username=username, password=password) # 인증(세션 발급)
# login(request, user)