from rest_framework import serializers
from app.models import *

class StoreURLSerializers(serializers.ModelSerializer):
	def create(self, validated_data):
		return store_tinyurl.objects.create(**validated_data)

	class Meta:
		model = store_tinyurl
		fields = (
			'short_key',
			'url',
			'create_time'
		)

