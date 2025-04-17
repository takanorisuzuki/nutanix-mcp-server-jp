import requests
from requests.auth import HTTPBasicAuth
import urllib3
from utils.env_loader import (
    NUTANIX_PC_IP,
    NUTANIX_PC_PORT,
    NUTANIX_PC_USERNAME,
    NUTANIX_PC_PASSWORD
)

API_ENDPOINT = f"https://{NUTANIX_PC_IP}:{NUTANIX_PC_PORT}/api/clustermgmt/v4.0/config/clusters"

def get_cluster_info():
    """
    Prism Central からクラスタ情報を取得する関数（v4 API）。
    """
    try:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(
            API_ENDPOINT,
            auth=HTTPBasicAuth(NUTANIX_PC_USERNAME, NUTANIX_PC_PASSWORD),
            verify=False,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Nutanix APIリクエストに失敗しました: {e}")

def format_cluster_info(info):
    """
    v4 API のレスポンスから、各クラスタの要約情報をリストで返します。
    """
    data = info.get("data", [])
    if not data:
        return []

    formatted_clusters = []

    for cluster in data:
        config = cluster.get("config", {})
        nodes_obj = cluster.get("nodes", {})
        network = cluster.get("network", {})

        node_list = []
        for node in nodes_obj.get("nodeList", []):
            node_list.append({
                "nodeUuid": node.get("nodeUuid"),
                "controllerVmIp": node.get("controllerVmIp", {}).get("ipv4", {}).get("value"),
                "hostIp": node.get("hostIp", {}).get("ipv4", {}).get("value") or "",
            })

        software_map = []
        for sw in config.get("clusterSoftwareMap", []):
            software_map.append({
                "softwareType": sw.get("softwareType"),
                "version": sw.get("version")
            })

        ns_ips = [ns.get("ipv4", {}).get("value") for ns in network.get("nameServerIpList", []) if "ipv4" in ns]
        ntp_fqdns = [ntp.get("fqdn", {}).get("value") for ntp in network.get("ntpServerIpList", []) if "fqdn" in ntp]

        formatted = {
            "extId": cluster.get("extId"),
            "name": cluster.get("name"),
            "vmCount": cluster.get("vmCount") or 0,
            "inefficientVmCount": cluster.get("inefficientVmCount") or 0,
            "numberOfNodes": nodes_obj.get("numberOfNodes"),
            "nodeList": node_list,
            "hypervisorTypes": config.get("hypervisorTypes", []),
            "clusterSoftwareMap": software_map,
            "timezone": config.get("timezone"),
            "isLts": config.get("isLts"),
            "redundancyFactor": config.get("redundancyFactor"),
            "currentFaultTolerance": config.get("faultToleranceState", {}).get("currentClusterFaultTolerance"),
            "desiredFaultTolerance": config.get("faultToleranceState", {}).get("desiredClusterFaultTolerance"),
            "nameServerIpList": ns_ips,
            "ntpServerFqdns": ntp_fqdns,
            "upgradeStatus": cluster.get("upgradeStatus") or "",
            "buildInfo": config.get("buildInfo", {}).get("fullVersion"),
            "clusterFunction": config.get("clusterFunction"),
            "operationMode": config.get("operationMode"),
            "isAvailable": config.get("isAvailable"),
            "pulseEnabled": config.get("pulseStatus", {}).get("isEnabled"),
            "externalDataServiceIp": network.get("externalDataServiceIp", {}).get("ipv4", {}).get("value"),
            "smtpEmailAddress": network.get("smtpServer", {}).get("emailAddress"),
            "smtpServerFqdn": network.get("smtpServer", {}).get("server", {}).get("ipAddress", {}).get("fqdn", {}).get("value")
        }

        formatted_clusters.append(formatted)

    return formatted_clusters