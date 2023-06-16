from rest_framework import serializers

from comment.serializers import CommentSerializer
from .models import Post, PostImage
from category import models
from category.models import Category


class PostListSerializer(serializers.ModelSerializer):
    # в json есть два ключа owner_name и category_name.
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = Post
        fields = ('id', 'title', 'owner', 'owner_username', 'category', 'category_name', 'preview')

    def to_representation(self, instance):
        # repr это просто json данные ОДНОГО объекта.INstance это объект экземпляра класса.
        repr = super(PostListSerializer, self).to_representation(instance)
        repr['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
            repr['is_favorite'] = user.favorites.filter(post = instance).exists()
        return repr


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(required=True, queryset=Category.objects.all())
    owner = serializers.ReadOnlyField(source='owner.id')
    images = PostImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        images = request.FILES.getlist('images')
        post = Post.objects.create(**validated_data)
        for image in images:
            PostImage.objects.create(image=image, post=post)
        return post


class PostDetailSerializer(serializers.ModelSerializer):
    owner_username = serializers.ReadOnlyField(source='owner.username')
    category_name = serializers.ReadOnlyField(source='category.name')
    images = PostImageSerializer(many=True)

    # это первфй способ с помошью related name
    # comment = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['commnents_count'] = instance.comments.count()
        repr['comments'] = CommentSerializer(
            instance.comments.all(), many=True
        ).data
        repr['likes_count'] = instance.likes.count()
        user = self.context['request'].user
        if user.is_authenticated:
            repr['is_liked'] = user.likes.filter(post=instance).exists()
            repr['is_favorite'] = user.favorites.filter(post = instance).exists()
        return repr
