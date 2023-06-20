import random
import cv2,os
from face_rec import FaceRecognition
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import User
from  visual_cryptography import captchageneration,share_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import globals
from .models import Captcha
from django.contrib.auth import authenticate

def home(request):
    return render(request, 'website/index.html',)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            captcha_array=[]
            os.mkdir(f"static/media/shares/{username}")
            captchageneration.generate_captcha(username,captcha_array)
            client_share=share_generator.split_image(image_path=f"static/media/captcha/{username}.png",k=2,n=2,output_dir=f"static/media/shares/{username}",username=username)
            for i in range(3,10):
             captchageneration.generate_captcha(username,captcha_array)
             share_generator.split_image_new(image_path=f"static/media/captcha/{username}.png",k=2,n=2,output_dir=f"static/media/shares/{username}",username=username,client_share=client_share,num=i)
            share_url=f"/media/shares/{username}/" + username + "_share_1.png"
            #captcha_url="/media/captcha/" + username + ".png"
            form.save()
            user = User.objects.get(username=username)
            captcha_form=Captcha()
            setattr(captcha_form,'username',user)
            setattr(captcha_form,'uname',username)
            for i in range(0,8):
                setattr(captcha_form,f'captcha_{i+1}',captcha_array[i])
            captcha_form.save()
            return render(request,"website/captcha_and_share.html",{'share':share_url,'message1':"This is your share",'message2':"(Download it and print it on a physical transparency)"})
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'website/login.html',)
    elif request.method == 'POST':
        username = request.POST.get('username')
        user = authenticate(request, username = username)
        globals.globaluser=username
    
        userdata = User.objects.filter(username = username).values()
        global frame
        directory=os.getcwd()
        def capture_frame(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                os.path.join(directory,"captured_images")
                cv2.imwrite(username+".jpg", frame)

        if(User.objects.filter(username=username).exists()):
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
            faceRecognition = FaceRecognition()
            originalImagePath = str(userdata[0]['image'])
            result = faceRecognition.classify_face(os.path.join(directory,f"{username}.jpg"),os.path.join(directory,f"{originalImagePath}"))  
            if result == 0 or result==None:
                messages.error(request,'Face recognition failed!Please try again.')
                return redirect('login')
            else:
                random_index = random.randint(2,9)
                globals.random_index=random_index
                url=f"/media/shares/{username}/" + username + f"_share_{random_index+1}.png"
                return render(request,"website/captcha_check.html",{'img_url':url})
        else:
            messages.error(request,'Invalid Username!Please try again.')
            return redirect('login')
    return render(request, 'website/login.html',)

def checkcaptcha(request):
    if request.method == 'POST':
        captcha_text=request.POST.get('ctext')
        username=globals.globaluser
        sample_instance = Captcha.objects.get(username=username)
        print(sample_instance)
        if(globals.random_index==1):
           value = sample_instance.captcha_1
        elif(globals.random_index==2):
           value = sample_instance.captcha_2
        elif(globals.random_index==3):
           value = sample_instance.captcha_3
        elif(globals.random_index==4):
           value = sample_instance.captcha_4
        elif(globals.random_index==5):
           value = sample_instance.captcha_5
        elif(globals.random_index==6):
           value = sample_instance.captcha_6
        elif(globals.random_index==7):
           value = sample_instance.captcha_7
        elif(globals.random_index==8):
           value = sample_instance.captcha_8
        if(captcha_text==value):
            print("success")
        else:
            messages.error(request,'Incorrect Captcha!Please try again.')
            return redirect('login')
        return render(request, 'website/success.html',)


