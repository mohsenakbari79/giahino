from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import authentication, permissions
from Auth.models import User
from Devices.models import Device,Sensor,Relay,PinOfDevice,SensorForDevice
from Devices.serializers import DeviceSerializer,SensoreSerializer,PinSerializer,SensoreForDeviceSerializer,RelayForDevice
from collections import Counter,defaultdict
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from Devices.utils import redisclient
import json

class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('hostname',)
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        queryset = queryset.filter(user=self.request.user)
        return queryset
    
   

class SensorViewSet(ModelViewSet):
    queryset = Sensor.objects.all()
    serializer_class =  SensoreSerializer
    http_method_names = ['post', 'get', 'delete', 'put']
    search_fields = ('uniq_name')

class RelayViewSet():
    queryset = Relay.objects.all()
    serializer_class =  RelaySerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name')

class RelayForDeviceViewSet(ModelViewSet):
    queryset = RelayForDevice.objects.all()
    serializer_class =  RelayForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name')

class SensorForDeviceViewSet(ModelViewSet):
    queryset = SensorForDevice.objects.all()
    serializer_class =  SensoreForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return result


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        return super().update(request, *args, **kwargs)

class PinForDeviceViewSet(ModelViewSet):
    queryset = PinOfDevice.objects.all()
    serializer_class = PinSerializer
    http_method_names = ['post', 'get', 'delete', 'put']   

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return result


    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pin = json.loads(request.data.get("pin"))
        if pin != None:
            pin_counter=dict(Counter(pin.values()))
            pin_counter.pop(None)
            try:
                for key,value in pin_counter.items():
                    split_key=key.split("_")
                    sensor =None
                    if split_key[0]=="sensor":
                        sensor = self.queryset.get(pk=kwargs["pk"]).device.device_sensor.get(pk=split_key[1]).sensor
                    if split_key[0] in ["sensor","device"]:
                        return Response({'error': f"A sensor {key} not good format (sensor_pk | relay_pk) "}, status=status.HTTP_400_BAD_REQUEST)
                    elif sensor != None and value != sensor.pin_number :
                        return Response({'error': f"A sensor {sensor.uniq_name} has {sensor.pin_number} pins while you have given {sensor}"}, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({'error': f"Use the corresponding device sensors for all pins"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs) 


class SensorForDeviceViewSet(ModelViewSet):
    queryset = SensorForDevice.objects.all()
    serializer_class =  SensoreForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    search_fields = ('uniq_name')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        return result

class TimeDefualtValueViewSet(ModelViewSet):
    queryset = SensorForDevice.objects.all()
    serializer_class =  SensoreForDeviceSerializer
    http_method_names = ['post' , 'get', 'delete', 'put']
    # search_fields = ('uniq_name')

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        pin = json.loads(request.data.get("pin"))
        all_time=TimeEnable.objects.filter(sensorfordevice=kwargs["sensorfordevice"])
        if (kwargs["end_day"] != None and kwargs["start_day"] < kwargs["end_day"]) or (kwargs["end_time"] != None and kwargs["start_time"] < kwargs["end_time"]):
            pass
        for time_check in all_time:          
            if kwargs["start_day"] != None and kwargs["end_day"] != None and\
                    time_check.start_day != None and time_check.start_day != None and  \
                    (time_check.start_day < d2.start_day < time_check.end_day) or (time_check.start_day < d2.end_day < time_check.end_day) or (d2.start_day <= time_check.start_day and d2.end_day >= time_check.end_day):       
                if kwargs["start_time"] != None and kwargs["end_time"] != None and\
                    time_check.start_time != None and time_check.start_time != None and  \
                    (time_check.start_time < d2.start_time < time_check.end_time) or (time_check.start_time < d2.end_time < time_check.end_time) or (d2.start_time <= time_check.start_time and d2.end_time >= time_check.end_time):
                    raise ValidationError()  
        return super().update(request, *args, **kwargs)
    


# @api_view(['GET', 'POST'])
# def sensorvalue(request,device,sensore=None):
#     try:
#         obj_device = Device.objects.get(name=device)
        
        
#         senosr_list=[]
#         rs=redisclient.query(f"select * from {obj_device.name}")
#         respons ={"device":obj_device.name,"data":[]}
#         if sensore is not None:
#             senosr_list.append(list(rs.get_points(tags={"sensor_id": f"{sensore}"})))
#         else:
#             senosr=obj_device.device_sensor.all()
#             for sen in senosr:
#                 templist=list(rs.get_points(tags={"sensor_id": f"{sen.pk}"}))
#                 if 0<len(templist):
#                     senosr_list.extend(templist)
#         for value in senosr_list:
#             sensor=obj_device.device_sensor.get(sensor=value["sensor_id"]).sensor
#             respons["data"].append({
#                 "sensore":sensor.uniq_name,
#                 "value":value["data"],
#                 "time":value["time"],
#             })
#         return Response(data=respons)
#     except Exception as e:
#         print("salam",e, e.__traceback__.tb_lineno )
#         return Response({'error': f"not exit device or senore by id entered"}, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET', 'POST'])
def sensorvalue(request,device,sensore=None):
    try:
        obj_device = Device.objects.get(name=device)

        senosr_list=[]
        rs=redisclient.query(f"select * from {obj_device.name}")
        respons ={"device":obj_device.name,"data":[]}
        if sensore is not None:
            senosr_list.append(list(rs.get_points(tags={"sensor_id": f"{sensore}"})))
        else:
            senosr=obj_device.device_sensor.all()
            for sen in senosr:
                templist=list(rs.get_points(tags={"sensor_id": f"{sen.pk}"}))
                if 1==len(templist):
                    senosr_list.append(templist)
                elif 1<len(templist):
                    all_value={
                        "sensor_id":sen.pk,
                        "data":[value["data"] for value in templist],
                    }
                    senosr_list.append(all_value)
        for value in senosr_list:
            sensor=obj_device.device_sensor.get(sensor=value["sensor_id"]).sensor
            respons["data"].append({
                "sensore":sensor.uniq_name,
                "value":value["data"],
            })
        return Response(data=respons)
    except Exception as e:
        print("salam",e, e.__traceback__.tb_lineno )
        return Response({'error': f"not exit device or senore by id entered"}, status=status.HTTP_400_BAD_REQUEST)


