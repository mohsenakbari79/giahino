# Generated by Django 4.0.5 on 2022-07-14 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Devices', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uniq_name', models.CharField(max_length=25)),
            ],
        ),
        migrations.RemoveField(
            model_name='sensorvaluetype',
            name='validation',
        ),
        migrations.AddField(
            model_name='sensorvaluetype',
            name='sort',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sensorvaluetype',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Devices.sensor'),
        ),
        migrations.CreateModel(
            name='TimeEnable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day', models.DateField(blank=True, null=True)),
                ('end_day', models.DateField(blank=True)),
                ('start_time', models.TimeField(blank=True)),
                ('end_time', models.TimeField(blank=True)),
                ('sensorfordevice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_enable', to='Devices.sensorfordevice')),
            ],
        ),
        migrations.CreateModel(
            name='SensorDeviceValidation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('validation', models.JSONField()),
                ('device_sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sensorvalidation', to='Devices.sensorfordevice')),
                ('senortype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Devices.sensorvaluetype')),
            ],
        ),
        migrations.CreateModel(
            name='RelayForDevice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('enable', models.BooleanField(default=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device_relay', to='Devices.device')),
                ('relay', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Devices.relay')),
            ],
            options={
                'unique_together': {('device', 'id')},
            },
        ),
    ]
