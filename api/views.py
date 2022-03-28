import requests
from api.models import GeolocationData
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers import GeolocationDataSerializer
from django.db import DatabaseError

def ip_curl(ip):
    """
    Function to colect ip geolocation data from ipstack.com
    and return json file
    """
    try:
        response = requests.get(
            "http://api.ipstack.com/" + ip + "?access_key=dc07b8645087135b1064ba9bca4d7f40",
        )
        rawData = response.json()
    except requests.exceptions.ConnectionError as e:
        return Response({'message': 'Something wrong with connection - check url'}, e)
    except requests.exceptions.Timeout as e:
        return Response({'message': 'Server Timeout, try again later'}, e)
    return rawData

def create_geolocation_object(user, rawData, is_own):
    """
    Function to add an object to the GeolocationData model, needs:
        user
        raw_data(json file from ipstack.com)
        is_own(responsible for indicating if ip is own or foreign)
    """

    # if some data is None -> add N/A in charfields or 0.0 in floatfields
    ip = rawData['ip']
    continent_code = rawData['continent_code'] or "N/A"
    continent_name = rawData['continent_name'] or "N/A"
    country_code = rawData['country_code'] or "N/A"
    country_name = rawData['country_name'] or "N/A"
    region_code = rawData['region_code'] or "N/A"
    region_name = rawData['region_name'] or "N/A"
    city = rawData['city'] or "N/A"
    zip = rawData['zip'] or "N/A"
    latitude = rawData['latitude'] or "0.0"
    longitude = rawData['longitude'] or "0.0"

    # create new geolocation data object in data base, is_own parameter need to be pass in function
    geolocation_data = GeolocationData(
        user=user,
        ip=ip,
        continent_code=continent_code,
        continent_name=continent_name,
        country_code=country_code,
        country_name=country_name,
        region_code=region_code,
        region_name=region_name,
        city=city,
        zip=zip,
        latitude=latitude,
        longitude=longitude,
        is_own=is_own,
    )
    geolocation_data.save()
    return Response({'info': 'succesful look up'}, status=status.HTTP_200_OK)


class GetUserGeolocationData(APIView):
    """
    APIView to get User own ip geolocation data,
        If the user does not know his ip address,
        it will be automatically collected and
        GeolocationData object added to the database
        when get the endpoint: ".../api/get_user_geolocation_data/"
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        # logic to collect visitor ip address, visitor must be autenticated so its user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        # checking if the user hasn't already look up his ip(to reduce ipstack plan usage)
        geolocation_qs = GeolocationData.objects.filter(ip=ip)
        if geolocation_qs.exists():
            return Response({'message': 'ip already in database'}, status=status.HTTP_400_BAD_REQUEST)

        # collect raw data from ipstack.com
        rawData = ip_curl(ip)

        #add is_own parameter beacouse we collect user ip
        is_own = True

        create_geolocation_object(self.request.user, rawData, is_own)

        return Response({'message': 'succesful look up'}, status=status.HTTP_200_OK)

class GeolocationDataViewSet(ModelViewSet):
    serializer_class = GeolocationDataSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Filter queryset - You can only see your geolocation data
        """
        try:
            return self.request.user.geolocation.all()
        except DatabaseError:
            return Response({'message': 'database error - contact with site admin'}, status=status.HTTP_400_BAD_REQUEST)


    def create(self, request, *args, **kwargs):
        """
        Function that adds a new object based on ip address and checks if ip geolocation data is already in the db
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # catch ip from serializer
            validatedData = serializer.validated_data
            ip = validatedData.get('ip')

            # check if ip is already in database
            qs = GeolocationData.objects.filter(ip=ip)
            if qs.exists():
                return Response({'message': 'ip already in database'}, status=status.HTTP_208_ALREADY_REPORTED)

            else:
                # if ip isnt in database catch geolocation data based on ip and add object to database
                rawData = ip_curl(ip)
                is_own = False
                create_geolocation_object(self.request.user, rawData, is_own)
                return Response({'message':'Ip address correct - sucessful added Geolocation Data'}, status=status.HTTP_201_CREATED)

        return Response({'message': 'something went wrong - serializer not valid'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """
        Function destroy selected object
        """
        geolocation_data = self.get_object()
        geolocation_data.delete()
        return Response({'message': 'Geolocation data succesful deleted'}, status=status.HTTP_200_OK)


