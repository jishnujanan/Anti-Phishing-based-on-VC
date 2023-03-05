from django.shortcuts import render , redirect
from .forms import RegistrationForm
from  visualcryptography import captchageneration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            path = captchageneration.generate_captcha(username=username)
            newPath = 'finalyearproject/'+path
            return render(request,"users/captcha_and_share.html",{'path':newPath})
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request,'users/profile.html')