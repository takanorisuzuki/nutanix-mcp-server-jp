import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.cluster_route import router as cluster_router
from api.vm_route import router as vm_router

# ログ設定（プロダクション環境に応じた設定を追加可能）
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# FastAPI の初期化
app = FastAPI(
    title="Nutanix MCP Server",
    version="1.0.0",
    description="MCP サーバーによる Nutanix クラスタ情報管理 API"
)

app.include_router(cluster_router)
app.include_router(vm_router)

# サーバー起動時の各種設定（例: uvicorn 経由で実行）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)