from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from .models import Comments, Review


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='comments'
    )

    class Meta:
        model = Comments
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    review = SlugRelatedField(
        slug_field='review', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
