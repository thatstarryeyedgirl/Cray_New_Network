from rest_framework import serializers
from .models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        # maps the fields from the News model to the API; 
        fields = ["id", "author", "title", "body", "image", "video", "created_at", "updated_at"]
        # prevents users from editing id, author, and timestamp fields
        read_only_fields = ["id", "author", "created_at", "updated_at"]

    def validate(self, data):
        # ensures that every news article includes an image; raises an error if missing
        if not data.get("image"):
            raise serializers.ValidationError({"image": "An image is required for news."})
        
        # Check if title already exists
        title = data.get("title")
        if title and News.objects.filter(title=title).exists():
            raise serializers.ValidationError({"title": "This story already exists try updating the story instead"})
        
        # Check if video is provided and valid
        video = data.get("video")
        if video and hasattr(video, 'content_type'):
            if not video.content_type.startswith('video/'):
                raise serializers.ValidationError({"video": "Invalid video file format."})
        
        return data
    
