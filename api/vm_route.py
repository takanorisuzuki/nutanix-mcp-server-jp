from fastapi import APIRouter
from typing import List
from schemas.vm import VmSummary
from vm_manager import get_vm_list, format_vm_info

router = APIRouter()

@router.get("/vms", response_model=List[VmSummary], summary="仮想マシンの一覧取得")
async def get_vms():
    raw_data = get_vm_list()
    return format_vm_info(raw_data)
