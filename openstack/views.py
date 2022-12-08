from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from .serializer import ChurmHubSerializer
from juju.controller import Controller
from django.http import HttpResponse
from rest_framework import viewsets
from django.shortcuts import render 
from juju.model import Model
from .models import ChurmHub
from juju.unit import Unit


import json
import asyncio
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

#------------Data for Juju request-----------#
request_entity_url=''
request_application_name=''
request_series=''
request_num_units=0
request_channel=''
request_name_machine=''
#------------Data for Juju request-----------#



def index(request):
    global request_entity_url
    global request_application_name
    global request_series
    global request_num_units
    global request_channel
    global request_name_machine
    if request.method == 'GET':
        return HttpResponse(data_list)
    elif request.method == 'POST':
        my_json = request.body.decode('utf8').replace("'", '"') 
        data_js = json.loads(my_json)
        for i in data_js:
            print(data_js[i])
            if i == 'entity_url':
                request_entity_url = data_js[i]
            elif i == 'application_name':
                request_application_name = data_js[i]
            elif i =='series':
                request_series = data_js[i]
            elif i == 'channel':
                request_channel=data_js[i]
            elif i == 'constraints':
                request_name_machine=data_js[i]
            elif i == 'num_units':
                request_num_units = data_js[i]
        for i in data_js:
            if i =='COMMAND':
                if data_js[i]=='1':
                    asyncio.run(controller_mode())
                elif data_js[i]=='2':
                    asyncio.run(model_mode())
                elif data_js[i]=='3':
                    asyncio.run(deploy_mode())
                elif data_js[i]=='4':
                    asyncio.run(remove_mode())
        global source_data
        return HttpResponse(source_data)
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
    

async def controller_mode():
    print('START-CONTROLLER-SYSTEM')
    global source_data
    controller = Controller()
    controller.add_credential()
    await controller.connect(endpoint=data_list['endpoint_test_version'],
                             username=data_list['username_test_version'],
                             password=data_list['password_test_version'],
                             cacert=data_list['cert_test_version']
                             )
    print(await controller.list_models())
    source_data = await controller.list_models()

async def model_mode():
    model = Model()
    global source_data
    print("START-MODEL-INFO")
    await model.connect(endpoint=data_list['endpoint_test_version'],
                        uuid=data_list['uuid_test_version'],
                        username=data_list['username_test_version'],
                        password=data_list['password_test_version'],
                        cacert=data_list['cert_test_version']
    )
    source_data = model.info
    print(model.info)

async def deploy_mode():
    model = Model()
    await model.connect(endpoint=data_list['endpoint_test_version'],
                        uuid=data_list['uuid_test_version'],
                        username=data_list['username_test_version'],
                        password=data_list['password_test_version'],
                        cacert=data_list['cert_test_version']
                        )

    await model.deploy(
        entity_url='mysql-innodb-cluster',
        application_name='mysql-innodb-cluster',
        series='jammy',
        num_units=3,
        channel='8.0/stable',
        constraints={
            'tags': ['testdb']
        },
    )
    await model.deploy(
        entity_url='keystone',
        application_name='keystone',
        series='jammy',
        channel='yoga/stable',
        constraints={
            'tags': ['testapp']
        },
    )
    await model.deploy(
        entity_url='mysql-router',
        application_name='keystone-mysql-router',
        series='jammy',
        channel='8.0/stable',
    )

    await model.add_relation('keystone-mysql-router', 'mysql-innodb-cluster')
    await model.add_relation('keystone-mysql-router', 'keystone')
    print("DEPLOY-MODEL-ADD_RELATION-INFO:?>", model.info)


async def remove_mode():
    model = model_mode()
    await model.remove_application(
        app_name='wordpress',
        force=True
    )
    await model.remove_application(
        app_name='mysql',
        force=True
    )

