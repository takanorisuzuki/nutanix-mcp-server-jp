from pydantic import BaseModel, Field
from typing import Optional, List


class DiskInfo(BaseModel):
    deviceBus: Optional[str] = Field(None, description="ディスクのバス種別")
    isCdrom: Optional[bool] = Field(None, description="CD-ROMかどうか")
    sizeBytes: Optional[int] = Field(None, description="ディスクサイズ（バイト）")


class NicInfo(BaseModel):
    subnetName: Optional[str] = Field(None, description="NICが接続されているサブネット名")
    ipAddress: Optional[str] = Field(None, description="NICのIPアドレス")


class VmSummary(BaseModel):
    extId: str = Field(..., description="VMのUUID")
    name: str = Field(..., description="VM名")
    createTime: Optional[str] = Field(None, description="作成日時")
    updateTime: Optional[str] = Field(None, description="更新日時")
    powerState: Optional[str] = Field(None, description="電源状態")
    numSockets: Optional[int] = Field(None, description="ソケット数")
    numCoresPerSocket: Optional[int] = Field(None, description="コア数（ソケットあたり）")
    memorySizeBytes: Optional[int] = Field(None, description="メモリサイズ（バイト）")
    machineType: Optional[str] = Field(None, description="マシンタイプ（例: PC）")
    hardwareClockTimezone: Optional[str] = Field(None, description="ハードウェアクロックのタイムゾーン")
    protectionType: Optional[str] = Field(None, description="保護ポリシー種別（例: NONE）")
    hostId: Optional[str] = Field(None, description="割り当て先ホストのUUID")
    clusterId: Optional[str] = Field(None, description="所属クラスタのUUID")
    diskList: Optional[List[DiskInfo]] = Field(default_factory=list, description="ディスク構成")
    nicList: Optional[List[NicInfo]] = Field(default_factory=list, description="ネットワーク構成")
    vcpu: Optional[int] = Field(None, description="vCPU数（ソケット × コア）")
    memoryGiB: Optional[float] = Field(None, description="メモリ容量（GiB）")