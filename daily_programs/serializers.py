from rest_framework import serializers
from .models import DailyProgram, DailyProgramMembership
from programs.models import Program
from datetime import datetime
from django.shortcuts import get_object_or_404


class DailyProgramSerializer(serializers.HyperlinkedModelSerializer):
    """Daily media Program serializer"""

    class Meta:
        model = DailyProgram
        fields = ("id", "url", "creator", "creator_id", "title", "description",
                  "program_members", "is_in_use", "created_at", "updated_at")

        read_only_fields = ("id", "url", "creator", "creator_id",
                            "created_at", "updated_at")

        required_fields = ("client", "title", "description")
        extra_kwargs = {field: {"required": True} for field in required_fields}

    def get_current_user(self):
        """Gets current user from request"""
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return user
        return None

    def validate_creator(self, value):
        """Validate creator field"""
        user = self.get_current_user()
        if user != value:
            raise serializers.ValidationError("You can not create services for another user")
        return value

    def _custom_time_shema_validator(self):
        request_data = self.context.get("request").data

        if "time_shema" not in request_data:
            raise serializers.ValidationError("Bad formated json.")
        time_schema = request_data["time_shema"]

        if len(time_schema) < 1:
            raise serializers.ValidationError("Bad formated json.")
        elif len(time_schema) == 1:
            get_object_or_404(Program, id=time_schema["0"]["id"])
            time_schema["0"]["stop_time"] = time_schema["0"]["start_time"]
        else:
            for index in range(len(time_schema)):
                get_object_or_404(Program, id=time_schema[str(index)]["id"])
                if index + 1 < len(time_schema):
                    if datetime.strptime(time_schema[str(index+1)]["start_time"], "%H:%M:%S").time() \
                                < datetime.strptime(time_schema[str(index)]["start_time"], "%H:%M:%S").time():
                        raise serializers.ValidationError("Bad formated json.")
                    else:
                        time_schema[str(index)]["stop_time"] = time_schema[str(index+1)]["start_time"]
                else:
                    time_schema[str(index)]["stop_time"] = "23:59:59"
        return time_schema

    def create(self, validated_data):
        time_schema = self._custom_time_shema_validator()

        daily_program = super().create(validated_data)
        for key in time_schema:
            print(key)
            DailyProgramMembership(program=Program.objects.get(id=time_schema[key]["id"]),
                                   daily_program=daily_program,
                                   start_time=time_schema[key]["start_time"],
                                   stop_time=time_schema[key]["stop_time"]).save()
        return daily_program

    def update(self, instance, validated_data):
        time_schema = self._custom_time_shema_validator()

        daily_program = super().update(instance, validated_data)
        daily_program.program_members.clear()
        for key in time_schema:
            print(key)
            DailyProgramMembership(program=Program.objects.get(id=time_schema[key]["id"]),
                                   daily_program=daily_program,
                                   start_time=time_schema[key]["start_time"],
                                   stop_time=time_schema[key]["stop_time"]).save()
        return daily_program


class DailyProgramMembershipSerializer(serializers.HyperlinkedModelSerializer):
    """Daily media program membership serializer"""

    class Meta:
        model = DailyProgramMembership
        fields = ("id", "url", "program",  "daily_program",
                  "start_time",  "stop_time",
                  "created_at", "updated_at")
        read_only_fields = ("program",  "daily_program", "url")
