# 麹管理アプリ API

## 概要
米麹作成管理アプリのバックエンドAPI。麹作りのサイクル（3日間）の温度管理と記録を提供します。

## 技術スタック
- AWS Lambda (Python)
- Amazon DynamoDB
- Amazon API Gateway
- Terraform (IaC)

## API エンドポイント

### ユーザー管理
| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| POST | `/users` | 新規ユーザー作成 |
| GET | `/users/{user_id}` | ユーザー情報取得 |

### サイクル管理
| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| POST | `/users/{user_id}/cycles` | 新規サイクル作成 |
| GET | `/users/{user_id}/cycles` | ユーザーのサイクル一覧取得 |
| GET | `/cycles/{cycle_id}` | 特定のサイクル情報取得 |
| PUT | `/cycles/{cycle_id}` | サイクル情報更新 |

### 温度記録
| メソッド | エンドポイント | 説明 |
|----------|----------------|------|
| POST | `/cycles/{cycle_id}/logs` | 温度記録作成 |
| GET | `/cycles/{cycle_id}/logs` | サイクルの温度記録一覧取得 |
| GET | `/cycles/{cycle_id}/stats` | 温度と湿度の統計情報取得 |
| GET | `/cycles/{cycle_id}/latest` | 最新の温度記録取得 |

## リクエスト/レスポンス例

### ユーザー作成
```json
// POST /users
{
  "email": "user@example.com",
  "name": "John Doe"
}

// レスポンス
{
  "message": "User created",
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### サイクル作成
```json
// POST /users/{user_id}/cycles
{
  "start_date": "2024-03-20",
  "end_date": "2024-03-22",
  "status": "active",
  "notes": "春の麹作り"
}

// レスポンス
{
  "message": "Cycle created",
  "cycle_id": "123e4567-e89b-12d3-a456-426614174000"
}
```

### 温度記録作成
```json
// POST /cycles/{cycle_id}/logs
{
  "temperature": 30.5,
  "humidity": 60,
  "time": "10:00",
  "notes": "朝の計測"
}

// レスポンス
{
  "message": "Temperature log created",
  "timestamp": "2024-03-20T10:00:00Z"
}
```

### 温度統計情報取得
```json
// GET /cycles/{cycle_id}/stats
// レスポンス
{
  "temperature": {
    "min": 28.5,
    "max": 32.0,
    "avg": 30.2
  },
  "humidity": {
    "min": 55,
    "max": 65,
    "avg": 60
  },
  "total_logs": 10
}
```


### 主要コンポーネント
- **Lambda関数**: 単一のLambda関数で全てのAPIリクエストを処理
- **DynamoDB**: 単一テーブル設計でデータを管理
- **API Gateway**: HTTP APIを使用した高速なAPIエンドポイント
- **IAM**: Lambda関数の実行権限とDynamoDBアクセス権限を管理

## デプロイ方法

### 前提条件
- AWS CLIがインストールされている
- Terraformがインストールされている
- AWS認証情報が設定されている

### デプロイ手順

1. **Lambdaコードの準備**
```bash
# Lambdaディレクトリに移動
cd lambda

# 依存関係のインストール
pip install -r requirements.txt -t .

# ZIPファイルの作成
zip -r ../handler.zip .
```

2. **Terraformの初期化**
```bash
# プロジェクトルートに移動
cd ..

# Terraformの初期化
terraform init
```

3. **インフラのデプロイ**
```bash
# デプロイの実行
terraform apply
```

### デプロイ後の確認
- API GatewayのエンドポイントURLを確認
- Lambda関数のログを確認
- DynamoDBテーブルの作成を確認

## データモデル

### DynamoDBテーブル設計

#### テーブル名: `koji_data`

##### 1. ユーザー情報
| 属性名 | 型 | 説明 |
|--------|------|------|
| PK | String | `USER#<user_id>` |
| SK | String | `PROFILE#<user_id>` |
| email | String | ユーザーのメールアドレス |
| name | String | ユーザー名 |
| created_at | String | 作成日時（ISO 8601） |

##### 2. サイクル情報
| 属性名 | 型 | 説明 |
|--------|------|------|
| PK | String | `USER#<user_id>` |
| SK | String | `CYCLE#<cycle_id>` |
| start_date | String | 開始日 |
| end_date | String | 終了日 |
| status | String | サイクルの状態 |
| notes | String | メモ |
| created_at | String | 作成日時（ISO 8601） |

##### 3. 温度記録
| 属性名 | 型 | 説明 |
|--------|------|------|
| PK | String | `CYCLE#<cycle_id>` |
| SK | String | `LOG#<timestamp>` |
| temperature | Number | 温度 |
| humidity | Number | 湿度 |
| time | String | 記録時間 |
| notes | String | メモ |
| created_at | String | 作成日時（ISO 8601） |

## エラーハンドリング

### エラーレスポンス形式
```json
{
  "error": "エラーメッセージ"
}
```

### ステータスコード
| コード | 説明 |
|--------|------|
| 200 | リクエスト成功 |
| 400 | 不正なリクエスト（バリデーションエラーなど） |
| 404 | リソースが見つからない |
| 500 | サーバーエラー |

### エラーケース

#### バリデーションエラー
```json
{
  "error": "Missing field: email"
}
```

#### リソース未検出
```json
{
  "error": "User not found"
}
```

#### サーバーエラー
```json
{
  "error": "Internal server error"
}
```

### エラーログ
- エラーはCloudWatch Logsに記録
- エラーメッセージには詳細な情報を含める
- 機密情報はログに含めない

## AWS Lambda Layerの作成方法

AWS Lambda Layerを作成するためには、以下の手順を実行します。

### 1. Dockerイメージのビルド

まず、Dockerfileを使用してLambda Layerをビルドします。以下のコマンドを実行してください。

```bash
docker buildx build --platform linux/amd64 -t lambda-layer-builder .
```

このコマンドは、現在のディレクトリにあるDockerfileを基に、`lambda-layer-builder`という名前のDockerイメージをビルドします。

### 2. Dockerコンテナの作成

次に、ビルドしたイメージから新しいコンテナを作成します。以下のコマンドを実行してください。

```bash
docker create --platform linux/amd64 --name extract-layer lambda-layer-builder
```

このコマンドは、`lambda-layer-builder`イメージを基に`extract-layer`という名前のコンテナを作成します。

### 3. ZIPファイルのコピー

最後に、作成したコンテナからLambda LayerのZIPファイルをホストマシンにコピーします。以下のコマンドを実行してください。

```bash
docker cp extract-layer:/tmp/lambda-layer.zip ./lambda-layer.zip
```

このコマンドは、`extract-layer`コンテナ内の`/tmp/lambda-layer.zip`ファイルをホストマシンのカレントディレクトリにコピーします。

### 4. 使用したコンテナの削除

作業が完了したら、使用したコンテナを削除します。以下のコマンドを実行してください。

```bash
docker rm extract-layer
```

このコマンドは、`extract-layer`という名前のコンテナを削除します。

### 注意事項

- 上記の手順を実行する前に、Dockerがインストールされていることを確認してください。
- 必要に応じて、Dockerfileや依存関係を適切に設定してください。