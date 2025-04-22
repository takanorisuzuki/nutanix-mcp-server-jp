from typing import List, Optional, Any, Dict
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
    timezone: Optional[str] = Field(None, description="クラスタのタイムゾーン")
    isLts: Optional[bool] = Field(None, description="LTSクラスタかどうか")
    redundancyFactor: Optional[int] = Field(None, description="冗長性係数")
    currentFaultTolerance: Optional[str] = Field(None, description="現在のフォールトトレランス状態")
    desiredFaultTolerance: Optional[str] = Field(None, description="期待されるフォールトトレランス状態")
    upgradeStatus: Optional[str] = Field(None, description="アップグレードステータス")
    buildInfo: Optional[str] = Field(None, description="ビルド情報")
    clusterFunction: Optional[List[str]] = Field(None, description="クラスタの機能")
    operationMode: Optional[str] = Field(None, description="運用モード")
    isAvailable: Optional[bool] = Field(None, description="利用可能かどうか")
    pulseEnabled: Optional[bool] = Field(None, description="Pulse 通知が有効かどうか")
    externalDataServiceIp: Optional[str] = Field(None, description="外部データサービスのIP")
    smtpEmailAddress: Optional[str] = Field(None, description="SMTP送信元メールアドレス")
    smtpServerFqdn: Optional[str] = Field(None, description="SMTPサーバーのFQDN")


class ClusterListResponse(BaseModel):
    data: List[ClusterSummary] = Field(..., alias="data", description="取得されたクラスタの一覧")

    class Config:
        allow_population_by_field_name = True
