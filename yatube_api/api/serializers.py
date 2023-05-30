from posts.models import Comment, Follow, Group, Post, User
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CurrentUserDefault, ModelSerializer
from rest_framework.serializers import SlugRelatedField as SlugRelated
from rest_framework.serializers import ValidationError


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
    author = SlugRelated(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)


class FollowSerializer(ModelSerializer):
    user = SlugRelated(
        read_only=True,
        slug_field='username',
        default=CurrentUserDefault()
    )
    following = SlugRelated(
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
