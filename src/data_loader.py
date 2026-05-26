"""データ読込モジュール"""
from pathlib import Path
import pandas as pd
import numpy as np


def load_sample_data(path: str | Path | None = None) -> pd.DataFrame:
    """サンプルECデータを読み込む（ファイルがなければ生成）"""
    if path is None:
        path = Path(__file__).parent / "sample_data.csv"
    path = Path(path)

    if not path.exists():
        df = generate_sample_data()
        df.to_csv(path, index=False)
        return df

    df = pd.read_csv(path)
    df["注文日"] = pd.to_datetime(df["注文日"])
    return df


def generate_sample_data(n_orders: int = 1000) -> pd.DataFrame:
    """再現可能なサンプルECデータを生成"""
    rng = np.random.default_rng(seed=42)
    categories = ["食品", "家電", "アパレル", "書籍", "雑貨"]
    products = {
        "食品": ["お米", "コーヒー豆", "オリーブオイル", "チョコレート"],
        "家電": ["イヤホン", "炊飯器", "ロボット掃除機", "スマートスピーカー"],
        "アパレル": ["Tシャツ", "ジーンズ", "スニーカー", "ジャケット"],
        "書籍": ["技術書", "小説", "ビジネス書", "雑誌"],
        "雑貨": ["マグカップ", "ノート", "観葉植物", "アロマキャンドル"],
    }
    price_range = {"食品": (500, 5000), "家電": (3000, 50000), "アパレル": (2000, 20000), "書籍": (800, 4000), "雑貨": (500, 8000)}

    dates = pd.date_range(start="2025-01-01", end="2026-05-22", freq="D")
    rows = []
    for _ in range(n_orders):
        date = rng.choice(dates)
        category = rng.choice(categories)
        product = rng.choice(products[category])
        low, high = price_range[category]
        unit_price = int(rng.uniform(low, high))
        quantity = int(rng.integers(1, 5))
        rows.append({
            "注文日": pd.Timestamp(date),
            "注文ID": f"O{len(rows) + 1:06d}",
            "カテゴリ": category,
            "商品名": product,
            "単価": unit_price,
            "数量": quantity,
            "売上金額": unit_price * quantity,
        })
    return pd.DataFrame(rows).sort_values("注文日").reset_index(drop=True)
