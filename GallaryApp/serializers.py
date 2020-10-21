from rest_framework import serializers

from .models import GallaryImages


class GallaryImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GallaryImages
        fields = ("id","file", "is_active", "is_deleted", 'created_date', 'last_updated_date')

    def update(self, instance, validated_data):
        if validated_data.get('file'):
            instance.file = validated_data.get('file')

        instance.save()
        return self.instance
