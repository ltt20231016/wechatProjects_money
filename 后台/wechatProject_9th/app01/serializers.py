from rest_framework import serializers,exceptions
from app01 import models


class UserModelSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ["id", "username", "password", "confirm_password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only":True}
        }

    def validate_confirm_password(self, value):
        # value=confirm_password
        # self.inital_data：fields的全部字段值
        password = self.initial_data.get("password")
        if password != value:
            raise exceptions.ValidationError("密码不一致！")
        return value


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "password"]


class RecordSerializers(serializers.ModelSerializer):
    type = serializers.CharField(source="get_type_display")
    # category = serializers.CharField(source="category.category_name")
    category = serializers.SerializerMethodField()
    username = serializers.CharField(source="user.username")

    class Meta:
        model = models.Record
        fields = ["type", "ctime", "money", "note", "category", "username"]

    def get_category(self, obj):
        return {"id": obj.category.id, "name": obj.category.category_name}
