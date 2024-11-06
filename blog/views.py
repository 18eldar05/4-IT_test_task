from django.http import Http404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import Blog, User, Comment
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializer import UserRegisterSerializer, BlogSerializer, UserSerializer, CommentSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = 'Account has been created'
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
    permission_classes = (IsOwnerOrAdminOrReadOnly,)


class BlogAPIList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class BlogAPIView(APIView):
    permission_classes = (IsOwnerOrAdminOrReadOnly,)

    def get(self, request, **kwargs):
        pk = kwargs["pk"]
        try:
            instance = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404("No id found!")
        instance.views = instance.views + 1
        instance.save()
        return Response(BlogSerializer(instance).data)

    def put(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            instance = Blog.objects.get(pk=pk)
        except Blog.DoesNotExist:
            raise Http404("No id found!")

        serializer = BlogSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            Blog.objects.filter(pk=pk).delete()
        except Blog.DoesNotExist:
            raise Http404("No id found!")

        return Response({"post": "deleted post " + str(pk)})


class CommentAPIList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrAdminOrReadOnly,)


class LikeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        pk = kwargs["pk"]
        try:
            instance = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404("No id found!")
        instance.likes = instance.likes + 1
        instance.save()
        return Response("Like submited!")
