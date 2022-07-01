from easy_pika.pika_obj import PikaMassenger
import json 
# import redis
# from redis.commands.json.path import Path
import threading
# from Auth.models import AuthDevice
# from Devices.models import Device,SensorForDevice,Sensor
from Devices.utils import add_sensor_to_device,add_sensor,sensor_value
# client = redis.Redis(host='localhost', port=6379, db=0)
# result = client.json().get('somejson:1')
router_amqp={}

PMI=PikaMassenger(host='localhost',port=5672,username='guest',password='guest',exchange_name="Message2")
def callback(ch, method, properties, body):
    try:
        print("*******************************\n",ch.__dict__,"\n*******************************\n",method.__dict__,"\n*******************************\n",properties.__dict__)
        body=json.loads(body)
        swich= body.get('type',None)
        device_auth_id=method.routing_key
        device = AuthDevice.objects.get(pk=device_auth_id).device
        if swich !=None  :
            if swich == "sensor_value":
                id_sensor = body.get('type',None)
                sensor_value(device,id_sensor,body)
            elif swich == "pin":
                PMI.send_message(method.routing_key,json.loads(device.pinofdevice.pin))
        # print(body)
        # # if method.routing_key:
        # if method.router_key:
        
        # if method.routing_key=="sensore":
        #     add_sensor(body['value'])    
        #     PMI.connection._channel.basic_ack(method.delivery_tag)
        #     return
        # device=Device.objects.get(name=properties.headers['DeviceNameU'])
        # if method.routing_key=="device_sensore":
        #     add_sensor_to_device(device.pk,body['value']) 
        # elif "sensor_" in method.routing_key.lower():
        #     sensor_name=method.routing_key.split("_")[1]
        #     sensor_value(sensor_name,device=device,body=body)
        # elif "enable_sensore" in method.routing_key.lower():
        #     sensor_name=method.routing_key.split("_")[1]
        #     sensor=Sensor.objects.get(uniq_name=sensor_name)
        #     sensorFdevice=SensorForDevice.objects.get(sensor=sensor,device=device)
        #     sensorFdevice.enable=body.get("status",)

    except Exception as e:
        print(f'<lo: {e.__traceback__.tb_lineno}> error detailed:{e}')
    PMI.connection._channel.basic_ack(method.delivery_tag)
    # client.json().set(json.loads(body))


test1=threading.Thread(name="test" , target=PMI.run ,kwargs={'queue_name':"shire",'routing_keys':["device","sensore","device_sensore"],'callback':callback})


