"""PeaceCraft 売上ダッシュボード — Streamlit 実例デモ"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import timedelta, datetime

from data_loader import load_sample_data
from analytics import (
    calculate_kpis,
    daily_sales,
    monthly_sales,
    category_breakdown,
    top_products,
)


# ── ページ設定 ────────────────────────────────────────────
st.set_page_config(
    page_title="PeaceCraft 売上ダッシュボード｜実例デモ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ── カスタム CSS（プロフェッショナル感を強化）─────────────
st.markdown(
    """
    <style>
    /* メインヘッダー */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #2563eb 100%);
        padding: 28px 32px;
        border-radius: 16px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.18);
    }
    .main-header h1 {
        margin: 0;
        font-size: 28px;
        letter-spacing: 0.01em;
    }
    .main-header p {
        margin: 6px 0 0 0;
        opacity: 0.85;
        font-size: 14px;
    }

    /* KPI カード */
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        border-color: #cbd5e1;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-size: 12px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
    }

    /* サイドバー */
    section[data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }

    /* セクション見出し */
    h2, h3 {
        color: #0f172a;
        font-weight: 700;
        letter-spacing: -0.01em;
    }

    /* フッター */
    .footer {
        margin-top: 60px;
        padding-top: 24px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        color: #64748b;
        font-size: 12px;
    }
    .footer a { color: #2563eb; text-decoration: none; }
    .footer a:hover { text-decoration: underline; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── データ ─────────────────────────────────────────
@st.cache_data
def load_data() -> pd.DataFrame:
    return load_sample_data()


def format_delta(current: float, baseline: float) -> str:
    if baseline == 0:
        return None
    pct = (current - baseline) / baseline * 100
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.1f}%"


def main():
    # ── ヘッダー ────────────────────
    st.markdown(
        """
        <div class="main-header">
            <h1>📊 売上分析ダッシュボード</h1>
            <p>架空 EC データを使った、PeaceCraft 製ダッシュボード実装の <strong>ライブデモ</strong>です。
            実際の案件では御社データに合わせて項目・グラフ・連携先をカスタムします。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    # ── サイドバー: フィルター ────────────────
    with st.sidebar:
        st.markdown("### 🎯 フィルター")

        min_date = df["注文日"].min().date()
        max_date = df["注文日"].max().date()

        period = st.radio(
            "プリセット期間",
            ["過去 30 日", "過去 90 日", "過去 180 日", "全期間", "カスタム"],
            index=1,
        )

        if period == "カスタム":
            date_range = st.date_input(
                "期間（任意）",
                value=(max_date - timedelta(days=90), max_date),
                min_value=min_date,
                max_value=max_date,
            )
        else:
            days_map = {"過去 30 日": 30, "過去 90 日": 90, "過去 180 日": 180}
            if period == "全期間":
                date_range = (min_date, max_date)
            else:
                date_range = (max_date - timedelta(days=days_map[period]), max_date)

        selected_categories = st.multiselect(
            "カテゴリ",
            options=sorted(df["カテゴリ"].unique()),
            default=sorted(df["カテゴリ"].unique()),
        )

        st.markdown("---")
        st.markdown(
            """
            <div style="font-size: 12px; color: #64748b; line-height: 1.6;">
            <strong>このデモについて</strong><br>
            PeaceCraft が構築するデータダッシュボード実装の標準形をライブで体験できます。
            データソースは Google Sheets / Excel / PostgreSQL / API 等に切替可能。
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── フィルター適用 ────────────────
    filtered = df.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["注文日"].dt.date >= start_date)
            & (filtered["注文日"].dt.date <= end_date)
        ]
    if selected_categories:
        filtered = filtered[filtered["カテゴリ"].isin(selected_categories)]

    if filtered.empty:
        st.warning("選択条件に該当するデータがありません。フィルターを変更してください。")
        st.stop()

    # 前期間（比較用）
    period_days = (filtered["注文日"].max() - filtered["注文日"].min()).days + 1
    prev_end = filtered["注文日"].min() - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=period_days - 1)
    prev = df[(df["注文日"] >= prev_start) & (df["注文日"] <= prev_end)]
    if selected_categories:
        prev = prev[prev["カテゴリ"].isin(selected_categories)]

    # ── KPI ────────────────────
    kpis = calculate_kpis(filtered)
    prev_kpis = calculate_kpis(prev) if not prev.empty else None

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "売上合計",
        f"¥{kpis['売上合計']:,}",
        delta=format_delta(kpis["売上合計"], prev_kpis["売上合計"]) if prev_kpis else None,
    )
    col2.metric(
        "注文数",
        f"{kpis['注文数']:,} 件",
        delta=format_delta(kpis["注文数"], prev_kpis["注文数"]) if prev_kpis else None,
    )
    col3.metric(
        "平均単価",
        f"¥{kpis['平均単価']:,}",
        delta=format_delta(kpis["平均単価"], prev_kpis["平均単価"]) if prev_kpis else None,
    )
    col4.metric(
        "ユニーク商品数",
        f"{kpis['ユニーク商品数']}",
    )

    st.markdown("")

    # ── 売上推移 ─────────────────────
    st.subheader("売上推移")

    tab_daily, tab_monthly = st.tabs(["📈 日次", "📊 月次"])

    with tab_daily:
        daily = daily_sales(filtered)
        if not daily.empty:
            fig = px.line(
                daily,
                x="日付",
                y="売上金額",
                markers=True,
                color_discrete_sequence=["#2563eb"],
            )
            fig.update_traces(line=dict(width=2.5), marker=dict(size=5))
            fig.update_layout(
                height=380,
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                xaxis=dict(showgrid=False, color="#64748b"),
                yaxis=dict(gridcolor="#e2e8f0", color="#64748b", tickformat=",.0f"),
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab_monthly:
        monthly = monthly_sales(filtered)
        if not monthly.empty:
            fig = px.bar(
                monthly,
                x="年月",
                y="売上金額",
                color_discrete_sequence=["#2563eb"],
            )
            fig.update_traces(marker_line_width=0)
            fig.update_layout(
                height=380,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                xaxis=dict(showgrid=False, color="#64748b"),
                yaxis=dict(gridcolor="#e2e8f0", color="#64748b", tickformat=",.0f"),
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ── カテゴリ / ランキング ─────────────
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("カテゴリ別売上")
        category = category_breakdown(filtered)
        if not category.empty:
            fig = px.pie(
                category,
                names="カテゴリ",
                values="売上金額",
                hole=0.55,
                color_discrete_sequence=[
                    "#1e3a8a",
                    "#2563eb",
                    "#60a5fa",
                    "#93c5fd",
                    "#bfdbfe",
                ],
            )
            fig.update_traces(
                textposition="outside",
                textinfo="percent+label",
                marker=dict(line=dict(color="#ffffff", width=2)),
            )
            fig.update_layout(
                height=380,
                showlegend=False,
                margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("商品ランキング Top 10")
        ranking = top_products(filtered)
        if not ranking.empty:
            ranking_display = ranking.copy()
            ranking_display["売上金額"] = ranking_display["売上金額"].apply(lambda v: f"¥{v:,}")
            ranking_display.index = range(1, len(ranking_display) + 1)
            ranking_display.index.name = "順位"
            st.dataframe(
                ranking_display,
                use_container_width=True,
                height=380,
            )

    # ── ヒートマップ（曜日別 × カテゴリ別）─────────
    st.subheader("曜日別 × カテゴリ別 売上ヒートマップ")
    heat = filtered.copy()
    heat["曜日"] = heat["注文日"].dt.day_name()
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    weekday_jp = {"Monday": "月", "Tuesday": "火", "Wednesday": "水", "Thursday": "木", "Friday": "金", "Saturday": "土", "Sunday": "日"}
    heat["曜日"] = heat["曜日"].map(weekday_jp)
    heat_pivot = heat.pivot_table(index="曜日", columns="カテゴリ", values="売上金額", aggfunc="sum", fill_value=0)
    order_jp = [weekday_jp[d] for d in weekday_order if weekday_jp[d] in heat_pivot.index]
    heat_pivot = heat_pivot.reindex(order_jp)
    fig = go.Figure(
        data=go.Heatmap(
            z=heat_pivot.values,
            x=heat_pivot.columns,
            y=heat_pivot.index,
            colorscale=[[0, "#eff6ff"], [0.5, "#60a5fa"], [1, "#1e3a8a"]],
            colorbar=dict(title="売上金額"),
            hovertemplate="曜日: %{y}<br>カテゴリ: %{x}<br>売上: ¥%{z:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        height=300,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(color="#64748b"),
        yaxis=dict(color="#64748b"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── データ詳細 + CSV ─────────
    with st.expander("📋 元データを確認 / CSV ダウンロード"):
        st.dataframe(
            filtered.sort_values("注文日", ascending=False).head(50),
            use_container_width=True,
            height=300,
        )
        csv = filtered.to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 フィルター適用後のデータを CSV でダウンロード",
            data=csv,
            file_name=f"sales_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            type="primary",
        )

    # ── フッター ─────────
    st.markdown(
        """
        <div class="footer">
            <strong>PeaceCraft</strong> — AI Native Development.<br>
            このダッシュボードと同じものをお求めの方は
            <a href="https://corporate-lp-nextjs.vercel.app/#contact" target="_blank">こちら</a>から
            無料相談をお申し込みください。 ¥150,000〜 / 納期 2〜4 週間。
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
