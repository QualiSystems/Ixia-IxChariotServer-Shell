import imp
import sys
import os

install_path = 'C:/IxChariotPython'

sys.path.append(install_path)

webapi = imp.load_source('webapi', os.path.join(install_path, 'ixia/webapi.py'))
ixchariotapi = imp.load_source('ixchariotapi', os.path.join(install_path, 'ixchariotApi.py'))

connection = webapi.webApi.connect('https://ixchariot.corp.airties.com', 'v1', None, 'yoram.s@quali.com',
                                   'Testshell.1234')

session = connection.createSession('ixchariot')

endpoints = session.httpGet("config/ixchariot/resources/endpoint")
for endpoint in endpoints:
    print endpoint.managementIp

session.startSession()

session.loadConfiguration('tcp sample')

a = session.httpGet('config/ixchariot')
if a.appMixes:
    network_url = 'config/ixchariot/appMixes/1/network'
elif a.flowGroups:
    network_url = 'config/ixchariot/flowGroups/1/network'
else:
    network_url = 'config/ixchariot/multicastGroups/1/network/'

ep1 = ixchariotapi.getEndpointFromResourcesLibrary(session, 'Testshell-ChariotPC-1')
ep2 = ixchariotapi.getEndpointFromResourcesLibrary(session, 'Testshell-ChariotPC-2')

session.httpDelete(network_url + 'sourceEndpoints')
session.httpDelete(network_url + 'destinationEndpoints')

session.httpPost(network_url + 'sourceEndpoints', data=ep2)
session.httpPost(network_url + 'destinationEndpoints', data=ep1)

result = session.runTest()

filePath = "c:/temp/testResults.zip"
with open(filePath, "wb+") as statsFile:
    connection.getStatsCsvZipToFile(result.testId, statsFile)
