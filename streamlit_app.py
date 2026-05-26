"""PeaceCraft 売上ダッシュボード — Streamlit 実例デモ"""
import streamlit as st
import pandas as pd
import numpy as np
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
from insights import generate_insights, detect_anomalies, simple_forecast
from styling import (
    apply_css,
    render_hero,
    render_section_header,
    render_insight_grid,
    render_cta,
)


# ── Page Config ──
st.set_page_config(
    page_title="PeaceCraft Analytics｜Live Demo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://corporate-lp-nextjs.vercel.app/#contact",
        "About": "PeaceCraft が制作するダッシュボード実装の実例デモです。",
    },
)


apply_css()


# ── Data ──
@st.cache_data
def load_data() -> pd.DataFrame:
    return load_sample_data()


def fmt_delta(current: float, baseline: float) -> str | None:
    if baseline == 0:
        return None
    pct = (current - baseline) / baseline * 100
    sign = "+" if pct >= 0 else ""
    return f"{sign}{pct:.1f}%"


def main():
    df = load_data()

    # ── Sidebar ──
    with st.sidebar:
        st.markdown('<div class="sidebar-title">🎯 Filters</div>', unsafe_allow_html=True)

        min_date = df["注文日"].min().date()
        max_date = df["注文日"].max().date()

        period = st.radio(
            "期間プリセット",
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

        show_forecast = st.toggle("📈 簡易予測を表示", value=True)
        show_ma = st.toggle("〰️ 7日移動平均を重ねる", value=True)

        st.markdown(
            """
            <div class="sidebar-note">
                <strong>PeaceCraft Live Demo</strong><br>
                架空 EC データを使ったライブダッシュボード。
                サイドバーで条件を変えると、すべての分析が再計算されます。
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <a href="https://corporate-lp-nextjs.vercel.app/#contact" target="_blank"
               style="display:block; text-align:center; background:#2563eb; color:white;
                      padding:10px 16px; border-radius:8px; text-decoration:none;
                      font-weight:600; font-size:13px; margin-top:16px;">
                同じものを作る ¥150,000〜
            </a>
            """,
            unsafe_allow_html=True,
        )

    # ── Apply filters ──
    filtered = df.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start_date, end_date = date_range
        filtered = filtered[
            (filtered["注文日"].dt.date >= start_date)
            & (filtered["注文日"].dt.date <= end_date)
        ]
    if selected_categories:
        filtered = filtered[filtered["カテゴリ"].isin(selected_categories)]

    # ── Hero ──
    period_label = period if period != "カスタム" else "カスタム"
    if filtered.empty:
        render_hero(0, 0, 0, period_label)
        st.warning("選択条件に該当するデータがありません。フィルターを変更してください。")
        st.stop()

    kpis_now = calculate_kpis(filtered)
    render_hero(
        total_sales=kpis_now["売上合計"],
        n_orders=kpis_now["注文数"],
        n_categories=len(selected_categories) if selected_categories else df["カテゴリ"].nunique(),
        period_label=period_label,
    )

    # ── Previous period for comparison ──
    period_days = (filtered["注文日"].max() - filtered["注文日"].min()).days + 1
    prev_end = filtered["注文日"].min() - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=period_days - 1)
    prev = df[(df["注文日"] >= prev_start) & (df["注文日"] <= prev_end)]
    if selected_categories:
        prev = prev[prev["カテゴリ"].isin(selected_categories)]
    prev_kpis = calculate_kpis(prev) if not prev.empty else None

    # ============================================================
    # ── AI INSIGHTS ──
    # ============================================================
    render_section_header(
        "AI INSIGHTS",
        "データから自動抽出した 4 つの洞察",
        "リアルタイム生成",
    )
    insights = generate_insights(filtered, df)
    render_insight_grid(insights)

    # ============================================================
    # ── KPI ──
    # ============================================================
    render_section_header("KPI", "主要指標と前期間比較")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(
        "💰 売上合計",
        f"¥{kpis_now['売上合計']:,}",
        delta=fmt_delta(kpis_now["売上合計"], prev_kpis["売上合計"]) if prev_kpis else None,
    )
    col2.metric(
        "📦 注文数",
        f"{kpis_now['注文数']:,} 件",
        delta=fmt_delta(kpis_now["注文数"], prev_kpis["注文数"]) if prev_kpis else None,
    )
    col3.metric(
        "💵 平均単価",
        f"¥{kpis_now['平均単価']:,}",
        delta=fmt_delta(kpis_now["平均単価"], prev_kpis["平均単価"]) if prev_kpis else None,
    )
    col4.metric(
        "🛍 ユニーク商品",
        f"{kpis_now['ユニーク商品数']}",
    )

    # ============================================================
    # ── Trend (with moving avg + forecast) ──
    # ============================================================
    render_section_header("TREND", "売上推移（移動平均 + 予測オプション）")
    tab_daily, tab_monthly = st.tabs(["📈 日次", "📊 月次"])

    with tab_daily:
        daily = daily_sales(filtered)
        if not daily.empty:
            fig = go.Figure()
            # メインライン
            fig.add_trace(
                go.Scatter(
                    x=daily["日付"],
                    y=daily["売上金額"],
                    mode="lines+markers",
                    name="日次売上",
                    line=dict(color="#2563eb", width=2.5),
                    marker=dict(size=5, color="#2563eb"),
                    hovertemplate="%{x|%Y-%m-%d}<br>売上: ¥%{y:,.0f}<extra></extra>",
                )
            )

            # 移動平均
            if show_ma and len(daily) >= 7:
                ma7 = daily["売上金額"].rolling(window=7, min_periods=1).mean()
                fig.add_trace(
                    go.Scatter(
                        x=daily["日付"],
                        y=ma7,
                        mode="lines",
                        name="7日移動平均",
                        line=dict(color="#f59e0b", width=2, dash="dot"),
                        hovertemplate="%{x|%Y-%m-%d}<br>移動平均: ¥%{y:,.0f}<extra></extra>",
                    )
                )

            # 予測
            if show_forecast:
                fc = simple_forecast(filtered, periods=30)
                if not fc.empty:
                    fig.add_trace(
                        go.Scatter(
                            x=fc["日付"],
                            y=fc["upper"],
                            mode="lines",
                            line=dict(width=0),
                            showlegend=False,
                            hoverinfo="skip",
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=fc["日付"],
                            y=fc["lower"],
                            mode="lines",
                            line=dict(width=0),
                            fill="tonexty",
                            fillcolor="rgba(99, 102, 241, 0.15)",
                            name="予測レンジ",
                            hoverinfo="skip",
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=fc["日付"],
                            y=fc["予測売上金額"],
                            mode="lines",
                            name="予測（次30日）",
                            line=dict(color="#6366f1", width=2, dash="dash"),
                            hovertemplate="%{x|%Y-%m-%d}<br>予測: ¥%{y:,.0f}<extra></extra>",
                        )
                    )

            fig.update_layout(
                height=420,
                hovermode="x unified",
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                xaxis=dict(showgrid=False, color="#64748b"),
                yaxis=dict(gridcolor="#e2e8f0", color="#64748b", tickformat=",.0f"),
                margin=dict(l=10, r=10, t=20, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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
                text=monthly["売上金額"].apply(lambda v: f"¥{v/1_000_000:.1f}M"),
            )
            fig.update_traces(
                marker_line_width=0,
                textposition="outside",
                textfont=dict(color="#64748b", size=10),
            )
            fig.update_layout(
                height=400,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                xaxis=dict(showgrid=False, color="#64748b"),
                yaxis=dict(gridcolor="#e2e8f0", color="#64748b", tickformat=",.0f"),
                margin=dict(l=10, r=10, t=30, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # ── Category + Ranking ──
    # ============================================================
    render_section_header("CATEGORY", "カテゴリ別深掘り + Top 10 商品")
    col_left, col_right = st.columns([5, 7])

    with col_left:
        category = category_breakdown(filtered)
        if not category.empty:
            fig = go.Figure(
                go.Pie(
                    labels=category["カテゴリ"],
                    values=category["売上金額"],
                    hole=0.62,
                    marker=dict(
                        colors=["#1e3a8a", "#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#bfdbfe"],
                        line=dict(color="#ffffff", width=2),
                    ),
                    textposition="outside",
                    textinfo="percent+label",
                    hovertemplate="<b>%{label}</b><br>売上: ¥%{value:,.0f}<br>構成比: %{percent}<extra></extra>",
                )
            )
            fig.update_layout(
                height=340,
                showlegend=False,
                margin=dict(l=10, r=10, t=20, b=10),
                annotations=[
                    dict(
                        text=f"¥{kpis_now['売上合計']/1_000_000:.1f}M",
                        x=0.5, y=0.55, font=dict(size=22, color="#0f172a", family="sans-serif", weight=800),
                        showarrow=False,
                    ),
                    dict(
                        text="TOTAL",
                        x=0.5, y=0.45, font=dict(size=10, color="#64748b"),
                        showarrow=False,
                    ),
                ],
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_right:
        ranking = top_products(filtered)
        if not ranking.empty:
            ranking = ranking.copy()
            ranking["構成比"] = (ranking["売上金額"] / kpis_now["売上合計"] * 100).round(1)
            fig = go.Figure(
                go.Bar(
                    x=ranking["売上金額"],
                    y=ranking["商品名"],
                    orientation="h",
                    marker=dict(
                        color=ranking["売上金額"],
                        colorscale=[[0, "#bfdbfe"], [1, "#1e3a8a"]],
                        showscale=False,
                        line=dict(width=0),
                    ),
                    text=[f"¥{v:,}" for v in ranking["売上金額"]],
                    textposition="outside",
                    textfont=dict(color="#64748b", size=11),
                    hovertemplate="<b>%{y}</b><br>売上: ¥%{x:,.0f}<extra></extra>",
                )
            )
            fig.update_layout(
                height=340,
                plot_bgcolor="#ffffff",
                paper_bgcolor="#ffffff",
                xaxis=dict(showgrid=True, gridcolor="#e2e8f0", color="#64748b", tickformat=",.0f"),
                yaxis=dict(showgrid=False, color="#0f172a", autorange="reversed"),
                margin=dict(l=10, r=80, t=20, b=10),
                showlegend=False,
            )
            st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # ── Heatmap ──
    # ============================================================
    render_section_header(
        "HEATMAP",
        "曜日 × カテゴリ クロス分析",
        "色が濃い ＝ 売上が高い",
    )
    heat = filtered.copy()
    heat["曜日"] = heat["注文日"].dt.day_name()
    weekday_jp = {
        "Monday": "月", "Tuesday": "火", "Wednesday": "水",
        "Thursday": "木", "Friday": "金", "Saturday": "土", "Sunday": "日",
    }
    weekday_order_jp = ["月", "火", "水", "木", "金", "土", "日"]
    heat["曜日"] = heat["曜日"].map(weekday_jp)
    heat_pivot = heat.pivot_table(
        index="曜日", columns="カテゴリ", values="売上金額", aggfunc="sum", fill_value=0
    )
    order_jp = [d for d in weekday_order_jp if d in heat_pivot.index]
    heat_pivot = heat_pivot.reindex(order_jp)
    fig = go.Figure(
        data=go.Heatmap(
            z=heat_pivot.values,
            x=heat_pivot.columns,
            y=heat_pivot.index,
            colorscale=[[0, "#eff6ff"], [0.5, "#60a5fa"], [1, "#1e3a8a"]],
            colorbar=dict(title=dict(text="売上 ¥", font=dict(size=10, color="#64748b"))),
            hovertemplate="曜日: %{y}<br>カテゴリ: %{x}<br>売上: ¥%{z:,.0f}<extra></extra>",
            text=[[f"¥{v/1000:.0f}k" if v >= 1000 else "" for v in row] for row in heat_pivot.values],
            texttemplate="%{text}",
            textfont=dict(size=11, color="#0f172a"),
        )
    )
    fig.update_layout(
        height=320,
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(color="#64748b", side="top"),
        yaxis=dict(color="#64748b"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # ── Anomaly Detection ──
    # ============================================================
    render_section_header(
        "ANOMALY",
        "異常値検知（売上の急増・急減日）",
        "z-score |1.8σ| 以上",
    )
    anomalies = detect_anomalies(filtered, threshold_sigma=1.8)
    if anomalies.empty:
        st.info("選択期間内に統計的に異常な日付はありませんでした。安定した運営状況です。")
    else:
        st.dataframe(
            anomalies.assign(
                売上金額=anomalies["売上金額"].apply(lambda v: f"¥{int(v):,}"),
            ),
            use_container_width=True,
            hide_index=True,
            column_config={
                "日付": st.column_config.Column("📅 日付", width="small"),
                "売上金額": st.column_config.Column("💰 売上金額", width="small"),
                "種別": st.column_config.Column("🔔 種別", width="small"),
                "通常比": st.column_config.Column("📊 通常比", width="small"),
            },
        )

    # ============================================================
    # ── Export ──
    # ============================================================
    with st.expander("📥 データ出力 / 元データを確認", expanded=False):
        c1, c2 = st.columns([3, 2])
        with c1:
            st.markdown("**フィルター適用後データ（最新 50 行）**")
            st.dataframe(
                filtered.sort_values("注文日", ascending=False).head(50),
                use_container_width=True,
                height=280,
                hide_index=True,
            )
        with c2:
            st.markdown("**エクスポート**")
            csv = filtered.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 CSV ダウンロード",
                data=csv,
                file_name=f"peacecraft_sales_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary",
            )

            # Summary report (markdown)
            summary = f"""# PeaceCraft 売上サマリー

期間: {filtered['注文日'].min().date()} 〜 {filtered['注文日'].max().date()}
カテゴリ: {", ".join(selected_categories)}

## 主要 KPI
- 売上合計: ¥{kpis_now['売上合計']:,}
- 注文数: {kpis_now['注文数']:,} 件
- 平均単価: ¥{kpis_now['平均単価']:,}
- ユニーク商品数: {kpis_now['ユニーク商品数']}

## カテゴリ別売上
{category.assign(売上金額=category['売上金額'].apply(lambda v: f"¥{int(v):,}")).to_markdown(index=False)}

---
PeaceCraft — AI Native Development
https://corporate-lp-nextjs.vercel.app/
"""
            st.download_button(
                label="📄 サマリー（Markdown）",
                data=summary.encode("utf-8"),
                file_name=f"peacecraft_summary_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True,
            )

            st.markdown(
                """
                <div style="background:#eff6ff; border:1px solid #bfdbfe;
                  border-radius:8px; padding:10px 12px; font-size:11px;
                  color:#1e40af; margin-top:8px; line-height:1.5;">
                  💡 実案件では PDF レポート生成 / メール自動配信 / Slack 通知も実装可能です
                </div>
                """,
                unsafe_allow_html=True,
            )

    # ── CTA ──
    render_cta()


if __name__ == "__main__":
    main()
