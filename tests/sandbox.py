import imp

import sys
import os


install_path = 'C:\\IxChariotPython'
webServerAddress = 'https://ixchariot.corp.airties.com'
apiVersion = "v1"

print "Connecting to " + webServerAddress
sys.path.append(install_path)
webapi = imp.load_source('webapi', os.path.join(install_path, 'ixia/webapi.py'))
path = os.path.join(install_path, 'ixchariotApi.py')
ixchariotapi = imp.load_source('ixchariotapi', os.path.join(install_path, 'ixchariotApi.py'))

api = webapi.webApi.connect(webServerAddress, apiVersion, None, 'yoram.s@quali.com',
                                   'Testshell.1234')
session = api.createSession("ixchariot")
print "Created session %s" % session.sessionId

print "Starting the session..."
session.startSession()

try:
    print "Starting the test..."

    resources = session.parentConvention.httpGet("ixchariot/resources/endpoint")

    for i in range(0, len(resources)):
        resource = resources[i]
        print resource.managementIp

except Exception, e:
    print "Error", e

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
    api.getStatsCsvZipToFile(result.testId, statsFile)
