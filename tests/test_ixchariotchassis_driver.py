#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tests for `IxChariotServerDriver.`
"""

import unittest

from cloudshell.shell.core.driver_context import (ConnectivityContext, ResourceContextDetails, InitCommandContext)

from src.ixc_server_handler import IxcHandler

address = 'ixchariot.corp.airties.com'
client_install_path = 'C:/'
user = 'yoram.s@quali.com'
password = 'Testshell.1234'
user = 'fetullah.turkeli@airties.com'
password = '123456789aA.'


class TestIxChariotServerDriver(unittest.TestCase):

    def setUp(self):
        self.connectivity = ConnectivityContext(None, None, None, None)
        self.resource = ResourceContextDetails(None, None, None, None, None, None, None, None, None, None)
        self.resource.address = address
        self.resource.attributes = {'Client Install Path': client_install_path,
                                    'User': user,
                                    'Password': password}
        self.context = InitCommandContext(self.connectivity, self.resource)
        self.handler = IxcHandler()
        self.handler.initialize(self.context)

    def tearDown(self):
        pass

    def testAutoload(self):
        context = InitCommandContext(self.connectivity, self.resource)
        inventory = self.handler.get_inventory(context)
        for r in inventory.resources:
            print r.relative_address, r.model, r.name
        for a in inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
