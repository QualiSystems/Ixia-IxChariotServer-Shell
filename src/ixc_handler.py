"""
IxChariot server (==chassis) shell driver implementation for Auto-load only.

@author: yoram-s@qualisystems.com
"""

import imp
import sys
import os

from cloudshell.shell.core.driver_context import AutoLoadDetails, AutoLoadResource, AutoLoadAttribute
from cloudshell.shell.core.session.cloudshell_session import CloudShellSessionContext


class IxcHandler(object):

    def initialize(self, context, logger):

        self.logger = logger

        address = context.resource.address
        username = context.resource.attributes['User']
        encripted_password = context.resource.attributes['Password']
        password = CloudShellSessionContext(context).get_api().DecryptPassword(encripted_password).Value
        client_install_path = context.resource.attributes['Client Install Path']

        sys.path.append(client_install_path)
        webapi = imp.load_source('webapi', os.path.join(client_install_path, 'ixia/webapi.py'))
        self.ixchariotapi = imp.load_source('ixchariotapi', os.path.join(client_install_path, 'ixchariotApi.py'))

        self.connection = webapi.webApi.connect('https://' + address, 'v1', None, username, password)

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """

        self.attributes = []
        self.resources = []
        session = self.connection.createSession('ixchariot')
        session.startSession()
        self._get_server(session)

        return AutoLoadDetails(self.resources, self.attributes)

    def _get_server(self, session):
        """ Get server resource and attributes. """

        self.attributes.append(AutoLoadAttribute(relative_address='',
                                                 attribute_name='Vendor',
                                                 attribute_value='Ixia'))

        endpoints = session.parentConvention.httpGet("ixchariot/resources/endpoint")
        for endpoint in endpoints:
            self.logger.info('endpoint = {}'.format(endpoint))
            self._get_endpoint(endpoint)

    def _get_endpoint(self, endpoint):
        """ Get module resource and attributes. """

        relative_address = 'EP' + endpoint.managementIp.address
        self.resources.append(AutoLoadResource(model='IxChariot Endpoint',
                                               name=endpoint.name,
                                               relative_address=relative_address))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='OS Version',
                                                 attribute_value=endpoint.operatingSystem))
        for test_ip in endpoint.ips:
            self.logger.info('test IP = {}'.format(test_ip))
            self._get_test_ip(relative_address, test_ip)

    def _get_test_ip(self, endpoint, test_ip):
        """ Get port group resource and attributes. """

        relative_address = endpoint + '/' + test_ip.address
        self.resources.append(AutoLoadResource(model='Traffic Generator Test IP',
                                               name=test_ip.address.replace(':', '-'),
                                               relative_address=relative_address))
        self.attributes.append(AutoLoadAttribute(relative_address=relative_address,
                                                 attribute_name='Abstraction Selector',
                                                 attribute_value=test_ip.address.replace(':', '-')))
