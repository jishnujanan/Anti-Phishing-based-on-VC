import cv2,os
from face_rec import FaceRecognition
from django.shortcuts import render
from .forms import RegistrationForm
from .models import User
from  visual_cryptography import captchageneration,share_generator

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
            return render(request,"website/captcha_and_share.html",{'share':share_url})
    else:
        form = RegistrationForm()
    return render(request, 'website/register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'website/login.html',)
    elif request.method == 'POST':
        username = request.POST.get('username')
        userdata = User.objects.filter(username = username).values()
        print(userdata[0]['image'])
        global frame
        def capture_frame(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                directory = r'D:\ANTI PHISHING\Anti-Phishing-based-on-VC\captured_images'
                os.chdir(directory)
                cv2.imwrite(username+".jpg", frame)
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
            #FaceRecognition.classify_face(username+".jpg")
            
        else:
            print("Username not Exists")
    return render(request, 'website/login.html',)

