from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.db import models
from django.shortcuts import get_object_or_404

from rest_framework import serializers, validators
from reviews.models import Comment, Review
from titles.models import Category, Genre, Title

User = get_user_model()
check_token = default_token_generator.check_token


class SignUpSerializer(serializers.Serializer):
    username = serializers.RegexField(
        r'^(?!me$)[\w.@+-]+$',
        max_length=150
    )
    email = serializers.EmailField()

    def validate(self, data):
        if User.objects.filter(
            ~models.Q(email=data['email']),
            username=data['username'],
        ).exists():
            raise serializers.ValidationError(
                {'username': 'Такой пользователь уже существует!'}
            )
        if User.objects.filter(
            ~models.Q(username=data['username']),
            email=data['email']
        ).exists():
            raise serializers.ValidationError(
                {'email': 'Такой email уже существует!'}
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        r'^[\w.@+-]+$',
        max_length=150
    )
    confirmation_code = serializers.RegexField(
        r'^(?:\d{5})|(?:\w{3}-\w{20})$'
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not check_token(user, data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения!'}
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        fields = '__all__'
        model = Title


class CurrentTitleDefault:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context['view'].kwargs['title_id']


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=CurrentTitleDefault())

    class Meta:
        model = Review
        fields = '__all__'
        validators = (
            validators.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Вы уже оставили отзыв этому произведению.',
            ),
        )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        exclude = ('review',)
