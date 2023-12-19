
from rest_framework import serializers
from rest_framework.fields import empty

from config.settings import FRONT_HOSTNAME


class CalculatorPaySerializer(serializers.Serializer):
    type = serializers.CharField(max_length=255, required=False)
    monthlyPayGross = serializers.FloatField(required=False)
    under26 = serializers.BooleanField(required=False)
    zus = serializers.CharField(max_length=255, required=False)
    sickLeave = serializers.BooleanField(required=False)
    costOfIncome = serializers.FloatField(required=False)
    zusb2b = serializers.CharField(max_length=255, required=False)
    tax = serializers.CharField(max_length=255, required=False)



    class Meta:
        fields = ['type', 'monthlyPayGross', 'under26', 'zus', 'sickLeave', 'costOfIncome', 'zusb2b', 'tax']

class ArticleSerializer(serializers.Serializer):
        id = serializers.UUIDField(required=False)
        type = serializers.CharField(max_length=255, required=False)
        link = serializers.CharField(max_length=255, required=False)
        title_eng = serializers.CharField(max_length=255, required=False)
        description_eng = serializers.CharField(max_length=255, required=False)
        image = serializers.SerializerMethodField()

        def get_image(self, obj):
            if obj.image:
                return FRONT_HOSTNAME +f"/media/news/{obj.guid}.jpg"
                # return "http://localhost:8070" +f"/media/news/{obj.guid}.jpg"
            else:
                return None


        class Meta:
            fields = ['id' ,'type', 'link', 'title_eng', 'description_eng', 'image']