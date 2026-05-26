"""売上データから自動でインサイトを生成"""
from __future__ import annotations
import pandas as pd
import numpy as np


def generate_insights(filtered: pd.DataFrame, full: pd.DataFrame) -> list[dict]:
    """フィルター後のデータと全データから 4 つの洞察カードを生成"""
    insights: list[dict] = []
    if filtered.empty:
        return insights

    # --- (1) 期間比較インサイト ---
    period_days = (filtered["注文日"].max() - filtered["注文日"].min()).days + 1
    prev_end = filtered["注文日"].min() - pd.Timedelta(days=1)
    prev_start = prev_end - pd.Timedelta(days=period_days - 1)
    prev = full[(full["注文日"] >= prev_start) & (full["注文日"] <= prev_end)]
    current_total = int(filtered["売上金額"].sum())
    prev_total = int(prev["売上金額"].sum()) if not prev.empty else 0

    if prev_total > 0:
        pct = (current_total - prev_total) / prev_total * 100
        if pct >= 5:
            insights.append({
                "kind": "success",
                "icon": "📈",
                "label": "成長トレンド",
                "text": f"今期間の売上は前期比 <strong>+{pct:.1f}%</strong>。前期 ¥{prev_total/1_000_000:.2f}M → 今期 ¥{current_total/1_000_000:.2f}M に伸長しています。",
            })
        elif pct <= -5:
            insights.append({
                "kind": "warning",
                "icon": "📉",
                "label": "前期比減少",
                "text": f"今期間の売上は前期比 <strong>{pct:.1f}%</strong>。前期 ¥{prev_total/1_000_000:.2f}M → 今期 ¥{current_total/1_000_000:.2f}M です。施策の見直しを検討。",
            })
        else:
            insights.append({
                "kind": "info",
                "icon": "📊",
                "label": "横ばい",
                "text": f"今期間の売上は前期比 <strong>{pct:+.1f}%</strong> でほぼ横ばい。安定推移しています（¥{current_total/1_000_000:.2f}M）。",
            })

    # --- (2) 曜日トレンド ---
    weekday_map = {0: "月", 1: "火", 2: "水", 3: "木", 4: "金", 5: "土", 6: "日"}
    filtered = filtered.copy()
    filtered["曜日"] = filtered["注文日"].dt.dayofweek.map(weekday_map)
    by_wday = filtered.groupby("曜日")["売上金額"].sum()
    if not by_wday.empty:
        top_wday = by_wday.idxmax()
        avg = by_wday.mean()
        top_amount = by_wday.max()
        diff_pct = (top_amount - avg) / avg * 100 if avg > 0 else 0
        insights.append({
            "kind": "info",
            "icon": "🗓",
            "label": "曜日インサイト",
            "text": f"<strong>{top_wday}曜日</strong>の売上が他曜日平均より <strong>{diff_pct:+.0f}%</strong> 高い傾向。プロモーション配信日に最適。",
        })

    # --- (3) Top カテゴリ ---
    cat = filtered.groupby("カテゴリ")["売上金額"].sum().sort_values(ascending=False)
    if not cat.empty:
        top_cat = cat.index[0]
        top_val = cat.iloc[0]
        share = top_val / cat.sum() * 100
        if share >= 40:
            insights.append({
                "kind": "warning",
                "icon": "⚠️",
                "label": "集中リスク",
                "text": f"売上の <strong>{share:.0f}%</strong> が「<strong>{top_cat}</strong>」に集中（¥{top_val/1_000_000:.2f}M）。リスク分散の検討余地あり。",
            })
        else:
            insights.append({
                "kind": "success",
                "icon": "🎯",
                "label": "Top カテゴリ",
                "text": f"<strong>{top_cat}</strong> が全体の <strong>{share:.0f}%</strong> を占めるトップカテゴリ。¥{top_val/1_000_000:.2f}M の売上を牽引。",
            })

    # --- (4) 異常日検知 (高売上日) ---
    daily = filtered.groupby(filtered["注文日"].dt.date)["売上金額"].sum()
    if len(daily) >= 7:
        mean = daily.mean()
        std = daily.std()
        if std > 0:
            spike_threshold = mean + 2 * std
            spikes = daily[daily > spike_threshold].sort_values(ascending=False)
            if not spikes.empty:
                spike_date = spikes.index[0]
                spike_val = int(spikes.iloc[0])
                spike_ratio = spike_val / mean * 100
                insights.append({
                    "kind": "info",
                    "icon": "⚡",
                    "label": "スパイク検出",
                    "text": f"<strong>{spike_date}</strong> に通常の <strong>{spike_ratio:.0f}%</strong> 相当の売上（¥{spike_val:,}）。要因分析推奨。",
                })
            else:
                # No spike → 安定インサイト
                cv = std / mean if mean > 0 else 0
                if cv < 0.3:
                    insights.append({
                        "kind": "success",
                        "icon": "✨",
                        "label": "安定運営",
                        "text": f"日次売上の変動係数は <strong>{cv:.2f}</strong>。スパイクなしで安定した運営状況です。",
                    })

    return insights


def detect_anomalies(filtered: pd.DataFrame, threshold_sigma: float = 1.8) -> pd.DataFrame:
    """日次売上の異常検知。平均 ± N × σ を逸脱した日を返す"""
    if filtered.empty:
        return pd.DataFrame(columns=["日付", "売上金額", "種別", "通常比"])
    daily = filtered.groupby(filtered["注文日"].dt.date)["売上金額"].sum().reset_index()
    daily.columns = ["日付", "売上金額"]
    if len(daily) < 3:
        return pd.DataFrame(columns=["日付", "売上金額", "種別", "通常比"])
    mean = daily["売上金額"].mean()
    std = daily["売上金額"].std()
    if std == 0:
        return pd.DataFrame(columns=["日付", "売上金額", "種別", "通常比"])
    daily["zscore"] = (daily["売上金額"] - mean) / std
    anomalies = daily[daily["zscore"].abs() >= threshold_sigma].copy()
    anomalies["種別"] = anomalies["zscore"].apply(lambda z: "📈 急増" if z > 0 else "📉 急減")
    anomalies["通常比"] = (anomalies["売上金額"] / mean * 100).round(0).astype(int).astype(str) + "%"
    return anomalies[["日付", "売上金額", "種別", "通常比"]].sort_values("日付", ascending=False)


def simple_forecast(filtered: pd.DataFrame, periods: int = 30) -> pd.DataFrame:
    """シンプルな移動平均ベースの予測"""
    if filtered.empty:
        return pd.DataFrame(columns=["日付", "予測売上金額", "lower", "upper"])
    daily = filtered.groupby(filtered["注文日"].dt.date)["売上金額"].sum().reset_index()
    daily.columns = ["日付", "売上金額"]
    if len(daily) < 7:
        return pd.DataFrame(columns=["日付", "予測売上金額", "lower", "upper"])

    # 直近 14 日の平均と標準偏差で予測
    recent = daily["売上金額"].tail(14)
    forecast_mean = recent.mean()
    forecast_std = recent.std()

    # 簡易線形トレンド
    if len(daily) >= 14:
        x = np.arange(len(daily))[-14:]
        y = daily["売上金額"].tail(14).values
        slope, intercept = np.polyfit(x, y, 1)
    else:
        slope = 0
        intercept = forecast_mean

    last_date = pd.to_datetime(daily["日付"].iloc[-1])
    future_dates = [last_date + pd.Timedelta(days=i + 1) for i in range(periods)]
    base_x = len(daily)
    predictions = [intercept + slope * (base_x + i) for i in range(periods)]

    return pd.DataFrame({
        "日付": future_dates,
        "予測売上金額": predictions,
        "lower": [max(0, p - forecast_std) for p in predictions],
        "upper": [p + forecast_std for p in predictions],
    })
