
from rest_framework import serializers
from list_api.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','username','password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance





















# from django.contrib.auth import get_user_model, authenticate

# UserModel = get_user_model()


# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = "__all__"

#     def create(self,clean_data):
#         user_obj = UserModel.objects.create_user(email=clean_data["email"],password=clean_data["password"])
#         user_obj.username = clean_data["username"]
#         user_obj.save()
#         return user_obj


# class UserLoginSerializer(serializers.ModelSerializer):



#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def check_user(self, clean_data):
#         user= authenticate(username=clean_data["email"],password=clean_data["password"])

#         if not user:
#             raise ValiationError("user not found")
#         return user


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ("email","username")



# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = "__all__"


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = "__all__"
