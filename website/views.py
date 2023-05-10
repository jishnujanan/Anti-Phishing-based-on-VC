import cv2

from django.shortcuts import render
from .forms import RegistrationForm
from .models import User
from  visual_cryptography import captchageneration,share_generator

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            path = captchageneration.generate_captcha(username=username)
            share_generator.split_image(image_path=f"static/media/captcha/{username}.png",k=2,n=2,output_dir="static/media/shares/",username=username)
            share_url="/media/shares/" + username + "_share_1.png"
            captcha_url="/media/captcha/" + username + ".png"
            form.save()
            return render(request,"website/captcha_and_share.html",{'share':share_url,'captcha':captcha_url})
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'website/login.html',)
    elif request.method == 'POST':
        username = request.POST.get('username')
        userdata = User.objects.filter(username = username).values()
        global frame
        def capture_frame(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                cv2.imwrite(username, frame)
                print(OS)
        if(User.objects.filter(username=username).exists()):
            print("Username Exists")
            video_capture = cv2.VideoCapture(0)
            if not video_capture.isOpened():
                print("Failed to open video capture.")
                exit()
            cv2.namedWindow("Live Video")
            cv2.setMouseCallback("Live Video", capture_frame)
            while True:
                ret, frame = video_capture.read()
                if ret:
                    cv2.imshow("Live Video", frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                else:
                    print("Failed to capture frame from video.")
                    break
            video_capture.release()
            cv2.destroyAllWindows()
            
        else:
            print("Username not Exists")
    return render(request, 'website/login.html',)

