# disco-bot

Discord Botから始める、個人用AI Agent学習プロジェクト。

「Discord Botを作ること」自体が目的ではなく、Discordを入り口(UI)にして、AIエージェント的な仕組み(Tool Calling・DB・スケジューラ・RAGなど)を段階的に学びながら構築していくことを目的としている。

詳細な設計思想・ロードマップは [CLAUDE.md](./CLAUDE.md) を参照。

## 構成

```
Discord
  │ (@メンション / スラッシュコマンド)
Bot (discord.py)
  │ HTTP
Backend (FastAPI)
  │
  ├─ OpenAI API (Chat / Embeddings)
  └─ PostgreSQL + pgvector (SQLAlchemy + Alembic)
```

- **Bot**: Discordとのやり取りのみを担当する薄いクライアント。コマンドは`bot/cogs/`配下にコマンドごとにファイル分割
- **Backend**: 会話・Tool Calling・DB永続化などのロジックを集約。Discordに依存しない設計
- **DB**: 会話履歴・タスク・長期記憶・RAG用ドキュメントを永続化。スキーマ変更はAlembicで管理

## 現在実装済みの機能

- `/ping`, `/help`
- `@メンション`でのAI会話(会話履歴はチャンネル単位でPostgreSQLに永続化)
- Tool Calling
  - **Task Tool**: 毎日リマインドタスク・締切付きタスクの登録/一覧(重複登録防止あり)
  - **Reminder Tool**: 該当時刻(JST基準)になったら該当チャンネルへ自動通知(Bot側から60秒間隔でbackendをポーリング)
  - **News Tool**: APIキー不要な4ソースからニュース取得(AI関連 / IT技術全般 / 英語ニュース / 半導体・シミュレーション論文)
  - **Memory**: 「覚えておいて」等の発言をベクトル化して長期記憶として保存し、関連する話題が出たときに意味的検索で思い出す(直近の会話履歴の範囲外でも機能する)
  - **RAG(Markdown)**: `backend/rag_documents/`に置いたMarkdownファイルを`/ingest`で取り込み、`@メンション`での会話中に内容を検索して回答に利用できる
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
- `db`: PostgreSQL + pgvector(データは`db_data`ボリュームに永続化)

### DBスキーマを変更した場合

```bash
docker exec ai-agent-backend alembic revision --autogenerate -m "説明"
docker cp ai-agent-backend:/app/alembic/versions/<生成されたファイル名> ./backend/alembic/versions/
docker exec ai-agent-backend alembic upgrade head
```

※ `pgvector`型のカラムを含む場合、自動生成されたマイグレーションファイルに`import pgvector.sqlalchemy`が入っていないことがあるため、手動で追記が必要。

### RAG用ドキュメントの追加

`backend/rag_documents/`にMarkdownファイルを置き、Discordで`/ingest`を実行すると検索対象に反映される。詳細は[backend/rag_documents/README.md](./backend/rag_documents/README.md)を参照。

## 既知の課題 / 今後の予定

- `tasks`テーブルの自動削除は未実装(締切から数日後に削除、など)
- `memories`の重複保存防止は未実装(同じ内容を繰り返し覚えさせると重複して保存される)
- `conversation_id`はDiscordチャンネル単位。ユーザー単位での分離は未対応
- RAGはMarkdownのみ対応。PDF/Obsidian/Notionは未対応
- Phase 6(Scheduler: Redis, APScheduler)は未着手。現状はBot側の簡易ポーリングでリマインドを実現している
- Phase 9(MCP)は保留中。複数プロジェクトのログ監視をDiscordから確認できるようにする用途で、後日着手予定
