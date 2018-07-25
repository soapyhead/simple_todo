from rest_framework import serializers
from companies.serializers import CompanySerializer
from .models import Todo


class CreateTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('description',)


class TodoSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Todo
        fields = '__all__'
