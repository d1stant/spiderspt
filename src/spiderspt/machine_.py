from hashlib import md5

import wmi


class MachineCode:
    def __init__(self) -> None:
        self.connect_wmi = wmi.WMI()

    def get_cpu_info(self) -> str:
        cpu_infos: list = self.connect_wmi.Win32_Processor()
        cpu_info: str = "-".join(
            [i.ProcessorId.strip() for i in cpu_infos if i.ProcessorId]
        )
        return cpu_info

    def get_baseboard_info(self) -> str:
        baseboard_infos: list = self.connect_wmi.Win32_BaseBoard()
        baseboard_info: str = "-".join(
            [i.SerialNumber.strip() for i in baseboard_infos if i.SerialNumber]
        )
        return baseboard_info

    def get_disk_info(self) -> str:
        disk_infos: list = self.connect_wmi.Win32_DiskDrive()
        disk_info: str = "-".join(
            [i.SerialNumber.strip() for i in disk_infos if i.SerialNumber]
        )
        return disk_info

    def get_network_info(self) -> str:
        network_infos: list = self.connect_wmi.Win32_NetworkAdapter()
        network_info: str = "-".join(
            [i.MACAddress.strip() for i in network_infos if i.MACAddress]
        )
        return network_info

    def generate_machine_code(self) -> str:
        machine_info: str = ";".join(
            [
                self.get_cpu_info(),
                self.get_baseboard_info(),
                self.get_disk_info(),
                self.get_network_info(),
            ]
        )
        machine_code: str = md5(machine_info.encode("utf-8")).hexdigest().upper()
        return machine_code
