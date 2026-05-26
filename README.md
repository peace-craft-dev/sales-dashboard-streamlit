# Streamlit 売上ダッシュボード

> Developed by **PeaceCraft** — AI-Native Development
> データ分析・ダッシュボードのサンプル作品

---

## 概要

サンプルECデータを Streamlit で可視化したダッシュボード。
日次・月次の売上推移、カテゴリ別シェア、商品ランキング、トレンド分析を表示します。
Claude/Pandas/Plotly を活用した、典型的なデータダッシュボード構築の見本。

## 機能

- ✅ 売上推移（日次・月次・年次グラフ）
- ✅ カテゴリ別売上構成（円グラフ・棒グラフ）
- ✅ 商品ランキング Top 10
- ✅ 前年同月比 / 前月比トレンド
- ✅ 期間フィルター・カテゴリフィルター
- ✅ KPIカード（売上合計、平均単価、注文数等）
- ✅ CSV ダウンロード機能

## システム要件

- Python 3.10+

## セットアップ

```bash
cd sample_4_dashboard

# 依存パッケージインストール
pip install -r requirements.txt

# 起動
streamlit run src/streamlit_app.py
# → http://localhost:8501
```

## ディレクトリ構造

```
sample_4_dashboard/
├── README.md
├── deployment_guide.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── streamlit_app.py     # メインアプリ
│   ├── data_loader.py       # データ読込
│   ├── analytics.py         # 集計・分析
│   └── sample_data.csv      # サンプルデータ
└── tests/
    └── test_analytics.py
```

## スクリーンショット撮影ポイント

1. ダッシュボード全体（KPIカード + グラフ）
2. 売上推移グラフ拡大
3. カテゴリ別円グラフ
4. 商品ランキング表
5. フィルター適用後の動的表示

---

## ライセンス

MIT License — Developed by PeaceCraft (2026)

---

**PeaceCraft** — AI Native Development で、あなたの業務に平穏を。
