
import sys
import logging

from shellfoundry.releasetools.test_helper import create_autoload_context

from driver import IxChariotServerShell

client_install_path = 'C:/Program Files (x86)/Ixia/IxChariot/webapi-96'
address = '192.168.42.167'
user = 'admin'
password = 'DxTbqlSgAVPmrDLlHvJrsA=='


class TestIxChariotServerDriver():

    def setup(self):
        self.context = create_autoload_context(address=address, client_install_path=client_install_path,
                                               controller='', port='', user=user, password=password)
        self.driver = IxChariotServerShell()
        self.driver.initialize(self.context)
        self.driver.logger.addHandler(logging.StreamHandler(sys.stdout))

    def teardown(self):
        pass

    def test_autoload(self):
        inventory = self.driver.get_inventory(self.context)
        for r in inventory.resources:
            print r.relative_address, r.model, r.name
        for a in inventory.attributes:
            print a.relative_address, a.attribute_name, a.attribute_value
