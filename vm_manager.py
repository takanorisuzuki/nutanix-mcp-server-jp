import requests
from requests.auth import HTTPBasicAuth
from utils.env_loader import (
    NUTANIX_PC_IP,
    NUTANIX_PC_PORT,
    NUTANIX_PC_USERNAME,
    NUTANIX_PC_PASSWORD,
)
import urllib3
from typing import List
from schemas.vm import VmSummary, DiskInfo, NicInfo

 

VM_API_ENDPOINT = f"https://{NUTANIX_PC_IP}:{NUTANIX_PC_PORT}/api/vmm/v4.0/ahv/config/vms"

def get_vm_list():
    """
    Prism Central から仮想マシン一覧を取得する関数。
    """
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(
            VM_API_ENDPOINT,
            auth=HTTPBasicAuth(NUTANIX_PC_USERNAME, NUTANIX_PC_PASSWORD),
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"VM取得リクエストに失敗しました: {e}")


def format_vm_info(info: dict) -> List[VmSummary]:
    """
    Nutanix APIのレスポンスからVM情報を整形し、VmSummaryのリストを返す。
    """
    vms = []
    for vm in info.get("data", []):
        disks = [
            DiskInfo(
                deviceBus=disk.get("deviceBus"),
                isCdrom=disk.get("isCdrom"),
                sizeBytes=disk.get("diskSizeBytes")
            )
            for disk in vm.get("diskList", [])
        ]

        nics = [
            NicInfo(
                subnetName=nic.get("subnet", {}).get("name"),
                ipAddress=nic.get("ipAddress", {}).get("ip")
            )
            for nic in vm.get("nicList", [])
        ]

        num_sockets = vm.get("numSockets")
        num_cores = vm.get("numCoresPerSocket")
        mem_bytes = vm.get("memorySizeBytes")
        vcpu = num_sockets * num_cores if num_sockets and num_cores else None
        memory_gib = round(mem_bytes / (1024 ** 3), 1) if mem_bytes else None

        vms.append(VmSummary(
            extId=vm.get("extId"),
            name=vm.get("name"),
            createTime=vm.get("createTime"),
            updateTime=vm.get("updateTime"),
            powerState=vm.get("powerState"),
            numSockets=vm.get("numSockets"),
            numCoresPerSocket=vm.get("numCoresPerSocket"),
            memorySizeBytes=vm.get("memorySizeBytes"),
            machineType=vm.get("machineType"),
            hardwareClockTimezone=vm.get("hardwareClockTimezone"),
            protectionType=vm.get("protectionType"),
            hostId=vm.get("host", {}).get("extId"),
            clusterId=vm.get("cluster", {}).get("extId"),
            diskList=disks,
            nicList=nics,
            vcpu=vcpu,
            memoryGiB=memory_gib
        ))
    return vms