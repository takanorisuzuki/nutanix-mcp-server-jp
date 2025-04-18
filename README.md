# nutanix-mcp-server
> Nutanix Prism Central と連携してクラスタ・仮想マシン情報を取得する MCP (Model Context Protocol) サーバーの FastAPI 実装

## 概要

本プロジェクトは、Nutanix環境を対象とした Model Context Protocol (MCP) サーバーの Minimum Viable Product (MVP) を実装するものです。主な目的は、FastAPI を利用して Nutanix Prism Central からクラスタ情報を取得することにあり、本 MVP は将来的な機能拡張（追加の情報取得、モデル操作、セキュリティ強化など）の基盤となります。
プロトタイプのため本番環境では利用しないでください。

## 動作環境

- OS: macOS, Linux, Windows（WSL2含む）
- Python: 3.12 以上推奨
- pip: 23.x 以上推奨
- Nutanix Prism Central API バージョン: v4.0.2（Cluster Management API）
- Nutanix Prism Central API バージョン: v4.0（Virtual Machine Management API）

## 使い方

### セットアップ手順

```bash
# リポジトリをクローン
git clone https://github.com/takanorisuzuki/nutanix-mcp-server-jp.git
cd nutanix-mcp-server-jp

# 仮想環境を作成・有効化（任意）
python3 -m venv venv
source venv/bin/activate  # Windows の場合は venv\Scripts\activate

# 依存パッケージをインストール
pip install -r requirements.txt

# .env ファイルを作成
cp .env.example .env
```

## .env ファイルの書き方

以下のように `.env` ファイルを作成し、認証情報や接続情報を定義します。

```dotenv
PRISM_CENTRAL_IP=192.168.10.11
PRISM_CENTRAL_PORT=9440
PRISM_CENTRAL_USERNAME=admin
PRISM_CENTRAL_PASSWORD=your_password_here
# VERIFY_SSL="false"
```

> `.env` ファイルはプロジェクトルートに配置してください。`.gitignore` によりコミット対象から除外されます。

- **SSL 検証について**：
  現在、自己署名証明書に対応するため、証明書検証を無効（`verify=False`）にしています。運用環境では、適切な SSL 検証を実施してください。
  `.env` 内の値はすべて文字列として扱われます。`VERIFY_SSL` を使用する際は `"false"` のようにクオートで囲むか、コード側で文字列をブール型に変換する処理が必要です。

### サーバーの起動

uvicorn を使用してMCPサーバーを起動します：

```bash
uvicorn app:app --reload
```

MCPサーバーは `http://127.0.0.1:8000` で起動します。

### API エンドポイントの確認

- **Swagger UI**： ブラウザで `http://127.0.0.1:8000/docs` にアクセスすると、API ドキュメントを確認・テストできます。
- **curl を利用して確認**：
  - `/clusters`: Nutanix クラスタの基本情報（UUID、クラスタ名、ノード構成など）を返します。
  - `/vms`: Prism Central 上の仮想マシン情報（名前、vCPU、メモリ構成など）を返します。

  ```bash
  curl -v http://127.0.0.1:8000/clusters
  curl -v http://127.0.0.1:8000/vms
  ```

### Dify 連携について

本リポジトリには、Dify のカスタムツールとして MCP サーバーを登録するための OpenAPI スキーマファイル `dify-openapi-schema.json` が含まれています。

Dify 上でこのスキーマを使ってカスタムツールを登録し、エージェントにそのツールを割り当てることで、自然言語で Nutanix クラスタ情報や仮想マシン情報を取得・確認することができます。

1. Dify の管理画面で「ツール」>「カスタムツール」から`Nutanix MCP Server`を作成します。
2. `dify-openapi-schema.json` で定義されているスキーマを貼り付けます。
3. 利用可能なツールに`getClusters`と`getVms`が表示され、テストが正常に動くことを確認します。
4. 新しいエージェントを作成し、ツールとして MCP サーバーを登録したカスタムツールを指定します。
5. エージェント画面で「クラスタの情報を教えて」など自然言語で問いかけると、MCP サーバーに問い合わせて結果を返してくれます。

> **接続アドレスについて**：
> Dify を Podman 上で動作させている場合、dify-openapi-schema.jsonを変更せずにMCP サーバーのアドレスとして `http://host.containers.internal:8000` を利用可能です。  
> Docker など他の環境では `http://host.docker.internal:8000`など適切なホスト名・IP アドレスに読み替えてください。

## 更新履歴

- **2025-04-18**: バージョン `v0.1.0` 初期リリース。
  - `/clusters` および `/vms` エンドポイントを実装。
  - Nutanix Prism Central との連携。
  - FastAPI による REST API サーバー。
  - `.env` による認証情報および接続先の外部化。
  - OpenAPI スキーマを Dify 連携用に対応。

## 貢献方法

貢献は大歓迎です。機能改善やバグ修正について Pull Request を送信してください。大きな変更を行う前には、まず Issue を立てて議論してください。

## ライセンス

本プロジェクトは LICENSE ファイルに記載の条件の下でライセンスされています。

## 将来の拡張予定

- 仮想マシンの詳細情報（NIC / ディスク構成）の追加
- クラスタ単体の詳細表示エンドポイントの実装
- Nutanix API vmm の統合による操作系 API の導入（仮想マシンの起動/停止など）
- Dify からの対話操作支援