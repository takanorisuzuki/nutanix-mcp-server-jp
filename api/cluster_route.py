from fastapi import APIRouter
from typing import List
from schemas.cluster import ClusterSummary
from cluster_manager import get_cluster_info, format_cluster_info

router = APIRouter()

@router.get("/clusters", response_model=List[ClusterSummary], summary="クラスタ情報の一覧取得")
async def get_clusters():
    raw_data = get_cluster_info()
    return format_cluster_info(raw_data)
