"""集計・分析モジュール"""
import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """主要KPIを算出"""
    if df.empty:
        return {"売上合計": 0, "注文数": 0, "平均単価": 0, "ユニーク商品数": 0}

    return {
        "売上合計": int(df["売上金額"].sum()),
        "注文数": int(df["注文ID"].nunique()),
        "平均単価": int(df["単価"].mean()),
        "ユニーク商品数": int(df["商品名"].nunique()),
    }


def daily_sales(df: pd.DataFrame) -> pd.DataFrame:
    """日次売上集計"""
    if df.empty:
        return pd.DataFrame(columns=["注文日", "売上金額", "注文数"])
    return (
        df.groupby(df["注文日"].dt.date)
        .agg(売上金額=("売上金額", "sum"), 注文数=("注文ID", "nunique"))
        .reset_index()
        .rename(columns={"注文日": "日付"})
    )


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """月次売上集計"""
    if df.empty:
        return pd.DataFrame(columns=["年月", "売上金額", "注文数"])
    df = df.copy()
    df["年月"] = df["注文日"].dt.strftime("%Y-%m")
    return (
        df.groupby("年月")
        .agg(売上金額=("売上金額", "sum"), 注文数=("注文ID", "nunique"))
        .reset_index()
    )


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """カテゴリ別集計"""
    if df.empty:
        return pd.DataFrame(columns=["カテゴリ", "売上金額", "件数"])
    return (
        df.groupby("カテゴリ")
        .agg(売上金額=("売上金額", "sum"), 件数=("注文ID", "nunique"))
        .reset_index()
        .sort_values("売上金額", ascending=False)
    )


def top_products(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """商品ランキング上位N件"""
    if df.empty:
        return pd.DataFrame(columns=["商品名", "売上金額", "数量"])
    return (
        df.groupby("商品名")
        .agg(売上金額=("売上金額", "sum"), 数量=("数量", "sum"))
        .reset_index()
        .sort_values("売上金額", ascending=False)
        .head(n)
    )
