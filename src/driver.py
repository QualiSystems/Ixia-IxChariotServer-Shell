"""
IxChariot server (==chassis) shell driver for Auto-load only.
This module is an empty shell, actual implementation is in ixc_handle.

@author: yoram-s@qualisystems.com
"""

from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from cloudshell.traffic import tg_helper

from ixc_handler import IxcHandler


class IxChariotServerShell(ResourceDriverInterface):

    def __init__(self):
        self.handler = IxcHandler()

    def initialize(self, context):
        """
        :type context: cloudshell.shell.core.driver_context.InitCommandContext
        """
        self.logger = tg_helper.get_logger(context)
        self.handler.initialize(context, self.logger)

    # Destroy the driver session, this function is called every time a driver instance is destroyed
    # This is a good place to close any open sessions, finish writing to log files
    def cleanup(self):
        pass

    def get_inventory(self, context):
        """ Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return self.handler.get_inventory(context)
