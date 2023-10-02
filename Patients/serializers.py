from rest_framework import serializers
import re
from Patients.models import Patient
from rest_framework.validators import ValidationError
from Patients.emails import send_otp_via_mail,password_reset_mail
from Patients.utils import Utils
from rest_framework.validators import UniqueValidator
# Register the Patient
class PatientRegistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(style={'input_type':'password'},write_only='True')
    class Meta:
        model=Patient
        fields=['email','username','first_name','last_name','password','confirm_password','mobile_number','gender']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def validate(self,attrs):
        password=attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        mobile_number=attrs.get('mobile_number')
        
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if password!=confirm_password:
            raise serializers.ValidationError("Password Must Be Same")
        elif not re.match(pattern,password):
               raise serializers.ValidationError("Password must contain a eight character  with a digit, a upper case , a lower case and a special character")    
        return attrs
    def create(self,validated_data):
        return Patient.objects.create_user(**validated_data)
# Patient Login
class PatientLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model = Patient
        fields = ['email','password']
    
    def validate(self,attrs):
     
        email=attrs.get('email')
        user=Patient.objects.filter(email=email)        
        if  not user.exists():
                    raise serializers.ValidationError({'message':'The email is not valid'})
        
        print("serializers")
        user=Patient.objects.get(email=email)
        if user.is_verified ==False:
            raise serializers.ValidationError({'error':"You are not verified"})
        return attrs



class PatientUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        error_messages={
            'blank': 'Username is required.'
        }
    )
    first_name = serializers.CharField(
        error_messages={
            'blank': 'First Name is required.'
        }
    )
    last_name = serializers.CharField(
        error_messages={
            'blank': 'Last Name is required.'
        }
    )
    dob = serializers.DateField(format='%Y-%m-%d')
    image_url=serializers.SerializerMethodField()
    class Meta:
        model=Patient
        fields=['id','username','first_name','last_name','dob','age','gender','image','image_url']
    
    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError(self.fields['username'].error_messages['required'])
        return value
        
    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username is required.")
        return value
        
    def get_dob(self, obj):
        return obj.dob.strftime('%Y-%m-%d') if obj.dob else None
    
    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return None
        
    @staticmethod
    def get_age(obj):
        # Calculate the age based on the dob field
        # You can implement your age calculation logic here
        return obj.age  # Assuming you have implemented the 'age' property in your model
        

                 
    
                      
# Patient get User
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Patient
        fields=['id','username','first_name','last_name','dob','age','gender','image']
        
   
                 

# verify otp for email verification
class Verifyotpserializers(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField()

# otp for reset password
class OtpForResetPassword(serializers.Serializer):
    email=serializers.EmailField()
    def validate(self,attrs):
        email=attrs.get('email')
        print(email)
        user=Patient.objects.filter(email=email)
        if not user:
            raise serializers.ValidationError({'messages':'The email you have entered is not a valid email!.','msg':'Error'}) 
        if user[0] and user[0].otp==None :
            print(email,'***************************************************')
            send_otp_via_mail(email)
            print("the otp is none and email is verified")
            return attrs
        
            
        elif  user[0].otp!=None:
            print("the otp is not None ")
            user[0].otp=None
            send_otp_via_mail(user[0])
            return attrs
            
        
            
        
# entering the otp for reset password
class PasswordResetSerializers(serializers.Serializer):
    otp=serializers.CharField()
    password=serializers.CharField(max_length=255,style={
        'input_type':'password' },write_only=True )
    confirm_password=serializers.CharField(max_length=255,style={
        'input_type':'password' },write_only=True )
    class Meta:
           fields=['password','confirm_password','otp']
    def validate(self,attrs):
        otp=attrs.get('otp')
        password=attrs.get('password')
        confirm_password=attrs.get('confirm_password')
        print(otp)
        print(password)
        print(confirm_password)
        pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
        if len(otp)==4:
            print(otp) 
            print(1)
            if otp is not None :
                print(otp)
                user=Patient.objects.filter(otp=otp).first()
                print(user)
                if user: 
                    if password!=confirm_password:
                        raise serializers.ValidationError({'message':'The password must be same','msg':'Error'})
                    if not re.match(pattern,password):
                         raise serializers.ValidationError({'message':"Password must contain a minimum eight character  with a digit, a upper case , a lower case and a special character",'msg':'Error'}) 
                    user.set_password(password)
                    print(1)
                    user.otp=None
                    user.save()
                    return attrs
                else:
                    raise serializers.ValidationError({'message':"The otp is incorrect",'msg':'Error'})
                raise serializers.ValidationError({'message':'the otp is not valid','msg':'Error'})
            
        raise serializers.ValidationError({'message':'the otp must contain four characters','msg':'Error'})

class ResendOtpserializer(serializers.Serializer):
    email=serializers.EmailField()
    def validate(self,attrs):
        email=attrs.get('email')
        print(email)
        user=Patient.objects.filter(email=email)
        
        
        if not user:
            raise serializers.ValidationError({'messages':'The email you have entered is not a valid email!.','msg':'Error'}) 
        if user[0] and user[0].otp==None :
            send_otp_via_mail(user[0])
            print("the otp is none and email is verified")
            return attrs
            
        if  user[0].otp!=None:
            print("the otp is not None ")
            user[0].otp=None
            send_otp_via_mail(user[0])
            
            # raise serializers.ValidationError({'messages':'Otp has been sent please check your mail.'})
            return attrs