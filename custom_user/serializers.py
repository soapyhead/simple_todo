from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from companies.models import Company


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(User.objects.all())]
    )
    companies = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=80),
        write_only=True
    )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'companies')

    def create(self, validated_data):
        user = User.objects.create_user_with_companies(
            email=validated_data['email'].lower(),
            password=validated_data['password'],
            companies=validated_data['companies']
        )
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    auth_company = serializers.CharField(min_length=1, max_length=80,
                                         required=True)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'auth_company')

    def validate(self, data):
        user = User.objects.filter(email__iexact=data['email']).first()
        if user:
            if not user.companies.filter(name__iexact=data['auth_company']):
                raise serializers.ValidationError(
                    "Company does not exist or user doesn't have access rights"
                )
            return data
        else:
            raise serializers.ValidationError('Unknown user')


class UserSerializer(serializers.ModelSerializer):
    companies = serializers.StringRelatedField(many=True)
    auth_company = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'companies', 'auth_company')

    def get_auth_company(self, obj):
        request = self.context['request']
        return request.session.get('company', None)

    def create(self, validated_data):
        user = User.objects.create_user_with_companies(
            email=validated_data['email'],
            password=validated_data['password'],
            companies=validated_data['companies']
        )
        return user
