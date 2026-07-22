# disco-bot

Discord Botから始める、個人用AI Agent学習プロジェクト。

「Discord Botを作ること」自体が目的ではなく、Discordを入り口(UI)にして、AIエージェント的な仕組み(Tool Calling・DB・スケジューラなど)を段階的に学びながら構築していくことを目的としている。

詳細な設計思想・ロードマップは [CLAUDE.md](./CLAUDE.md) を参照。

## 構成

```
Discord
  │ (@メンション)
Bot (discord.py)
  │ HTTP
Backend (FastAPI)
  │
  ├─ OpenAI API
  └─ PostgreSQL (SQLAlchemy + Alembic)
```

- **Bot**: Discordとのやり取りのみを担当する薄いクライアント。コマンドは`bot/cogs/`配下にコマンドごとにファイル分割
- **Backend**: 会話・Tool Calling・DB永続化などのロジックを集約。Discordに依存しない設計
- **DB**: 会話履歴・タスクを永続化。スキーマ変更はAlembicで管理

## 現在実装済みの機能

- `/ping`, `/help`
- `@メンション`でのAI会話(会話履歴はチャンネル単位でPostgreSQLに永続化)
- Tool Calling
  - **Task Tool**: 毎日リマインドタスク・締切付きタスクの登録/一覧(重複登録防止あり)
  - **Reminder Tool**: 該当時刻(JST基準)になったら該当チャンネルへ自動通知
  - **News Tool**: APIキー不要な4ソースからニュース取得(AI関連 / IT技術全般 / 英語ニュース / 半導体・シミュレーション論文)
- `messages`テーブルの自動削除(デフォルト30日、`MESSAGE_RETENTION_DAYS`で変更可)

## セットアップ

### 必要な環境変数

`bot/.env`
```
DISCORD_TOKEN=
```

`backend/.env`
```
OPENAI_API_KEY=
```

Discord Developer Portalの対象アプリケーションで、Bot設定の「MESSAGE CONTENT INTENT」を有効にしておく必要がある。

### 起動

```bash
docker compose up -d --build
```

- `bot`: Discord Bot本体
- `backend`: FastAPI(ポート8000で公開、`/health`, `/health/db`で稼働確認可能)
- `db`: PostgreSQL(データは`db_data`ボリュームに永続化)

### DBスキーマを変更した場合

```bash
docker exec ai-agent-backend alembic revision --autogenerate -m "説明"
docker cp ai-agent-backend:/app/alembic/versions/<生成されたファイル名> ./backend/alembic/versions/
docker exec ai-agent-backend alembic upgrade head
```

## 既知の課題 / 今後の予定

- `tasks`テーブルの自動削除は未実装(締切から数日後に削除、など)
- `conversation_id`はDiscordチャンネル単位。ユーザー単位での分離は未対応
- ロードマップの続き([CLAUDE.md](./CLAUDE.md)参照): Phase 6(Scheduler: Redis, APScheduler)以降
