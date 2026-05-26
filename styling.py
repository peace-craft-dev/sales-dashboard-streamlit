"""カスタム CSS と HTML テンプレート"""
import streamlit as st


def apply_css():
    st.markdown(
        """
        <style>
        /* === Hide Streamlit chrome === */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* === Layout === */
        .block-container {
            padding-top: 1.2rem;
            padding-bottom: 3rem;
            max-width: 1400px;
        }

        /* === Hero === */
        .hero {
            position: relative;
            background:
              radial-gradient(at 80% 0%, rgba(59, 130, 246, 0.35) 0px, transparent 50%),
              radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.25) 0px, transparent 50%),
              linear-gradient(135deg, #0c1330 0%, #1e3a8a 60%, #2563eb 100%);
            padding: 44px 40px 40px;
            border-radius: 24px;
            color: white;
            margin-bottom: 28px;
            box-shadow: 0 20px 50px -10px rgba(15, 23, 42, 0.32);
            overflow: hidden;
        }
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 5px 14px;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.30);
            font-size: 11px;
            font-weight: 600;
            margin-bottom: 14px;
            letter-spacing: 0.04em;
        }
        .hero-badge .dot {
            width: 7px; height: 7px; border-radius: 50%;
            background: #4ade80;
            box-shadow: 0 0 0 4px rgba(74, 222, 128, 0.25);
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.4; }
        }
        .hero h1 {
            font-size: 34px;
            font-weight: 800;
            letter-spacing: -0.02em;
            margin: 0;
            line-height: 1.1;
        }
        .hero h1 span.accent {
            background: linear-gradient(135deg, #93c5fd 0%, #c7d2fe 100%);
            -webkit-background-clip: text;
            background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero p {
            margin: 12px 0 0;
            opacity: 0.88;
            font-size: 14px;
            max-width: 760px;
            line-height: 1.6;
        }
        .hero-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 14px;
            margin-top: 24px;
            padding-top: 22px;
            border-top: 1px solid rgba(255, 255, 255, 0.18);
        }
        .hero-stat .label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            opacity: 0.65;
            font-weight: 600;
            margin-bottom: 4px;
        }
        .hero-stat .value {
            font-size: 22px;
            font-weight: 800;
        }
        .hero-stat .meta {
            font-size: 11px;
            opacity: 0.7;
            margin-top: 2px;
        }

        /* === Section Header === */
        .section-header {
            display: flex;
            align-items: baseline;
            gap: 12px;
            margin: 36px 0 18px;
        }
        .section-tag {
            font-size: 10px;
            letter-spacing: 0.20em;
            text-transform: uppercase;
            color: #2563eb;
            font-weight: 700;
            background: #eff6ff;
            padding: 4px 10px;
            border-radius: 6px;
            white-space: nowrap;
        }
        .section-title {
            font-size: 20px;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
            letter-spacing: -0.01em;
        }
        .section-subtitle {
            font-size: 13px;
            color: #64748b;
            margin-left: auto;
        }

        /* === KPI cards === */
        [data-testid="stMetric"] {
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 16px 20px;
            box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            transition: all 0.2s ease;
        }
        [data-testid="stMetric"]:hover {
            transform: translateY(-3px);
            border-color: #93c5fd;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        }
        [data-testid="stMetricLabel"] {
            font-size: 11px !important;
            color: #64748b !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 600 !important;
        }
        [data-testid="stMetricValue"] {
            color: #0f172a !important;
            font-weight: 800 !important;
            font-size: 26px !important;
        }
        [data-testid="stMetricDelta"] {
            font-size: 12px !important;
        }

        /* === Insight card === */
        .insight-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 12px;
        }
        .insight-card {
            background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
            border: 1px solid #bae6fd;
            border-radius: 14px;
            padding: 16px 18px 16px 64px;
            position: relative;
            min-height: 90px;
        }
        .insight-card.warning {
            background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
            border-color: #fcd34d;
        }
        .insight-card.success {
            background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
            border-color: #86efac;
        }
        .insight-card.info {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border-color: #93c5fd;
        }
        .insight-icon {
            position: absolute;
            left: 18px;
            top: 18px;
            width: 36px;
            height: 36px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: white;
            border-radius: 10px;
            font-size: 20px;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.08);
        }
        .insight-label {
            font-size: 10px;
            color: #475569;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 6px;
        }
        .insight-text {
            color: #0f172a;
            font-weight: 600;
            font-size: 14px;
            line-height: 1.5;
        }
        .insight-text strong {
            color: #1e40af;
        }

        /* === Sidebar === */
        section[data-testid="stSidebar"] {
            background: #f8fafc;
            border-right: 1px solid #e2e8f0;
        }
        section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
            padding-top: 1.5rem;
        }
        .sidebar-title {
            font-size: 12px;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: #64748b;
            font-weight: 700;
            margin: 0 0 10px;
        }
        .sidebar-note {
            margin-top: 24px;
            padding: 12px 14px;
            background: white;
            border: 1px solid #e2e8f0;
            border-radius: 10px;
            font-size: 11px;
            color: #475569;
            line-height: 1.6;
        }

        /* === DataFrame === */
        [data-testid="stDataFrame"] {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }

        /* === Tabs === */
        button[data-baseweb="tab"] {
            font-weight: 600 !important;
            color: #64748b !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #2563eb !important;
        }

        /* === Buttons === */
        .stDownloadButton button, .stButton button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.15s ease !important;
        }
        .stDownloadButton button:hover, .stButton button:hover {
            transform: translateY(-1px);
        }

        /* === CTA banner === */
        .cta-banner {
            background:
              radial-gradient(at 90% 50%, rgba(99, 102, 241, 0.35) 0px, transparent 50%),
              linear-gradient(135deg, #0c1330 0%, #1e3a8a 100%);
            padding: 36px 32px;
            border-radius: 18px;
            color: white;
            margin-top: 48px;
            margin-bottom: 8px;
            text-align: center;
            box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.25);
            position: relative;
            overflow: hidden;
        }
        .cta-banner .cta-tag {
            display: inline-block;
            font-size: 10px;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            background: rgba(255, 255, 255, 0.14);
            border: 1px solid rgba(255, 255, 255, 0.28);
            padding: 4px 12px;
            border-radius: 999px;
            font-weight: 600;
            margin-bottom: 14px;
        }
        .cta-banner h3 {
            margin: 0 0 8px;
            font-size: 24px;
            font-weight: 800;
            letter-spacing: -0.01em;
        }
        .cta-banner p {
            margin: 0 0 18px;
            opacity: 0.85;
            font-size: 14px;
            line-height: 1.6;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        .cta-banner a.cta-primary {
            display: inline-block;
            background: white;
            color: #1e3a8a;
            padding: 11px 28px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 700;
            font-size: 14px;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            margin: 0 4px;
        }
        .cta-banner a.cta-primary:hover {
            transform: scale(1.03);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        }
        .cta-banner a.cta-secondary {
            display: inline-block;
            color: white;
            padding: 11px 24px;
            border-radius: 10px;
            text-decoration: none;
            font-weight: 600;
            font-size: 14px;
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin: 0 4px;
        }

        /* === Footer === */
        .pc-footer {
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e2e8f0;
            text-align: center;
            color: #94a3b8;
            font-size: 11px;
        }
        .pc-footer a {
            color: #2563eb;
            text-decoration: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(total_sales: int, n_orders: int, n_categories: int, period_label: str):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-badge">
                <span class="dot"></span>
                LIVE DEMO · BUILT BY PEACECRAFT
            </div>
            <h1>売上分析<br><span class="accent">ダッシュボード。</span></h1>
            <p>架空 EC データを使った、PeaceCraft 製ダッシュボード実装のライブデモです。
            左のサイドバーから期間・カテゴリを切り替えると、AI による洞察・グラフ・予測がリアルタイムに再計算されます。
            実案件では御社データ・連携先・KPI に合わせてフルカスタム設計します。</p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="label">Period</div>
                    <div class="value">{period_label}</div>
                    <div class="meta">— 動的に変動</div>
                </div>
                <div class="hero-stat">
                    <div class="label">Total Sales</div>
                    <div class="value">¥{total_sales / 1_000_000:.1f}M</div>
                    <div class="meta">サブスク + 単品</div>
                </div>
                <div class="hero-stat">
                    <div class="label">Orders</div>
                    <div class="value">{n_orders:,}</div>
                    <div class="meta">ユニーク注文数</div>
                </div>
                <div class="hero-stat">
                    <div class="label">Categories</div>
                    <div class="value">{n_categories}</div>
                    <div class="meta">アクティブ分類</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(tag: str, title: str, subtitle: str = ""):
    sub_html = f'<span class="section-subtitle">{subtitle}</span>' if subtitle else ""
    st.markdown(
        f"""
        <div class="section-header">
            <span class="section-tag">{tag}</span>
            <h2 class="section-title">{title}</h2>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insight_grid(insights: list[dict]):
    cards = "".join(
        f"""
        <div class="insight-card {ins.get('kind', 'info')}">
            <div class="insight-icon">{ins['icon']}</div>
            <div class="insight-label">{ins['label']}</div>
            <div class="insight-text">{ins['text']}</div>
        </div>
        """
        for ins in insights
    )
    st.markdown(f'<div class="insight-grid">{cards}</div>', unsafe_allow_html=True)


def render_cta():
    st.markdown(
        """
        <div class="cta-banner">
            <div class="cta-tag">¥150,000〜 · 納期 2〜4 週間</div>
            <h3>御社データで、同じ分析ダッシュボードを。</h3>
            <p>Google Sheets / Excel / PostgreSQL / API など、データソースに合わせて項目・KPI・予測モデル・通知連携をフルカスタム実装します。
            ご相談はランサーズ・ココナラ・CrowdWorks のいずれかから（スパム対策のため）</p>
            <a href="https://corporate-lp-nextjs.vercel.app/#contact" class="cta-primary" target="_blank" rel="noopener noreferrer">
                ご相談はこちら（3 サイト経由）→
            </a>
        </div>
        <div class="pc-footer">
            © 2026 <strong>PeaceCraft</strong> — AI Native Development.
            Live demo built with Streamlit · Pandas · Plotly.
            <br>
            PeaceCraft TOP:
            <a href="https://corporate-lp-nextjs.vercel.app/" target="_blank" rel="noopener noreferrer">corporate-lp-nextjs.vercel.app</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
