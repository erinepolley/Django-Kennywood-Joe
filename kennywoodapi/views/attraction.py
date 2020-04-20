"""View module for handling requests about attractions"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import Attraction
#Serializer = the kitchen where you make JSON
class AttractionSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for attractions

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    #Must have Meta class. Instructions. Or else serializer won't know how to build it. 
    class Meta:
        #model = recipe
        model = Attraction
        url = serializers.HyperlinkedIdentityField(
            view_name='attraction',
            lookup_field='id'
        )
        #fields = the columns that you want to inlcude in the JSON response
        fields = ('id', 'url', 'name', 'area')
        depth = 2

# The CRUD functionality is inherited from ViewSet.
class Attractions(ViewSet):

    def list(self, request):
        """Handle GET requests to park attractions resource

        Returns:
        Response -- JSON serialized list of park attractions
        """

        attractions = Attraction.objects.all()
        #Checking to see if an id is passed? What does this have to do with area?
        area = self.request.query_params.get('area', None)
        
        if area is not None:
            attractions = attractions.filter(area__id=area)

            serializer = AttractionSerializer(attractions, many=True, context={'request': request})

            return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single attraction

        Returns:
        Response -- JSON serialized attraction instance
        """
        try:
            attraction = Attraction.objects.get(pk=pk)
            serializer = AttractionSerializer(attraction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        new_attraction_item = Attraction()
        new_attraction_item.name = request.data["name"]
        #I'm not sure how to obtain a foreign key.
        new_attraction_item.area_id = request.data["area_id"]
        new_attraction_item.save()
        serializer = AttractionSerializer(new_attraction_item, context={'request': request})

        return Response(serializer.data)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
          Response -- Empty body with 204 status code
        """
        #Why is objects plural? Aren't you just getting one? And are you getting this object directly from the database?
        attraction = Attraction.objects.get(pk=pk)
        attraction.name = request.data["name"]
        #Maybe there's a dropdown menu, and each menu item has an id somewhere you can obtain?
        attraction.area_id = request.data["area_id"]
        attraction.save()
        #Where does the status come from? Is that viewsets? And is this referring to what the user sees in the network tab?
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park area

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            attraction = Attraction.objects.get(pk=pk)
            attraction.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Attraction.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
#What is this Exception word? Is it some kind of viewset feature?
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

