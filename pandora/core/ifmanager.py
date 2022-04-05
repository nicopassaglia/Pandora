"""Este modulo inicializa la interfaz wifi"""
from time import sleep
from pandora.shell import netinfo, airmon
from pandora.utils.exceptions import InterfaceNotFoundError, InvalidInterfaceModeError
class InterfaceManager():
    def __init__(self):
        self.amon = airmon.Airmon()
        self.interfaces = []
        self.iwconfig = netinfo.Iwconfig()
        self.ifconfig = netinfo.Ifconfig()
        self.update_interfaces()

    def kill_conflicting_processes(self):
        print('Airmon-ng stopping conflicting processes')
        return self.amon.check_kill()

    def update_interfaces(self):
        interfaces = self.ifconfig.get_interfaces()
        for element in interfaces:
            mode = self.iwconfig.get_mode(element.get('iname'))
            element.update({'mode': mode})
        self.interfaces = interfaces

    def get_interfaces(self):
        return self.interfaces

    def get_interface_by_name(self, ifname):
        desired_interface = None
        for interface in self.interfaces:
            if interface.get('iname') == ifname:
                desired_interface = interface

        return desired_interface

    def get_interface(self, mode):
        desired_interface = None
        for interface in self.interfaces:
            if interface.get('mode') == mode:
                desired_interface = interface
        return desired_interface

    def get_amon_interface_by_name(self, ifname):
        """Returns tuple with (phy, ifname)"""
        interfaces_amon = self.amon.get_interfaces()
        for element in interfaces_amon:
            if element[1] == ifname:
                return element

    def get_amon_interface_by_phy(self, phy):
        """Returns tuple with (phy, ifname)"""
        interfaces_amon = self.amon.get_interfaces()
        for element in interfaces_amon:
            if element[0] == phy:
                return element

    def switch_mode(self, ifname, mode):
        if mode != 'Managed' and mode != 'Monitor':
            raise InvalidInterfaceModeError(f"{mode} is an invalid interface mode")
        interface_amon = self.get_amon_interface_by_name(ifname)
        self.ifconfig.ifup(ifname)
        self.update_interfaces()
        interface = self.get_interface_by_name(ifname)
        #If interface was not found raise exception.
        if interface is None or interface_amon is None:
            raise InterfaceNotFoundError(f"Interface {ifname} was not found")
        phy = interface_amon[0]
        print(f"Interface {ifname} in mode {interface.get('mode')}")

        if interface.get('mode') == mode: #If interface is already in mode. Return interface dict. If statement for readability.
            pass
        else: #Else interface is not in mode switch mode and return interface dict.
            self.iwconfig.set_mode(ifname, mode)
            interface_amon = self.get_amon_interface_by_phy(phy)
            self.ifconfig.ifup(interface_amon[1])
            self.update_interfaces()
            interface = self.get_interface_by_name(interface_amon[1])
            if interface.get("mode") != mode:
                self.amon.switch_mode(interface.get("iname"), mode)
                interface_amon = self.get_amon_interface_by_phy(phy)
                self.ifconfig.ifup(interface_amon[1])
                self.update_interfaces()
                interface = self.get_interface_by_name(interface_amon[1])

        name = interface.get('iname')
        print(f"Waiting for interface {name} to get into mode {mode} (max. 40 seconds)")
        waiting_seconds = 0
        while waiting_seconds < 20 and interface.get('mode') != mode:
            sleep(2)
            self.update_interfaces()
            interface = self.get_interface_by_name(interface_amon[1])
            waiting_seconds += 1

        if interface.get("mode") == mode:
            name = interface.get("iname")
            print(f"Interfaz {name} en modo {mode}")
        else:
            print(f"No se pudo pasar interfaz a modo {mode}")
        #interface.update({"phy": interface_amon[0]})
        return interface
