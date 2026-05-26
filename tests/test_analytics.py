"""集計ロジックのテスト"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
import pytest
from analytics import calculate_kpis, daily_sales, monthly_sales, category_breakdown, top_products


def make_sample_df():
    return pd.DataFrame({
        "注文日": pd.to_datetime(["2026-01-15", "2026-01-20", "2026-02-10"]),
        "注文ID": ["O1", "O2", "O3"],
        "カテゴリ": ["食品", "家電", "食品"],
        "商品名": ["お米", "イヤホン", "お米"],
        "単価": [3000, 8000, 3000],
        "数量": [1, 1, 2],
        "売上金額": [3000, 8000, 6000],
    })


def test_calculate_kpis():
    df = make_sample_df()
    kpis = calculate_kpis(df)
    assert kpis["売上合計"] == 17000
    assert kpis["注文数"] == 3
    assert kpis["ユニーク商品数"] == 2


def test_calculate_kpis_empty():
    kpis = calculate_kpis(pd.DataFrame())
    assert kpis["売上合計"] == 0
    assert kpis["注文数"] == 0


def test_monthly_sales():
    df = make_sample_df()
    result = monthly_sales(df)
    assert len(result) == 2
    assert result[result["年月"] == "2026-01"]["売上金額"].iloc[0] == 11000


def test_category_breakdown():
    df = make_sample_df()
    result = category_breakdown(df)
    food = result[result["カテゴリ"] == "食品"]
    assert food["売上金額"].iloc[0] == 9000


def test_top_products():
    df = make_sample_df()
    result = top_products(df, n=10)
    rice = result[result["商品名"] == "お米"]
    assert rice["売上金額"].iloc[0] == 9000


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
