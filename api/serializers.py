from rest_framework import serializers
from app.models import Channel
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

class Export(object):
    def __init__(self, time, endtime, pmin, channelId):
        self.time = time
        self.endtime = endtime
        self.pmin = pmin
        self.channelId = channelId

# Create serializer of the multiple export channel endpoit
class ExportMultipleChannelsSerializer(serializers.Serializer):

    time = serializers.DateTimeField()
    endtime = serializers.DateTimeField()
    pmin = serializers.IntegerField()
    channelId = serializers.IntegerField()
    # Add other fields here

    def is_valid(self):

        try:
            self.validate()
            return True
        except Exception:
            return False
        
    def validate(self):
        
        # get all exports requests, in the object
        for export in self.data:
            time = export['time']
            endtime = export['endtime']
            pmin = export['pmin']
            channelId = export['channelId']

            # Check if channelId exists

            try:

                channel = Channel.objects.get(pk=int(channelId))

            except ObjectDoesNotExist:
                raise ValidationError({'channelId' : 'Theres no channel with this id'})

            # Check if timef is before time
            if endtime < time:
                raise ValidationError({'endtime' : '"endtime" must be greater than "time"'})

        return self.data