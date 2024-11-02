from django.http import Http404
from rest_framework.views import APIView
from .models import Blog, User, Comment
from .serializer import UserRegisterSerializer, BlogSerializer, UserSerializer, CommentSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data['response'] = 'Account has been created'

            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        return Response(data)


class UserAPIList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAPIUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BlogAPIList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogAPIUpdate(generics.UpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogAPIDestroy(generics.DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class BlogAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs["pk"]
        try:
            instance = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404("No id found!")
        instance.views = instance.views + 1
        instance.save()
        return Response(BlogSerializer(instance).data)


class CommentAPIList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeAPIView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs["pk"]
        try:
            instance = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404("No id found!")
        instance.likes = instance.likes + 1
        instance.save()
        return Response("Like submited!")
