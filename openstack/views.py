from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from .serializer import ChurmHubSerializer
from .models import ChurmHub
from django.http import HttpResponse
import json 
from django.shortcuts import render
#JUJU-packeges
from juju.controller import Controller
from juju.model import Model
from juju.application import Application
from juju.charmstore import CharmStore
import asyncio
import os
import subprocess
source_data=[]
data_js={}
token = '1d3197820f949a00e726c70feb77d40c98523be2'
#-----------DataBase model for churmHub------#
class ChurmHubViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = ChurmHub.objects.all()
    serializer_class = ChurmHubSerializer
    permission_classes = [IsAuthenticated]

    def permissions(self, request):
        queryset = self.get_queryset()
        serializer = ChurmHubSerializer(queryset, many=True)
        content = JSONRenderer().render(serializer.data)
        print("CONTENT-DATA-SERIALIZER", content)
        return Response(serializer.data)
#-----------DataBase model for churmHub------#
      
"""
The index function is created to accept http requests
and is distributed by commands,
each command calls a separate function.

Функция индекс создан для принятия http запросов
и распределение по командам,
каждая команда вызывает отдельную функцию.

Requests arrive in the form of a json file,
which specifies the key-value,
which are passed as a parameter for the function.

Запросы прилетает в виде json файла,
в котором указаны ключ-значение,
которые передаются как параметр для функции. 
"""
def index(request):
    if request.method == 'GET': 
        if request.headers['Token'] == token:
            print("DATA-TOKEN-ACCEPTED")
            # print(ChurmHub.objects.filter(series='jammy'))  
            return HttpResponse('Paas Service')
        else:
            return HttpResponse('FAIL-LOAD')
    elif request.method == 'POST':
        my_json = request.body.decode('utf8').replace("'", '"') 
        global data_js
        global source_data
        data_js = json.loads(my_json)
        if data_js['COMMAND']=='controll_data':
            asyncio.run(controller_mode(data_js=data_js))
        elif data_js['COMMAND'] == 'create_controller':
            asyncio.run(create_controller(data_js=data_js))
        elif data_js['COMMAND']=='deploy_action':
            asyncio.run(deploy_mode(data_js=data_js))
        elif data_js['COMMAND']=='remove_action':
            asyncio.run(remove_mode(data_js=data_js))
        elif data_js['COMMAND']=='releation_create':
            asyncio.run(releation_create(data_js=data_js))
        elif data_js['COMMAND']=='releation_remove':
            asyncio.run(releation_remove(data_js=data_js))
        elif data_js['COMMAND']=='application_data':
            asyncio.run(application_data(data_js=data_js))
        elif data_js['COMMAND']=='remove_model_and_add_model':
            asyncio.run(remove_model_and_add_model(data_js=data_js))
        else:
            return HttpResponse('ERROR, PLEASE TRY AGAING REQUEST')
        return HttpResponse(json.dumps(source_data))

"""
Model mode function:
Function connected whit model, principe DRY
"""


async def controller_mode(data_js):
    global source_data
    controller = Controller()
    await controller.connect(data_js['controller_name'])
    print(await controller.model_uuids())
    source_data = await controller.model_uuids()


async def remove_model_and_add_model(data_js):
    global source_data
    controller = Controller()
    await controller.connect(data_js['controller_name'])
    # await controller.destroy_models('default')
    # await controller.destroy_models('controller')
    await controller.add_model(
        model_name= data_js['model_name'],

    )
    source_data = await controller.list_models()

async def create_controller(data_js):
    os.system('sudo snap install juju --classic')
    print("start-1")
    os.system('juju add-cloud --client -f maas-cloud.yaml maas1')
    print("start-2")
    os.system('juju add-credential --client -f maas-creds.yaml maas1')
    print("start-3")
    #tags указать машинку, потом облако, потом название!!!!
    os.system('juju bootstrap --config default-space=juju --config juju-ha-space=juju --config juju-mgmt-space=juju --config ssl-hostname-verification=false --bootstrap-series=jammy --constraints tags=testdb maas1 '+ str(data_js['controller_name']) +' --show-log --debug')
    
async def deploy_mode(data_js):
    global source_data
    model = Model()
    await model.connect(data_js['model_name'])
    await model.deploy(
        entity_url=data_js['entity_url'],
        application_name=data_js['application_name'],
        series=data_js['series'],
        channel=data_js['channel'],
        constraints={
            'tags': [data_js['constraints']]
        },
        num_units=data_js['num_units'],
    )
    app = Application(model=model, entity_id=data_js['entity_url'])
    source_data = app.status
    print(source_data)

async def remove_mode(data_js):
    global source_data
    model = Model()
    await model.connect(data_js['model_name'])
    await model.remove_application(
        app_name=data_js['application_name'],
        force=True
    )
    source_data = model.state
    print(source_data)

async def releation_create(data_js):
    model = Model()
    await model.connect(data_js['model_name'])
    global source_data
    await model.add_relation(data_js['relation_name1'], data_js['relation_name2'])
    app = Application(model=model, entity_id=data_js['entity_url'])
    source_data = app.status
    print(source_data)

async def releation_remove(data_js):
    model = Model()
    await model.connect(data_js['model_name'])
    global source_data
    app = Application(model=model, entity_id=data_js['entity_url'])
    app.remove_relation(local_relation=data_js['relation_name1'], remote_relation=data_js['relation_name2'])
    source_data = app.status
    print(source_data)

async def application_data(data_js):
    global source_data
    model = Model()
    await model.connect(data_js['model_name'])
    app = Application(model=model, entity_id=data_js['entity_url'])
    source_data = app.status
    print(app.status_message)

