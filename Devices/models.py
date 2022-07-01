from django.db import models
from django.core.exceptions import ValidationError
from Auth.models import AuthDevice
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Device(models.Model):
    name=models.CharField(max_length=50,blank=True)
    versions=models.IntegerField(default=1,blank=True)
    release=models.FileField(upload_to ='release/',blank=True)
    auth=models.OneToOneField("Auth.AuthDevice",on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        auth_device=AuthDevice()
        auth_device.save()
        self.auth=auth_device
        super(Device, self).save(*args, **kwargs)
    


class Sensor(models.Model):
    uniq_name = models.CharField(max_length=50,unique=True)
    pin_number = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ])
    
class SensorValueType(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE,related_name="sensor")
    name = models.CharField(max_length=15) 
    TYPE_CHOICES = (
        ("INT", "integer"),
        ("STR", "string"),
    )
    types = models.CharField(max_length=4,choices=TYPE_CHOICES, default=1)   
    validation=models.JSONField()
    def save(self, *args, **kwargs):
        if self.TYPE_CHOICES == 1:
            self.validation={
                "max_value" : None,
                "min_value" : None,
            }
        elif self.TYPE_CHOICES == 2:
            self.validation={
                "key_porblem" : [],
            }
        super(SensorValueType, self).save(*args, **kwargs)
    class Meta:
        unique_together = ('sensor', 'name',)



class SensorForDevice(models.Model):
    id = models.AutoField(primary_key=True)
    device = models.ForeignKey(Device,on_delete=models.CASCADE,related_name="device_sensor")
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    enable = models.BooleanField(default=True)
    class Meta:
        unique_together = ('device', 'id',)

class PinOfDevice(models.Model):
    device = models.OneToOneField(Device,on_delete=models.CASCADE,primary_key = True)
    pin_number = models.IntegerField(default=10,editable=False)
    pin = models.JSONField(blank=True) # serialized custom data
    def save(self, *args, **kwargs):
        if self.pin==None:
            temp={}
            for pin_num in range(self.pin_number):
                temp[pin_num]=None
            self.pin=temp
        super(PinOfDevice, self).save(*args, **kwargs)
    @property
    def pin_dict(self):
        return simplejson.loads(self.pin)

class TimeEnable():
    sensorfordevice=models.ForeignKey(SensorForDevice,on_delete=models.CASCADE,related_name="time_enable")
    start_day=models.DateField()
    end_day=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    def save(self, *args, **kwargs):
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
                
        super(TimeEnable, self).save(*args, **kwargs)    
