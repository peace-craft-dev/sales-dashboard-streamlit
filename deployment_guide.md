# デプロイガイド: Streamlit 売上ダッシュボード

> ユーザー（取締役会）作業手順
> 推定所要時間: 30分

---

## Step 1: ローカル動作確認

```bash
cd sample_4_dashboard
pip install -r requirements.txt
streamlit run src/streamlit_app.py
# → http://localhost:8501 で確認
```

初回起動時に `sample_data.csv` が自動生成されます。

## Step 2: Streamlit Community Cloud デプロイ（推奨・無料）

### 2.1 GitHub にプッシュ
```bash
git init
git add .
git commit -m "Initial commit: Streamlit sales dashboard"
gh repo create PeaceCraft/sample-dashboard --public --source=. --push
```

### 2.2 Streamlit Cloud にデプロイ
1. [Streamlit Community Cloud](https://share.streamlit.io/) にログイン（GitHub連携）
2. 「New app」→ GitHub リポジトリを選択
3. Main file path: `src/streamlit_app.py`
4. Deploy

数分で公開 URL が発行（例: `https://peacecraft-sample-dashboard.streamlit.app`）

## Step 3: テスト実行

```bash
pytest tests/ -v
```

## Step 4: スクリーンショット撮影

撮影スクリーン:
1. ダッシュボード全体（KPI + グラフ複数）
2. 売上推移グラフ（日次・月次タブ）
3. カテゴリ別円グラフ
4. 商品ランキング表
5. フィルター適用後の動的表示
6. CSV ダウンロードボタン

## Step 5: ポートフォリオ掲載

- スクリーンショット 5-6枚
- デモURL（Streamlit Cloud）
- GitHubリポジトリURL
- 説明文:
  > Streamlit + Plotly でEC売上を多角的に可視化したダッシュボード。日次・月次・カテゴリ別の集計、商品ランキング、フィルタリング、CSVエクスポートを実装。サンプルデータ生成も自動化。

## ランニング費用

- Streamlit Community Cloud: 無料（公開リポジトリ前提）
- プライベートリポジトリで使う場合: 有料プラン or 別ホスティング検討

## カスタマイズ案

実案件向けに以下を変更:
- データソース: Google Sheets API、データベース（PostgreSQL等）、API
- 認証: streamlit-authenticator や Cloudflare Access で保護
- 自動更新: `@st.cache_data(ttl=3600)` でTTL設定
- 追加グラフ: ヒートマップ、サンキー図、地図プロット等

## トラブルシュート

### Q. `streamlit run` でエラー
A. Python バージョン確認（3.10+）、`pip install --upgrade streamlit` を試す

### Q. グラフが表示されない
A. `plotly` のバージョン確認、Pythonキャッシュをクリア

### Q. データが反映されない
A. `@st.cache_data` のため、データ変更後はアプリ再起動

---

**PeaceCraft** — お困りの際はお気軽にお問い合わせください。
