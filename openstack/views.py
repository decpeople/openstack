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
data_list = {
 'endpoint_test_version': '172.16.141.9:17070',
 'uuid_test_version': '56247638-4d43-472c-8da1-311c4693dcb8',
 'username_test_version': 'admin',
 'password_test_version': 'c9834ffc1f2ae481463905ddac8143a2',
 'cert_test_version': "-----BEGIN CERTIFICATE-----\n" \
          "MIIEEjCCAnqgAwIBAgIUHpgnZRsqySsUnZB5TlrzZEuBrUIwDQYJKoZIhvcNAQEL" \
          "BQAwITENMAsGA1UEChMESnVqdTEQMA4GA1UEAxMHanVqdS1jYTAeFw0yMjA1MzAx" \
          "MDM4NTBaFw0zMjA1MzAxMDQzNTBaMCExDTALBgNVBAoTBEp1anUxEDAOBgNVBAMT" \
          "B2p1anUtY2EwggGiMA0GCSqGSIb3DQEBAQUAA4IBjwAwggGKAoIBgQDAFWV9K8ee" \
          "4dJLa4SjX1g6Ao88RnWHaabN/V9hIr7nEDKbC2W4UXGMyq0hGbCtl8IvJCyXu7Rt" \
          "pd3jonLMO9QHAlQFaTrnOFE8ldxUQQRRV3202BpIo9mpcH2kvP6OGPgHbNmllxEt" \
          "dnluTnK7qEr6Wg4k2U/CQGXC2HDT17mPSl9sNIdTvfSdYiA8M36KZr6T12F3cEaV" \
          "NQqhRrLSHtiAstUNf2Qa7UqZYZ/Kr0tg5ULjXmB4pGFpRI6isC0/6t5nWdT+KvKZ" \
          "+xqhSUyoUPXd6c85I71so1gkMfCPTrxEBFV04xiCTxqzoFCPRpH3UnFlf0gAQneB" \
          "RM7sN/IIbMkC/tTqr/t/PZfcWli2ZhhdTZXvfutairWL1Gdz+iVNofJoHUU0ZUsT" \
          "flwBMKtEY9ERzymar+6Ppdcc0VAUxqJuwMzbMRrr9r04v9BGu6P4/aXYJygLnpKd" \
          "1Fa2p6NJmH9tECavisc2E6u/TP+GKjQTHRVZgOnQ3T/eikfef6BYba0CAwEAAaNC" \
          "MEAwDgYDVR0PAQH/BAQDAgKkMA8GA1UdEwEB/wQFMAMBAf8wHQYDVR0OBBYEFACW" \
          "ghT+++8zexWYfAPH/16UBZPdMA0GCSqGSIb3DQEBCwUAA4IBgQBjMtOmhzCgK/pD" \
          "HmOT/SvKUZZPJTtg7zXG2g1KRFyFCTmOPPZVRe7cMb5Ja/a9hUP0myFMccCZ9DXu" \
          "w8Rer6GHOtZ6uO1rhfO6cIHaU0m9F3QArhzwzQA6sVfkFXbPcHkFZ5urbUzA/iWG" \
          "RcfUtohBXLCZwk1nokW5OcMcIB05CX1lpPvjaqOXDWSPqC9mJZVO17hUvvqKrll1" \
          "prDepuCMHBYmw3UuWiCMe5HwJKhHTTg9DZ3Oj5CBahe+EsA5HplvJnrAoor14S0Z" \
          "nHmULulpvMcCojcZ1Mapz9/DKFrhiADA3sBKQ+BspVOfF8PxgPaMVAvWyPc4K2Hc" \
          "F971Gg0m0geImd9C4wgbih7LTDQf9/PTvcx/iOF2Pf7wdt6q48FHkX8InS+5MO73" \
          "ht18kL8mbIeLGg/BK3pPpfdInhs1DZNxRDjb+z48/NMUVjUriNqV8PN1svaNMkJq" \
          "DN2QYiL+UE5ZC8PlH88JQmEJ0P5BAhQplCfBt0rcZgWo3gwgXSg=\n" \
          "-----END CERTIFICATE-----"
}
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
            asyncio.run(controller_mode())
        elif data_js['COMMAND'] == 'create_controller':
            asyncio.run(create_controller())
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
        else:
            return HttpResponse('ERROR, PLEASE TRY AGAING REQUEST')
        return HttpResponse(json.dumps(source_data))

"""
Model mode function:
Function connected whit model, principe DRY
"""
async def model_mode(model):
    model = Model()
    global source_data
    await model.connect(endpoint=data_list['endpoint_test_version'],
                        uuid=data_list['uuid_test_version'],
                        username=data_list['username_test_version'],
                        password=data_list['password_test_version'],
                        cacert=data_list['cert_test_version']
    )
    return model

async def controller_mode():
    global source_data
    controller = Controller()
    await controller.connect(endpoint=data_list['endpoint_test_version'],
                             username=data_list['username_test_version'],
                             password=data_list['password_test_version'],
                             cacert=data_list['cert_test_version']
                             )
    print(await controller.model_uuids())
    source_data = await controller.model_uuids()

async def deploy_mode(data_js):
    model = object
    global source_data
    model = await model_mode(model=model)
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
    model = object
    global source_data
    model = await model_mode(model=model)
    await model.remove_application(
        app_name=data_js['application_name'],
        force=True
    )
    app = Application(model=model, entity_id=data_js['entity_url'])
    source_data = app.status
    print(source_data)

async def releation_create(data_js):
    model = object
    global source_data
    model = await model_mode(model=model)
    await model.add_relation(data_js['relation_name1'], data_js['relation_name2'])
    app = Application(model=model, entity_id=data_js['entity_url'])
    source_data = app.status
    print(source_data)

async def releation_remove(data_js):
    model = object
    global source_data
    model = await model_mode(model=model)
    app = Application(model=model, entity_id=data_js['entity_url'])
    app.remove_relation(local_relation=data_js['relation_name1'], remote_relation=data_js['relation_name2'])
    source_data = app.status
    print(source_data)

async def add_user_controlelr():
    controller = Controller()
    await controller.connect(endpoint=data_list['endpoint_test_version'],
                       username=data_list['username_test_version'],
                       password=data_list['password_test_version'],
                       cacert=data_list['cert_test_version']
    )
    await controller.add_user(
        username='aibar',
        password='Ghjuyjp56',
        display_name='Turar Aiabr'
    )
    global source_data
    source_data = await controller.get_users()
    print(await controller.get_users())

async def application_data(data_js):
    global source_data
    model = object
    model = await model_mode(model=model)
    app = Application(model=model, entity_id=data_js['entity_url'])
    source_data = app.status
    print(app.status_message)

# TODO решить вопрос с моментом ресурса системы 


async def create_controller():
    os.system('sudo snap install juju --classic')
    os.system('nano maas-cloud.yaml')
    os.system('juju add-cloud --client -f maas-cloud.yaml maas1')
    os.system('nano maas-creds.yaml')
    os.system('juju add-credential --client -f maas-creds.yaml maas1')
    os.system('juju bootstrap \
    --config default-space=juju \
    --config juju-ha-space=juju \
    --config juju-mgmt-space=juju \
    --config ssl-hostname-verification=false \
    --bootstrap-series=focal --constraints tags=controller maas1 jujuControllerTestAibar --show-log --debug')

    




