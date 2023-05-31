from posts.models import Comment, Follow, Group, Post, User
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import (CurrentUserDefault, ModelSerializer,
                                        SlugRelatedField, ValidationError)


class PostSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(ModelSerializer):
    user = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )
    following = SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:
        model = Follow
        fields = '__all__'

    def validate_following(self, value):
        user = self.context['request'].user

        if user == value:
            raise ValidationError(
                'Нельзя подписаться на самого себя')

        if Follow.objects.filter(user=user, following=value).exists():
            raise ValidationError(
                'Вы уже подписаны на этого автора')
        return value
