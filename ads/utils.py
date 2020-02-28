from stations.models import Station, StationProgramRelation
from programs.models import Program, ProgramAdMembership


# Function to add advertisment media to stataions in current area and hour
def ad_media_loader(instance):
    # TODO: Determining the percentage of stations to engage relative to requested views
    stations_in_area = Station.objects.filter(area__in=instance.areas).order_by('?')[:5]
    for station in stations_in_area:
        """ check station for existed program for any needed hour in request  """
        for hour in instance.hours:
            """ Check for existed related hour program for station """
            program_rel = StationProgramRelation.objects.filter(station=station, hour=hour).first()
            if program_rel:
                try:
                    """ In case related hour program for station exist:
                        - create relation object for program <--> advertisment """
                    program = program_rel.program
                    ProgramAdMembership(ad=instance,
                                        program=program,
                                        ad_index=ProgramAdMembership.objects.filter(program=program).count()).save()
                except Exception as e:
                    raise e
            else:
                try:
                    """ In case related hour program for station doesnt exist """
                    """ create program pbject """
                    Program(title=str(station.id) + "_" + hour,
                            description=str(station.id) + "_" + hour + "_temporarily").save()
                    program = Program.objects.filter(title=str(station.id) + "_" + hour,
                                                     description=str(station.id) + "_" + hour + "_temporarily").first()
                    """ create relation object program <--> advertisment """
                    ProgramAdMembership(ad=instance,
                                        program=program,
                                        ad_index=0).save()
                    """ create relation object station <--> program (for current hour) """
                    StationProgramRelation(program=program,
                                           station=station,
                                           hour=hour).save()
                except Exception as e:
                    raise e
    instance.is_active = True
    instance.save()


# Function to remove advertisment media from all stataions programs
def ad_media_disable(instance):
    """Action that return list of Sifia's areas"""
    for program_relation in ProgramAdMembership.objects.filter(ad=instance).all():
        print(program_relation)
        program_relation.delete()
        print(print(program_relation))
    instance.is_active = False
    instance.save()
