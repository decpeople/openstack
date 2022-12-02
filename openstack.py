import asyncio
from juju.controller import Controller
from juju.model import Model
from juju.unit import Unit
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

async def controller_mode():
    print('START-CONTROLLER-SYSTEM')
    controller = Controller()
    await controller.connect(endpoint=data_list['endpoint_test_version'],
                             username=data_list['username_test_version'],
                             password=data_list['password_test_version'],
                             cacert=data_list['cert_test_version']
                             )
    print("LIST-MODELS:?>", await controller.list_models())


async def model_mode():
    model = Model()

    print("START-MODEL-INFO")
    await model.connect(endpoint=data_list['endpoint_test_version'],
                        uuid=data_list['uuid_test_version'],
                        username=data_list['username_test_version'],
                        password=data_list['password_test_version'],
                        cacert=data_list['cert_test_version']
    )
    print("FINISH", model.info)


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
        channel='8.0/stable', # указывать если нужна точная версия
        constraints={
            'tags': ['testdb']
        },
    )
    await model.deploy(
        entity_url='keystone',
        application_name='keystone',
        series='jammy',
        channel='yoga/stable', # указывать если нужна точная версия
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

asyncio.run(controller_mode(), debug=True)
asyncio.run(model_mode(), debug=True)