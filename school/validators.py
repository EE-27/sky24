from rest_framework import serializers


class LessonLinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if "youtube.com" not in value:
            raise serializers.ValidationError("The link must be from <<youtube.com>>!.")
