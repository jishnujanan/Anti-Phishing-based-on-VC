import random
import cv2,os
from PIL import Image
import numpy as np
from face_rec import FaceRecognition
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import User
from  visual_cryptography import captchageneration,share_generator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . import globals
from django.core.files.storage import FileSystemStorage


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
            return render(request,"website/captcha_and_share.html",{'share':share_url,'message1':"This is your share",'message2':"(Download it and print it on a physical transparency)"})
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'website/login.html',)
    elif request.method == 'POST':
        username = request.POST.get('username')
        globals.globaluser=username
        userdata = User.objects.filter(username = username).values()
        global frame
        def capture_frame(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                directory = r'D:\ANTI PHISHING\Anti-Phishing-based-on-VC\captured_images'
                os.chdir(directory)
                cv2.imwrite(username+".jpg", frame)

        directory = r'D:\ANTI PHISHING\Anti-Phishing-based-on-VC'
        os.chdir(directory)      
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
            originalImagePath = originalImagePath.replace("/","\\")
            result = faceRecognition.classify_face(os.path.join(directory,f"captured_images\{username}.jpg"),os.path.join(directory,f"{originalImagePath}"))  
            print(result)
            if result == 0 or result==None:
                messages.error(request,'Face recognition failed!Please try again.')
                return redirect('login')
            else:
                directory = r'D:\ANTI PHISHING\Anti-Phishing-based-on-VC'
                os.chdir(directory)  
                return render(request,"website\captcha_check.html")
        else:
            messages.error(request,'Invalid Username!Please try again.')
            return redirect('login')
    return render(request, 'website/login.html',)

def checkcaptcha(request):
    if request.method == 'POST':
        share = request.FILES['uploadFromPC']
        fs = FileSystemStorage(location='path/to/save')
        file_name = fs.save(share.name, share)
        file_path = fs.path(file_name)
        directory = r'D:\ANTI PHISHING\Anti-Phishing-based-on-VC'
        os.chdir(directory) 
        random_number = random.randint(2,9)
        print(f"globaluser={globals.globaluser}")
        share_url=f"static/media/shares/{globals.globaluser}/" + globals.globaluser + f"_share_{random_number}.png"
        output_image = share_generator.recombine_shares(share_url,file_path)
        recombined_image = Image.fromarray(output_image)
        share_path = os.path.join("static/", "display.png")
        recombined_image.save(share_path)
        share_path = os.path.join("", "display.png")
        return render(request,"website/captcha_and_share.html",{'share':share_path,'message1':"This is your captcha",'message2':''})

