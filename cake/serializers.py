from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser, Ingredient, Cake, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id","username", 'phone_number', 'role']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'phone_number', 'role', 'password']
        read_only_fields = ['role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            password=validated_data['password']
        )
        return user


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'extra_price', 'image']


class CakeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField

    class Meta:
        model = Cake
        fields = ['id', 'image', 'title', 'description', 'created_at', 'delivery_date', 'base_price', 'is_available',
                  'ingredients', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    cake = CakeSerializer(read_only=True)
    cake_id = serializers.PrimaryKeyRelatedField(
        queryset=Cake.objects.all(), many=True,
        source='cake', write_only=True, required=False
    )

    ingredients = IngredientSerializer(many=True, read_only=True)
    ingredients_id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        many=True,
        source='ingredients',
        write_only=True
    )

    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ['id', 'user', 'cake', 'cake_id', 'ingredients', 'ingredients_id',
                  'status', 'courier', 'total_price']
        read_only_fields = ['user', 'status', 'courier']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Username yoki parol noto‘g‘ri!")

        refresh = RefreshToken.for_user(user)
        data['access'] = str(refresh.access_token)
        data['refresh'] = str(refresh)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'phone_number', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            role=validated_data.get('role', 'client'),
            password=validated_data['password']
        )
        return user
