from rest_framework import serializers

from .models import Anketa



class Anketa_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Anketa
        fields = "__all__"