from django.shortcuts import render , redirect
from .forms import RegistrationForm
from  visualcryptography import captchageneration,share_generator
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            path = captchageneration.generate_captcha(username=username)
            share_generator.split_image(image_path=f"media/captcha/{username}.png",k=2,n=2,output_dir="media/shares/",username=username)
            return render(request,"users/captcha_and_share.html",{'filename':username})
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request,'users/profile.html')