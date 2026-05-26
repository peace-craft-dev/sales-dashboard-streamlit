"""Streamlit 売上ダッシュボード"""
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from data_loader import load_sample_data
from analytics import (
    calculate_kpis,
    daily_sales,
    monthly_sales,
    category_breakdown,
    top_products,
)


st.set_page_config(
    page_title="PeaceCraft 売上ダッシュボード",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    return load_sample_data()


def main():
    st.title("📊 売上ダッシュボード")
    st.caption("Developed by PeaceCraft — AI-Native Development")

    df = load_data()

    # サイドバー: フィルター
    st.sidebar.header("フィルター")
    min_date = df["注文日"].min().date()
    max_date = df["注文日"].max().date()

    date_range = st.sidebar.date_input(
        "期間",
        value=(max_date - timedelta(days=90), max_date),
        min_value=min_date,
        max_value=max_date,
    )

    selected_categories = st.sidebar.multiselect(
        "カテゴリ",
        options=df["カテゴリ"].unique(),
        default=df["カテゴリ"].unique(),
    )

    # フィルター適用
    filtered = df.copy()
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["注文日"].dt.date >= start_date)
            & (filtered["注文日"].dt.date <= end_date)
        ]
    if selected_categories:
        filtered = filtered[filtered["カテゴリ"].isin(selected_categories)]

    # KPI カード
    kpis = calculate_kpis(filtered)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("売上合計", f"¥{kpis['売上合計']:,}")
    col2.metric("注文数", f"{kpis['注文数']:,}件")
    col3.metric("平均単価", f"¥{kpis['平均単価']:,}")
    col4.metric("ユニーク商品数", f"{kpis['ユニーク商品数']}")

    st.markdown("---")

    # 売上推移
    st.subheader("売上推移")
    tab_daily, tab_monthly = st.tabs(["日次", "月次"])
    with tab_daily:
        daily = daily_sales(filtered)
        if not daily.empty:
            fig = px.line(daily, x="日付", y="売上金額", title="日次売上推移")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
    with tab_monthly:
        monthly = monthly_sales(filtered)
        if not monthly.empty:
            fig = px.bar(monthly, x="年月", y="売上金額", title="月次売上推移")
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    # カテゴリ・ランキング
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("カテゴリ別売上構成")
        category = category_breakdown(filtered)
        if not category.empty:
            fig = px.pie(category, names="カテゴリ", values="売上金額", hole=0.4)
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("商品ランキング Top 10")
        ranking = top_products(filtered)
        if not ranking.empty:
            st.dataframe(
                ranking.style.format({"売上金額": "¥{:,}"}),
                use_container_width=True,
                height=400,
            )

    # CSV ダウンロード
    st.markdown("---")
    st.subheader("📥 データダウンロード")
    csv = filtered.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="フィルター適用後のデータを CSV でダウンロード",
        data=csv,
        file_name=f"sales_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

    st.caption("— PeaceCraft (AI-Native Development) —")


if __name__ == "__main__":
    main()
