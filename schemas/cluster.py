from typing import List, Optional
from pydantic import BaseModel, Field


class NodeInfo(BaseModel):
    nodeUuid: str = Field(..., description="ノードのUUID")
    controllerVmIp: str = Field(..., description="CVMのIPv4アドレス")
    hostIp: str = Field(..., description="ホストのIPv4アドレス")


class SoftwareInfo(BaseModel):
    softwareType: str = Field(..., description="ソフトウェアの種類（例: NCC, AOS）")
    version: str = Field(..., description="ソフトウェアのバージョン")


class ClusterSummary(BaseModel):
    extId: str = Field(..., description="クラスタのUUID")
    name: str = Field(..., description="クラスタ名")
    vmCount: int = Field(..., description="VMの総数")
    inefficientVmCount: int = Field(..., description="非効率VMの数")
    numberOfNodes: int = Field(..., description="ノード数")
    nodeList: List[NodeInfo] = Field(..., description="ノードの詳細情報リスト")
    hypervisorTypes: List[str] = Field(..., description="ハイパーバイザーの種類（例: AHV）")
    clusterSoftwareMap: List[SoftwareInfo] = Field(..., description="クラスター内のソフトウェア構成")
    timezone: str = Field(..., description="クラスタのタイムゾーン")
    isLts: bool = Field(..., description="LTSクラスタかどうか")
    redundancyFactor: int = Field(..., description="冗長性係数")
    currentFaultTolerance: str = Field(..., description="現在のフォールトトレランス状態")
    desiredFaultTolerance: str = Field(..., description="期待されるフォールトトレランス状態")
    nameServerIpList: List[str] = Field(..., description="ネームサーバーIPのリスト")
    ntpServerFqdns: List[str] = Field(..., description="NTPサーバーFQDNのリスト")
    upgradeStatus: str = Field(..., description="アップグレードステータス")


class ClusterListResponse(BaseModel):
    clusters: List[ClusterSummary] = Field(..., description="取得されたクラスタの一覧")