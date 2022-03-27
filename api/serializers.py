from rest_framework import serializers
from api.models import GeolocationData
import ipaddress

class GeolocationDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeolocationData
        fields = ['id','ip', 'continent_code', 'continent_name', 'country_code', 'country_name',
                  'region_code', 'region_name', 'city', 'zip', 'latitude', 'longitude',]
        read_only_fields = ['id', 'continent_code', 'continent_name', 'country_code', 'country_name',
                  'region_code', 'region_name', 'city', 'zip', 'latitude', 'longitude',]

    def validate_ip(self, value):
        """
        Function validate ip address, "ipaddress" library used
        """
        try:
            ip = ipaddress.ip_address(value)
            return value
        except ValueError:
            raise serializers.ValidationError({'message':'invalid ip format'})
