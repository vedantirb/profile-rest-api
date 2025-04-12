from rest_framework import serializers

from profiles_api import models


class HelloSerializer(serializers.Serializer):
    """ Serializers name field for testing our APIView """
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile object """

    class Meta:
        """ in the modelserializer use meta to configure serializer to point to specific model in our porject """
        model = models.UserProfile
        fields = ("id", "email", "name", "password") #field which want to access in model
        # set password field to write only using custom configuration
        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"}
            }
        }

    def create(self, validated_data):
        """ create and return new user """
        user = models.UserProfile.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"]
        )
        return user


    def update(self, instance, validated_data):
        """Handle updating user account , there is a bug in `UserProfileSerializer`
        Issue :

            If a user updates their profile, the password field is stored in cleartext, and they are unable to login.

        Cause :

        This is because we need to override the default behaviour of Django REST Frameworks ModelSerializer to hash the users password when updating.

        Fix :

        To fix the issue, add the below method to the `UserProfileSerializer`
        """
        if "password" in validated_data:
            password = validated_data.pop("password")
            instance.set_password(password)
        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """ Serializer profilefeedItem """

    class Meta:
        model = models.ProfileFeedItem
        fields = ("id", "user_profile", "status_text", "created_on")
        extra_kwargs = {
            "user_profile": {"read_only": True}
        }
        
