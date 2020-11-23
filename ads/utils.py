from stations.models import Station, StationAdRelation
from django.db.models import Sum
from .models import Ad
from django.db.models import Max


# Function to add advertisment media to stataions in current area and hour
def ad_media_loader(instance):
    """Create relations Ad <--> Stations for requested hours"""

    # Add media to the development screen object (MAC:TEST)
    dev_station = Station.objects.filter(mac_addr="MAC:TEST").first()
    for hour in instance.hours:
        index = StationAdRelation.objects.filter(station=dev_station,
                                                 hour=hour).aggregate(Max('index'))["index__max"]
        if index is not None:
            index += 1
        else:
            index = 0
        StationAdRelation(ad=instance,
                          station=dev_station,
                          index=index,
                          hour=hour).save()
        instance.is_active = True
    # ------------------------------------------------

    percent_to_load = instance.percent_to_load
    sec_in_hour = 3600
    for area in instance.areas:
        area_stations_count = Station.objects.filter(area__in=instance.areas).count()
        # Filter requested percent of screens for each area
        stations_in_area = Station.objects.filter(area__in=instance.areas).exclude(mac_addr="MAC:TEST").order_by('?')[:round(percent_to_load * (area_stations_count / 100))]
        for station in stations_in_area:
            for hour in instance.hours:
                # Check the hour for enough free time (min 3 times in hour to show the advertisement)
                # Create relation
                busy_time = Ad.objects.filter(stadrelation__station=station,
                                              stadrelation__hour=hour).aggregate(Sum("duration"))["duration__sum"]
                if not busy_time:
                    busy_time = 0
                if int((sec_in_hour - busy_time) / instance.duration) >= 3:
                    index = StationAdRelation.objects.filter(station=station,
                                                             hour=hour).aggregate(Max('index'))["index__max"]
                    if index is not None:
                        index += 1
                    else:
                        index = 0
                    StationAdRelation(ad=instance,
                                      station=station,
                                      index=index,
                                      hour=hour).save()

                    instance.is_active = True
    instance.save()


def ad_media_disable(instance):
    """Delete relations Ad <--> Stations for current Ad.
    set Ad's is_active property to False"""
    for ad_relation in StationAdRelation.objects.filter(ad=instance).all():
        ad_relation.delete()
    instance.is_active = False
    instance.save()
