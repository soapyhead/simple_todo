from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import TodoSerializer, CreateTodoSerializer
from .models import Todo
from companies.models import Company


class TodoModelViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = TodoSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Todo.objects.all()

        auth_company = self.request.session.get('company', None)
        if auth_company:
            self.queryset = Todo.objects.filter(
                company__name__iexact=auth_company)
            return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = CreateTodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        auth_company = self.request.session.get('company', None)
        if auth_company:
            company = Company.objects.filter(name__iexact=auth_company).first()
            if company:
                todo = Todo.objects.create(company=company,
                                           **serializer.validated_data)
                return Response(self.serializer_class(todo).data,
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'unknown company'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)
