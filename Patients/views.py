from rest_framework.response import Response
from Patients.models import Patient
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.views import APIView
from Patients.serializers import( PatientRegistrationSerializer,PatientLoginSerializer,PatientSerializer,
                                 OtpForResetPassword,Verifyotpserializers,PasswordResetSerializers,PatientSerializer,ResendOtpserializer)
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from Patients.renderers import PatientRenderer
from Patients.mytokens import get_tokens_for_user
from django.utils.decorators import method_decorator  
from django.contrib.auth.decorators import login_required
from Patients.utils import Utils
from Patients.emails import send_otp_via_mail
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import authentication_classes
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
#Register User Information
class PatientRegistrationView(APIView):
    renderer_classes=[PatientRenderer]
    def post(self,request,format=None):
        serializer=PatientRegistrationSerializer(data=request.data)
    
        if serializer.is_valid(raise_exception=True):
            
            user=serializer.save()
            token=get_tokens_for_user(user)

            email=serializer.data['email']
            send_otp_via_mail(email)
            # token=get_tokens_for_user(patient)
            return Response({f'messages':'OTP has been send to your mail. You need to enter the otp for verfing the email.','msg':'Success'},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,{'msg':'Error'},status=status.HTTP_400_BAD_REQUEST)

class PatientLoginView(APIView):
    renderer_classes=[PatientRenderer]
    def post(self,request,format=None):
        serializer=PatientLoginSerializer(data=request.data)
        print("hihnihih")
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get('email')
            password=serializer.data.get('password')
          
            user=Patient.objects.get(email=email)
            
            if user is not None and check_password(password,user.password):
                
                serializer=PatientSerializer(user)
                token=get_tokens_for_user(user)
                print('token:',token)
                return Response({'token':token,'msg':'Success','messages':f'You Have Successfully {email} Logined Into Your Account','user_detail':serializer.data},                                           
                            status=status.HTTP_201_CREATED ,)
                
            else:
                return Response({'message':'Check if your','error':{'non_field_errors':['Email or Password is Not Valid']},'msg':'Error'},status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors,{'msg':'Error'},status.HTTP_400_BAD_REQUEST)
    

    
class VerifyotpView(APIView):
    def post(self,request):
        try:
            serializer=Verifyotpserializers(data=request.data)
            if serializer.is_valid():
                email=serializer.data['email']
                otp=serializer.data['otp']
                user=Patient.objects.filter(email=email)
                print(email)
                print(user[0].otp)
                if user[0].otp==None:
                    send_otp_via_mail(user[0].email)
                if not user.exists():
                    return  Response({'message':'The email is not exists','msg':'Error'},status=status.HTTP_401_UNAUTHORIZED)
                
                if not user[0].otp==otp:
                    return  Response({'message':'The otp is not matched','msg':'Error'},status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                
                # print(user.is_verified)
                user=user.first()
                user.is_verified = True
                user.otp = None 
                user.save()
                
                return Response({'message':'Your account has been Verified','msg':'Success'},status=status.HTTP_201_CREATED)
            return Response({'msg':'Error'},serializer.errors,status=status.HTTP_400_BAD_REQUEST)   
        except Exception as e:
            print(e)
            

class OtpResetPasswordView(APIView):
       renderer_classes=[PatientRenderer]
       def post(self,request):
           serializer=OtpForResetPassword(data=request.data)
           if serializer.is_valid():
                        
                         return Response({'message':'Otp sent successfully','msg':'Success'},status=status.HTTP_201_CREATED)
           return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
               


class PasswordResetView(APIView):
     def post(self,request):
         serializer=PasswordResetSerializers(data=request.data)
         if serializer.is_valid():
             print("yes")
             return Response({'message':"You Have Successfully Reset Your New Password!",'msg':'Success'},status=status.HTTP_201_CREATED)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
     
class PatientView(APIView):
    authentication_classes=[JWTTokenUserAuthentication]
    renderer_classes=[PatientRenderer]
    permission_classes=[IsAuthenticated]   
     
    def get(self,request,format=None):
        user=request.user
        print('user.id',user.id)
        if user:
            id=user.id
            print(user)
            serializer=PatientSerializer(user)
        
            patient=Patient.objects.get(id=id)
            # print(patient.username)
            return Response({'user_detail':{
                    'username':patient.username,
                    'email':patient.email,
                    'first_name':patient.first_name,
                    'last_name':patient.last_name,
                    'gender':patient.gender   
                }
                ,'msg':'Success'              
                                
                                
                                },   status=status.HTTP_201_CREATED)
        return Response({'msg':'Error'},status=status.HTTP_400_BAD_REQUEST)
        

    
    
class PatientUpdateView(APIView):
    authentication_classes=[JWTTokenUserAuthentication]
    renderer_classes=[PatientRenderer]
    permission_classes=[IsAuthenticated] 
    def post(self,request,pk):
        try:
            id=pk
            patient =Patient.objects.get(id=id)
            serializer = PatientSerializer(patient, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'msg':'Success','messages':'Successfully Updated'},status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Patient.DoesNotExist:
            print("this is except block")
            return Response({'msg':'Error'},status=status.HTTP_400_BAD_REQUEST)
        
class ResendOtpView(APIView):
        def post(self,request,format=None):
           serializer=ResendOtpserializer(data=request.data)
           if  serializer.is_valid(raise_exception=True):               
                  return Response({'msg':'Success','messages':'Otp has been sent please check your mail!.'},status=status.HTTP_201_CREATED)
           return Response({'msg':'Error','message':'otp has not sent  been resent'},status=status.HTTP_400_BAD_REQUEST)