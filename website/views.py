from django.shortcuts import render
from .forms import RegistrationForm
from  visual_cryptography import captchageneration,share_generator

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            path = captchageneration.generate_captcha(username=username)
            share_generator.split_image(image_path=f"static/media/captcha/{username}.png",k=2,n=2,output_dir="static/media/shares/",username=username)
            share_url="/media/shares/" + username + "_share_1.png"
            captcha_url="/media/captcha/" + username + ".png"
            return render(request,"website/captcha_and_share.html",{'share':share_url,'captcha':captcha_url})
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form': form})

def profile(request):
    return render(request,'website/profile.html')
