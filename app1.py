import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from html import escape
from textwrap import dedent

st.set_page_config(page_title="REFIT House Owner Energy Advisor", page_icon="🌿", layout="wide")

OUTPUT_DIR = Path("outputs")
TARIFF_AUD = 0.30

HOUSE_SUMMARY_PATHS = [
    OUTPUT_DIR / "house_summary_refit_365days_wrangled.csv",
    OUTPUT_DIR / "house_summary_refit_365days.csv",
    OUTPUT_DIR / "house_summary_refit_200days_wrangled.csv",
    OUTPUT_DIR / "house_summary_refit_200days.csv",
    OUTPUT_DIR / "house_summary_refit_3days.csv",
    OUTPUT_DIR / "house_summary_longwindow.csv",
    OUTPUT_DIR / "week5_house_summary.csv",
]
APPLIANCE_PATHS = [
    OUTPUT_DIR / "appliance_breakdown_refit_365days_wrangled.csv",
    OUTPUT_DIR / "appliance_breakdown_refit_365days.csv",
    OUTPUT_DIR / "appliance_breakdown_refit_200days_wrangled.csv",
    OUTPUT_DIR / "appliance_breakdown_refit_200days.csv",
    OUTPUT_DIR / "appliance_breakdown_refit_200days.csv",
    OUTPUT_DIR / "appliance_breakdown_refit_3days.csv",
    OUTPUT_DIR / "appliance_breakdown_longwindow.csv",
    OUTPUT_DIR / "week5_appliance_features.csv",
]
DAILY_PATHS = [
    OUTPUT_DIR / "house_daily_consumption_refit_365days_wrangled.csv",
    OUTPUT_DIR / "house_daily_consumption_refit_365days.csv",
    OUTPUT_DIR / "house_daily_consumption_refit_200days_wrangled.csv",
    OUTPUT_DIR / "house_daily_consumption_refit_200days.csv",
    OUTPUT_DIR / "house_daily_consumption_refit_3days.csv",
    OUTPUT_DIR / "house_daily_consumption_longwindow.csv",
]
APPLIANCE_DAILY_PATHS = [
    OUTPUT_DIR / "appliance_daily_consumption_refit_365days_wrangled.csv",
    OUTPUT_DIR / "appliance_daily_consumption_refit_365days.csv",
    OUTPUT_DIR / "appliance_daily_consumption_refit_200days_wrangled.csv",
    OUTPUT_DIR / "appliance_daily_consumption_refit_200days.csv",
    OUTPUT_DIR / "appliance_daily_consumption_refit_3days.csv",
    OUTPUT_DIR / "appliance_daily_consumption_longwindow.csv",
]
RAW_PATHS = [
    OUTPUT_DIR / "refit_365days_raw_preview_wrangled.csv",
    OUTPUT_DIR / "refit_365days_raw_preview.csv",
    OUTPUT_DIR / "refit_365days_raw_loaded.csv",
    OUTPUT_DIR / "refit_200days_raw_preview_wrangled.csv",
    OUTPUT_DIR / "refit_200days_raw_preview.csv",
    OUTPUT_DIR / "refit_200days_raw_loaded.csv",
    OUTPUT_DIR / "refit_3days_raw_loaded.csv",
    OUTPUT_DIR / "refit_first3_raw_loaded.csv",
]
RECOMMENDATION_PATHS = [
    OUTPUT_DIR / "appliance_recommendations_refit_365days_wrangled.csv",
    OUTPUT_DIR / "appliance_recommendations_refit_365days.csv",
    OUTPUT_DIR / "appliance_recommendations_refit_200days_wrangled.csv",
    OUTPUT_DIR / "appliance_recommendations_refit_200days.csv",
    OUTPUT_DIR / "appliance_recommendations_refit_200days.csv",
    OUTPUT_DIR / "appliance_recommendations_longwindow.csv",
    OUTPUT_DIR / "appliance_recommendations_refit_3days.csv",
]
PRODUCT_RECOMMENDATION_PATHS = [
    OUTPUT_DIR / "product_recommendations_refit_365days_wrangled.csv",
    OUTPUT_DIR / "product_recommendations_refit_365days.csv",
    OUTPUT_DIR / "product_recommendations_refit_200days_wrangled.csv",
    OUTPUT_DIR / "product_recommendations_refit_200days.csv",
    OUTPUT_DIR / "product_recommendations_refit_200days.csv",
    OUTPUT_DIR / "product_recommendations_longwindow.csv",
    OUTPUT_DIR / "product_recommendations_refit_3days.csv",
    OUTPUT_DIR / "week5_product_recommendations.csv",
]

# ── GREEN ENERGY PALETTE ─────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Hide Streamlit top toolbar / deploy bar ── */
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 2.5rem !important;
    }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    #MainMenu { display: none !important; }
    footer { display: none !important; }

    /* ── Base ── */
    .stApp { background: #f0fdf4; }
    .block-container { max-width: 1760px; padding-top: 0.35rem; padding-bottom: 0.7rem; }
    section[data-testid="stSidebar"] { font-size: 0.96rem; }
    div[data-testid="stVerticalBlock"] { gap: 0.35rem; }
    div[data-testid="stHorizontalBlock"] { gap: 0.55rem; }
    div[data-testid="stDataFrame"] { border-radius: 14px; overflow: hidden; }

    /* ── Main navigation tabs (top-level) ── */
    div[data-testid="stTabs"] > div > div[role="tablist"] {
        gap: 0.3rem;
        background: #ffffff;
        border-radius: 16px;
        padding: 0.4rem 0.5rem;
        border: 1.5px solid #bbf7d0;
        box-shadow: 0 2px 10px rgba(22,163,74,0.08);
        margin-bottom: 0.9rem;
        flex-wrap: nowrap;
        overflow-x: auto;
    }
    div[data-testid="stTabs"] > div > div[role="tablist"] button[role="tab"] {
        border-radius: 12px !important;
        padding: 0.55rem 1.1rem !important;
        font-weight: 800 !important;
        font-size: 0.92rem !important;
        border: none !important;
        background: transparent !important;
        color: #4b5563 !important;
        white-space: nowrap;
        transition: all 0.15s ease;
    }
    div[data-testid="stTabs"] > div > div[role="tablist"] button[role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #15803d, #16a34a) !important;
        color: #ffffff !important;
        box-shadow: 0 3px 10px rgba(22,163,74,0.30) !important;
    }

    /* ── Hero banner ── */
    .hero {
        background: linear-gradient(135deg, #14532d 0%, #166534 60%, #15803d 100%);
        border-radius: 24px;
        padding: 1.4rem 1.8rem;
        box-shadow: 0 10px 32px rgba(20,83,45,0.18);
        margin-bottom: 1.1rem;
    }
    .hero-title { font-size: 2.3rem; font-weight: 900; color: #ffffff; line-height: 1.1; letter-spacing:-0.02em; }
    .hero-sub { color: #bbf7d0; font-size: 1.02rem; margin-top: 0.4rem; }
    .hero-leaf { font-size:2.8rem; line-height:1; }

    /* ── House summary metrics ── */
    .metric-card {
        background: #ffffff;
        border-radius: 18px;
        border: 1.5px solid #bbf7d0;
        padding: 1rem 1.1rem;
        box-shadow: 0 3px 12px rgba(22,163,74,0.07);
        min-height: 108px;
    }
    .metric-label { font-size: 0.80rem; font-weight: 800; color: #4ade80; text-transform: uppercase; letter-spacing: 0.06em; }
    .metric-value { font-size: 2.05rem; font-weight: 900; color: #16a34a; line-height: 1.0; margin-top: 0.22rem; }
    .metric-sub { font-size: 0.90rem; color: #6b7280; margin-top: 0.18rem; }

    /* ────────────────────────────────────────────────────────
       HERO PRODUCT CARDS  (top of page, first thing users see)
       ──────────────────────────────────────────────────────── */
    .product-hero-wrap {
        margin-bottom: 1.3rem;
    }
    .product-hero-label {
        font-size: 0.78rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #16a34a;
        margin-bottom: 0.55rem;
    }
    /* Individual hero card */
    .phero {
        background: #ffffff;
        border-radius: 22px;
        border: 2px solid #bbf7d0;
        padding: 1.5rem 1.6rem 1.35rem 1.6rem;
        box-shadow: 0 6px 24px rgba(22,163,74,0.10);
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .phero::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background: linear-gradient(90deg, #16a34a, #4ade80);
        border-radius: 22px 22px 0 0;
    }
    /* BEST card gets extra emphasis */
    .phero-best {
        border: 2.5px solid #16a34a;
        box-shadow: 0 10px 36px rgba(22,163,74,0.20);
    }
    .phero-best::before {
        height: 7px;
        background: linear-gradient(90deg, #14532d, #16a34a, #4ade80);
    }
    .phero-badge {
        display: inline-block;
        background: #f0fdf4;
        border: 1.5px solid #86efac;
        color: #15803d;
        font-size: 0.76rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        padding: 0.22rem 0.65rem;
        border-radius: 999px;
        margin-bottom: 0.55rem;
    }
    .phero-best .phero-badge {
        background: #16a34a;
        border-color: #16a34a;
        color: #ffffff;
    }
    /* Appliance name — BIGGEST text on card */
    .phero-appliance {
        font-size: 1.75rem;
        font-weight: 900;
        color: #14532d;
        line-height: 1.15;
        margin-bottom: 0.45rem;
        letter-spacing: -0.01em;
    }
    /* Store — medium, pill badge */
    .phero-store {
        display: inline-block;
        background: #dcfce7;
        color: #166534;
        font-size: 0.88rem;
        font-weight: 800;
        padding: 0.28rem 0.85rem;
        border-radius: 999px;
        margin-bottom: 1.0rem;
        border: 1px solid #bbf7d0;
    }
    /* Price — second biggest, accent green */
    .phero-price-label {
        font-size: 0.75rem;
        font-weight: 800;
        color: #4ade80;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .phero-price {
        font-size: 2.8rem;
        font-weight: 900;
        color: #16a34a;
        line-height: 1.05;
        letter-spacing: -0.02em;
    }
    /* Divider */
    .phero-divider {
        border: none;
        border-top: 1px solid #dcfce7;
        margin: 1.0rem 0 0.85rem 0;
    }
    /* Secondary stats row */
    .phero-stats {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.5rem;
    }
    .phero-stat {
        background: #f0fdf4;
        border-radius: 12px;
        padding: 0.6rem 0.7rem;
        border: 1px solid #dcfce7;
    }
    .phero-stat-label {
        font-size: 0.72rem;
        font-weight: 800;
        color: #4ade80;
        text-transform: uppercase;
        letter-spacing: 0.06em;
    }
    .phero-stat-value {
        font-size: 1.05rem;
        font-weight: 900;
        color: #15803d;
        margin-top: 0.12rem;
    }
    /* No-data placeholder for hero area */
    .phero-empty {
        background: #f0fdf4;
        border: 2px dashed #86efac;
        border-radius: 22px;
        padding: 2.2rem 1.5rem;
        text-align: center;
        color: #4ade80;
        font-size: 0.92rem;
        font-weight: 700;
    }

    /* ── General card ── */
    .card {
        background: #ffffff;
        border-radius: 18px;
        border: 1.5px solid #dcfce7;
        padding: 1.05rem 1.1rem;
        box-shadow: 0 3px 12px rgba(22,163,74,0.06);
        margin-bottom: 0.6rem;
        height: auto;
        overflow: visible !important;
    }
    .section-title { font-size: 1.15rem; font-weight: 900; color: #14532d; margin-bottom: 0.15rem; }
    .section-sub { font-size: 0.90rem; color: #6b7280; margin-bottom: 0.75rem; }

    /* ── Appliance bar list ── */
    .appliance-row { display:flex; align-items:center; gap:0.55rem; padding:0.6rem 0; border-bottom:1px solid #f0fdf4; }
    .appliance-row:last-child { border-bottom:none; }
    .appliance-name { flex:1; font-size:0.94rem; font-weight:800; color:#14532d; }
    .appliance-meta { font-size:0.86rem; color:#6b7280; min-width:5.5rem; text-align:right; }
    .appliance-cost { font-size:0.94rem; color:#16a34a; font-weight:900; min-width:5rem; text-align:right; }
    .bar-wrap { flex:1.2; margin:0 0.25rem; }
    .bar-bg { background:#dcfce7; border-radius:999px; height:8px; overflow:hidden; }
    .bar-fill { height:8px; border-radius:999px; background:linear-gradient(90deg,#16a34a,#4ade80); }

    /* ── Recommendation cards (behaviour + product list) ── */
    .rec-card { background:#f0fdf4; border:1.5px solid #bbf7d0; border-radius:14px; padding:0.8rem 0.9rem; margin-bottom:0.6rem; }
    .rec-title { font-weight:900; color:#14532d; font-size:1.0rem; }
    .rec-body { color:#374151; font-size:0.92rem; margin-top:0.25rem; line-height:1.45; }
    .badge {
        display:inline-block; border-radius:999px; padding:0.12rem 0.55rem;
        background:#dcfce7; color:#166534; font-size:0.78rem; font-weight:800; margin-left:0.3rem;
        border:1px solid #bbf7d0;
    }


    /* ── Compact savings-at-a-glance cards ── */
    .glance-header {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border: 1.5px solid #bbf7d0;
        border-radius: 20px;
        padding: 1rem 1.15rem;
        margin: 0.8rem 0 0.75rem 0;
        box-shadow: 0 4px 16px rgba(22,163,74,0.07);
    }
    .glance-kicker {
        font-size: 0.76rem;
        font-weight: 900;
        text-transform: uppercase;
        letter-spacing: 0.09em;
        color: #16a34a;
        margin-bottom: 0.15rem;
    }
    .glance-title {
        font-size: 1.35rem;
        font-weight: 950;
        color: #14532d;
        line-height: 1.15;
    }
    .glance-sub {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    .summary-stat-card {
        background: #ffffff;
        border: 1.5px solid #bbf7d0;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        min-height: 128px;
        box-shadow: 0 4px 14px rgba(22,163,74,0.07);
        position: relative;
        overflow: hidden;
    }
    .summary-stat-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background: linear-gradient(90deg, #16a34a, #86efac);
    }
    .summary-label {
        font-size: 0.76rem;
        font-weight: 900;
        color: #4ade80;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.25rem;
    }
    .summary-value {
        font-size: 1.85rem;
        font-weight: 950;
        color: #16a34a;
        line-height: 1.05;
        letter-spacing: -0.02em;
    }
    .summary-name {
        font-size: 0.92rem;
        font-weight: 850;
        color: #14532d;
        margin-top: 0.35rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .summary-note {
        font-size: 0.82rem;
        color: #6b7280;
        margin-top: 0.15rem;
    }
    .summary-panel {
        background: #ffffff;
        border: 1.5px solid #dcfce7;
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 6px 22px rgba(22,163,74,0.08);
        margin-top: 0.75rem;
        min-height: 410px;
    }
    .summary-panel-title {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.8rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.65rem;
        border-bottom: 1px solid #dcfce7;
    }
    .summary-panel-title-main {
        font-size: 1.08rem;
        font-weight: 950;
        color: #14532d;
        line-height: 1.15;
    }
    .summary-panel-sub {
        font-size: 0.84rem;
        color: #6b7280;
        margin-top: 0.16rem;
    }
    .summary-count-pill {
        background: linear-gradient(135deg, #dcfce7, #bbf7d0);
        color: #166534;
        border: 1px solid #86efac;
        border-radius: 999px;
        padding: 0.22rem 0.64rem;
        font-size: 0.75rem;
        font-weight: 950;
        white-space: nowrap;
    }
    .compact-rec-card {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
        border: 1.5px solid #bbf7d0;
        border-left: 5px solid #16a34a;
        border-radius: 16px;
        padding: 0.78rem 0.9rem;
        margin-bottom: 0.65rem;
        box-shadow: 0 3px 10px rgba(22,163,74,0.06);
    }
    .compact-rec-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 0.65rem;
        margin-bottom: 0.35rem;
    }
    .compact-rec-name {
        font-size: 1.0rem;
        font-weight: 950;
        color: #14532d;
        line-height: 1.15;
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    .compact-rec-price {
        display: inline-block;
        background: #16a34a;
        color: #ffffff;
        border: 1px solid #16a34a;
        border-radius: 999px;
        padding: 0.18rem 0.62rem;
        font-size: 0.78rem;
        font-weight: 950;
        white-space: nowrap;
    }
    .compact-rec-pill {
        display: inline-block;
        background: #ffffff;
        color: #15803d;
        border: 1px solid #bbf7d0;
        border-radius: 999px;
        padding: 0.14rem 0.55rem;
        font-size: 0.74rem;
        font-weight: 900;
        white-space: nowrap;
    }
    .compact-rec-body {
        color: #374151;
        font-size: 0.88rem;
        line-height: 1.42;
        min-height: 2.35rem;
    }
    .compact-rec-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-top: 0.48rem;
    }
    .compact-rec-meta .compact-rec-pill { background:#f8fafc; }


    /* ── Appliance Advisor compact cards ── */
    .advisor-header-card {
        background: linear-gradient(135deg, #14532d 0%, #166534 70%, #16a34a 100%);
        border-radius: 20px;
        padding: 1rem 1.15rem;
        box-shadow: 0 8px 28px rgba(20,83,45,0.16);
        margin-bottom: 0.7rem;
    }
    .advisor-header-title {
        color: #ffffff !important;
        font-size: 1.45rem;
        font-weight: 950;
        line-height: 1.12;
        letter-spacing: -0.015em;
    }
    .advisor-header-sub {
        color: #bbf7d0 !important;
        font-size: 0.9rem;
        margin-top: 0.18rem;
    }
    .advisor-summary-strip {
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.55rem;
        margin: 0.55rem 0 0.78rem 0;
    }
    .advisor-mini-metric {
        background: #ffffff;
        border: 1.5px solid #dcfce7;
        border-radius: 15px;
        padding: 0.72rem 0.78rem;
        box-shadow: 0 3px 10px rgba(22,163,74,0.05);
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
    }
    .advisor-mini-metric:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(22,163,74,0.13);
        border-color: #86efac;
    }
    .advisor-mini-label {
        color: #4ade80;
        font-size: 0.70rem;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.16rem;
    }
    .advisor-mini-value {
        color: #14532d;
        font-size: 1.18rem;
        font-weight: 950;
        line-height: 1.05;
    }
    .advisor-mini-note {
        color: #6b7280;
        font-size: 0.78rem;
        margin-top: 0.16rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .advisor-grid-3 {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.62rem;
        margin-top: 0.48rem;
    }
    .advisor-grid-2 {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 0.55rem;
        margin-top: 0.48rem;
    }
    .advisor-product-card,
    .advisor-insight-card,
    .advisor-explain-card,
    .advisor-option-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1.5px solid #dcfce7;
        border-radius: 17px;
        padding: 0.82rem 0.9rem;
        box-shadow: 0 3px 12px rgba(22,163,74,0.06);
        height: 100%;
        transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        overflow: hidden;
    }
    .advisor-product-card:hover,
    .advisor-insight-card:hover,
    .advisor-explain-card:hover,
    .advisor-option-card:hover {
        transform: translateY(-2px);
        border-color: #86efac;
        box-shadow: 0 9px 24px rgba(22,163,74,0.13);
    }
    .advisor-role {
        display: inline-block;
        color: #15803d;
        background: #dcfce7;
        border: 1px solid #bbf7d0;
        border-radius: 999px;
        padding: 0.15rem 0.52rem;
        font-size: 0.70rem;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.44rem;
    }
    .advisor-product-name {
        color: #14532d;
        font-size: 1.05rem;
        font-weight: 950;
        line-height: 1.15;
        margin-bottom: 0.18rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .advisor-product-store {
        color: #6b7280;
        font-size: 0.82rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .advisor-price-big {
        color: #16a34a;
        font-size: 1.62rem;
        font-weight: 950;
        line-height: 1;
        margin-bottom: 0.55rem;
    }
    .advisor-stat-row {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.35rem;
        margin-top: 0.45rem;
    }
    .advisor-stat {
        background: #f0fdf4;
        border: 1px solid #dcfce7;
        border-radius: 12px;
        padding: 0.48rem 0.52rem;
    }
    .advisor-stat-label {
        color: #4ade80;
        font-size: 0.64rem;
        font-weight: 950;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .advisor-stat-value {
        color: #14532d;
        font-size: 0.84rem;
        font-weight: 950;
        margin-top: 0.08rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .advisor-short-note {
        color: #4b5563;
        font-size: 0.80rem;
        line-height: 1.36;
        margin-top: 0.52rem;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
    }
    .advisor-list-title {
        color: #14532d;
        font-size: 1.0rem;
        font-weight: 950;
        margin: 0.7rem 0 0.2rem 0;
    }
    .advisor-option-top {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 0.55rem;
        margin-bottom: 0.26rem;
    }
    .advisor-option-name {
        color: #14532d;
        font-size: 0.92rem;
        font-weight: 950;
        line-height: 1.18;
    }
    .advisor-option-price {
        color: #ffffff;
        background: #16a34a;
        border-radius: 999px;
        padding: 0.12rem 0.44rem;
        font-size: 0.72rem;
        font-weight: 950;
        white-space: nowrap;
    }
    .advisor-option-meta {
        color: #6b7280;
        font-size: 0.78rem;
        line-height: 1.35;
    }
    .advisor-insight-number {
        color: #16a34a;
        font-size: 1.5rem;
        font-weight: 950;
        line-height: 1.05;
        margin: 0.1rem 0;
    }
    .advisor-insight-text,
    .advisor-explain-text {
        color: #374151;
        font-size: 0.86rem;
        line-height: 1.43;
    }
    .advisor-reason-pills {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-top: 0.45rem;
    }
    .advisor-reason-pill {
        display: inline-block;
        background: #f0fdf4;
        color: #15803d;
        border: 1px solid #bbf7d0;
        border-radius: 999px;
        padding: 0.13rem 0.52rem;
        font-size: 0.72rem;
        font-weight: 900;
    }
    @media (max-width: 1100px) {
        .advisor-summary-strip, .advisor-grid-3 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .advisor-grid-2 { grid-template-columns: 1fr; }
    }

    /* ── Detail / choice cards ── */
    .choice-card { background:#ffffff; border:1.5px solid #dcfce7; border-radius:16px; padding:0.9rem 1rem; margin-bottom:0.7rem; box-shadow:0 2px 8px rgba(22,163,74,0.05); }
    .choice-title { font-size:1.0rem; font-weight:900; color:#14532d; margin-bottom:0.25rem; }
    .choice-body { color:#374151; font-size:0.92rem; line-height:1.5; }

    /* ── Insight / note boxes ── */
    .insight-box { background:#f0fdf4; border:1.5px solid #bbf7d0; border-radius:14px; padding:0.8rem 0.9rem; color:#14532d; font-size:0.92rem; margin-bottom:0.6rem; }
    .owner-note { background:#f0fdf4; border-left:4px solid #16a34a; border-radius:0 12px 12px 0; padding:0.85rem 1rem; color:#374151; font-size:0.94rem; margin-bottom:0.6rem; }
    .soft-note { background:#f9fafb; border:1px dashed #86efac; border-radius:12px; padding:0.78rem 0.9rem; color:#6b7280; font-size:0.82rem; margin-top:0.4rem; }

    /* ── Mini grid (2×2 stats) ── */
    .mini-grid { display:grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap:0.65rem; }
    .mini-card { background:#f0fdf4; border:1.5px solid #bbf7d0; border-radius:14px; padding:0.75rem 0.85rem; }
    .mini-title { font-size:0.88rem; font-weight:850; color:#374151; margin-bottom:0.2rem; }
    .mini-value { font-size:1.18rem; font-weight:900; color:#16a34a; }
    .mini-sub { font-size:0.82rem; color:#6b7280; margin-top:0.15rem; }

    /* ── Comparison cards ── */
    .comparison-card { background:#f0fdf4; border:1.5px solid #bbf7d0; border-radius:14px; padding:0.75rem 0.9rem; margin-bottom:0.55rem; }
    .comparison-title { font-weight:900; color:#14532d; font-size:0.98rem; }
    .comparison-body { color:#374151; font-size:0.90rem; line-height:1.45; margin-top:0.2rem; }

    /* ── Chart card ── */
    .chart-title-card { background:#f0fdf4; border:1.5px solid #bbf7d0; border-radius:14px; padding:0.75rem 0.9rem; margin-bottom:0.65rem; color:#14532d; font-weight:900; }
    .slider-heading { font-size:1.0rem; font-weight:900; color:#14532d; margin:0.25rem 0 0.2rem 0; }

    /* ── Overflow fixes ── */
    .stMarkdown { overflow: visible !important; }
    [data-testid="stElementContainer"] { overflow: visible !important; }
    .card, .rec-card, .choice-card, .insight-box, .owner-note, .soft-note { overflow: visible !important; }
    .element-container { margin-bottom: 0.08rem !important; }
    div[data-testid="stPlotlyChart"], div[data-testid="stImage"] { overflow: visible !important; }

    /* ── Text colours ── */
    h1,h2,h3,h4,h5,h6,p,label,span,div { color: #14532d; }
    .stApp h1,.stApp h2,.stApp h3,.stApp h4 { color: #14532d !important; font-weight: 900 !important; }
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li { color: #1f2937 !important; }

    /* ── Inner sub-tabs (Appliance Advisor) ── */
    .stTabs [data-baseweb="tab-list"] { gap:0.35rem; }
    .stTabs [data-baseweb="tab"] { background:#ffffff; border:1.5px solid #bbf7d0; border-radius:999px; padding:0.35rem 0.9rem; color:#15803d !important; font-weight:800; }
    .stTabs [aria-selected="true"] { background:#16a34a !important; border-color:#16a34a !important; color:#ffffff !important; }
    [data-testid="stWidgetLabel"] p { color:#14532d !important; font-weight:800 !important; }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] { background:#ffffff !important; border-right:1px solid #dcfce7 !important; }
    section[data-testid="stSidebar"] * { color:#111827 !important; }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] p { color:#111827 !important; font-weight:700 !important; }

    /* ── Selectbox / dropdowns ── */
    div[data-baseweb="select"],
    div[data-baseweb="select"] > div,
    div[data-baseweb="select"] input,
    div[data-baseweb="select"] span,
    div[data-baseweb="select"] div { background-color:#ffffff !important; color:#111827 !important; -webkit-text-fill-color:#111827 !important; opacity:1 !important; }
    div[data-baseweb="select"] > div { border:1.5px solid #bbf7d0 !important; border-radius:10px !important; }
    div[data-baseweb="select"] svg { fill:#16a34a !important; color:#16a34a !important; }
    div[data-baseweb="popover"],div[data-baseweb="popover"] *,ul[role="listbox"],ul[role="listbox"] *,li[role="option"],li[role="option"] * { background-color:#ffffff !important; color:#111827 !important; -webkit-text-fill-color:#111827 !important; opacity:1 !important; }
    li[role="option"]:hover,li[role="option"][aria-selected="true"],div[role="option"]:hover,div[role="option"][aria-selected="true"] { background-color:#f0fdf4 !important; color:#14532d !important; -webkit-text-fill-color:#14532d !important; }

    /* ── Sliders / checkboxes ── */
    div[data-testid="stSlider"] *,div[data-testid="stCheckbox"] *,div[data-testid="stRadio"] * { color:#111827 !important; -webkit-text-fill-color:#111827 !important; opacity:1 !important; }
    div[data-testid="stSlider"] [data-baseweb="slider"] div { color:#111827 !important; }
    div[data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] { background:#16a34a !important; border-color:#16a34a !important; }
</style>

""", unsafe_allow_html=True)

# ── LANDING DASHBOARD UX REWORK ──────────────────────────────────────────────
st.markdown("""
<style>
    .landing-shell { margin-top: 0.15rem; }

    .landing-header-card {
        background: linear-gradient(135deg, #14532d 0%, #166534 58%, #16a34a 100%);
        border-radius: 24px;
        padding: 1.12rem 1.22rem;
        box-shadow: 0 12px 34px rgba(20,83,45,0.18);
        border: 1px solid rgba(187,247,208,0.35);
        margin-bottom: 0.72rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
    }
    .landing-header-card:hover { transform: translateY(-3px); box-shadow: 0 18px 42px rgba(20,83,45,0.24); }
    .landing-header-eyebrow { color:#bbf7d0; font-size:0.78rem; font-weight:900; text-transform:uppercase; letter-spacing:0.11em; margin-bottom:0.25rem; }
    .landing-header-title { color:#ffffff !important; font-size:1.72rem; font-weight:950; line-height:1.05; letter-spacing:-0.03em; }
    .landing-header-sub { color:#dcfce7 !important; font-size:0.84rem; margin-top:0.45rem; line-height:1.35; }
    .landing-house-pill { display:inline-block; background:#ffffff; color:#15803d; font-weight:950; padding:0.28rem 0.75rem; border-radius:999px; margin-top:0.48rem; box-shadow:0 4px 14px rgba(0,0,0,0.10); }

    .landing-kpi-grid { display:grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap:0.56rem; margin-bottom:0.68rem; }
    .landing-kpi-card {
        background:#ffffff;
        border:1.5px solid #bbf7d0;
        border-radius:18px;
        padding:0.78rem 0.74rem;
        box-shadow:0 4px 16px rgba(22,163,74,0.08);
        min-height:96px;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .landing-kpi-card:hover { transform:translateY(-3px); box-shadow:0 10px 24px rgba(22,163,74,0.16); border-color:#16a34a; }
    .landing-kpi-label { font-size:0.68rem; font-weight:950; color:#15803d; text-transform:uppercase; letter-spacing:0.07em; line-height:1.25; }
    .landing-kpi-value { font-size:1.38rem; font-weight:950; color:#14532d; line-height:1.05; margin-top:0.3rem; }
    .landing-kpi-sub { font-size:0.67rem; color:#6b7280; margin-top:0.25rem; line-height:1.25; }

    .landing-panel {
        background:#ffffff;
        border:1.5px solid #dcfce7;
        border-radius:18px;
        padding:0.86rem 0.92rem;
        box-shadow:0 5px 18px rgba(22,163,74,0.08);
        margin-bottom:0.95rem;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .landing-panel:hover { transform:translateY(-2px); box-shadow:0 12px 28px rgba(22,163,74,0.14); border-color:#86efac; }
    .landing-panel-title { font-size:0.98rem; font-weight:950; color:#14532d; line-height:1.25; }
    .landing-panel-sub { font-size:0.74rem; color:#6b7280; margin-top:0.16rem; line-height:1.35; }

    .right-pick-card {
        background:#f0fdf4;
        border:1.5px solid #bbf7d0;
        border-radius:15px;
        padding:0.72rem 0.70rem;
        margin-top:0;
        min-height:228px;
        display:flex;
        flex-direction:column;
        justify-content:space-between;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .right-pick-card:hover { transform:translateY(-3px); box-shadow:0 8px 20px rgba(22,163,74,0.14); border-color:#16a34a; }
    .right-pick-head { display:flex; justify-content:space-between; align-items:flex-start; gap:0.5rem; margin-bottom:0.45rem; }
    .right-pick-badge { display:inline-block; background:#16a34a; color:#ffffff; font-size:0.61rem; font-weight:950; letter-spacing:0.06em; text-transform:uppercase; padding:0.18rem 0.55rem; border-radius:999px; }
    .right-pick-appliance { font-size:0.88rem; font-weight:950; color:#14532d; margin-top:0.35rem; line-height:1.15; }
    .right-pick-store { color:#166534; font-size:0.70rem; font-weight:850; margin-top:0.18rem; }
    .right-pick-price { color:#16a34a; font-size:1.05rem; font-weight:950; white-space:nowrap; }
    .right-pick-product { color:#4b5563; font-size:0.68rem; line-height:1.3; margin-bottom:0.55rem; }
    .right-pick-stats { display:grid; grid-template-columns: 1fr; gap:0.30rem; }
    .right-pick-stat { background:#ffffff; border:1px solid #dcfce7; border-radius:10px; padding:0.36rem 0.38rem; }
    .right-pick-stat-label { color:#16a34a; font-size:0.54rem; font-weight:950; text-transform:uppercase; letter-spacing:0.05em; }
    .right-pick-stat-value { color:#14532d; font-size:0.70rem; font-weight:950; margin-top:0.12rem; }

    .advice-stack { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:0.42rem; margin-top:0.52rem; }
    .advice-item { background:#f8fafc; border:1px solid #dcfce7; border-left:4px solid #16a34a; border-radius:12px; padding:0.52rem 0.58rem; }
    .advice-title { font-size:0.74rem; font-weight:950; color:#14532d; margin-bottom:0.16rem; }
    .advice-text { font-size:0.70rem; color:#374151; line-height:1.42; }

    .trend-mini-control-note { font-size:0.70rem; color:#6b7280; margin-top:-0.35rem; margin-bottom:0.45rem; }

    .home-mini-grid { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:0.56rem; margin:0.10rem 0 0.74rem 0; }
    .home-mini-card {
        background:linear-gradient(135deg,#ffffff 0%,#f8fafc 100%);
        border:1.5px solid #dcfce7;
        border-left:5px solid #16a34a;
        border-radius:16px;
        padding:0.74rem 0.78rem;
        min-height:112px;
        box-shadow:0 4px 14px rgba(22,163,74,0.07);
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
    }
    .home-mini-card:hover { transform:translateY(-2px); box-shadow:0 10px 24px rgba(22,163,74,0.13); border-color:#86efac; }
    .home-mini-label { font-size:0.68rem; font-weight:950; color:#15803d; text-transform:uppercase; letter-spacing:0.07em; margin-bottom:0.2rem; }
    .home-mini-value { font-size:1.05rem; font-weight:950; color:#14532d; line-height:1.15; }
    .home-mini-note { font-size:0.70rem; color:#6b7280; line-height:1.35; margin-top:0.28rem; }


    .right-picks-grid { display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:0.42rem; margin-top:0.55rem; }
    .home-trend-control-grid { display:grid; grid-template-columns: 0.85fr 1.15fr 1fr; gap:0.55rem; align-items:end; margin-top:0.35rem; }
    .home-trend-note { background:#f0fdf4; border:1px dashed #86efac; border-radius:12px; padding:0.45rem 0.6rem; color:#166534; font-size:0.70rem; font-weight:750; margin:0.35rem 0 0.25rem 0; }

    /* Home overview compact controls */
    div[data-testid="stRadio"] label p, div[data-testid="stSelectbox"] label p, div[data-testid="stSlider"] label p { font-size:0.74rem !important; }
    div[data-testid="stRadio"] [role="radiogroup"] { gap:0.25rem !important; }
    div[data-testid="stRadio"] [role="radiogroup"] label { padding:0.12rem 0.22rem !important; }

    @media (max-width: 1500px) { .right-picks-grid, .advice-stack { grid-template-columns: 1fr; } .right-pick-stats { grid-template-columns: repeat(3, minmax(0,1fr)); } }

    @media (max-width: 1200px) {
        .landing-kpi-grid, .home-mini-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .landing-header-title { font-size:1.65rem; }
    }
</style>
""", unsafe_allow_html=True)

# ── Chart colour palette (green-forward) ────────────────────────────────────
COLORS = ["#16a34a", "#4f46e5", "#0891b2", "#d97706", "#db2777", "#7c3aed", "#0d9488", "#ca8a04", "#6366f1", "#ec4899"]

# ── REFIT REAL APPLIANCE NAMES ───────────────────────────────────────────────
REFIT_APPLIANCE_NAME_MAP = {
    1: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge", "Chest Freezer", "Upright Freezer", "Tumble Dryer", "Washing Machine", "Dishwasher", "Computer Site", "Television Site", "Electric Heater"])),
    2: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge-Freezer", "Washing Machine", "Dishwasher", "Television", "Microwave", "Toaster", "Hi-Fi", "Kettle", "Oven Extractor Fan"])),
    3: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Toaster", "Fridge-Freezer", "Freezer", "Tumble Dryer", "Dishwasher", "Washing Machine", "Television", "Microwave", "Kettle"])),
    4: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge", "Freezer", "Fridge-Freezer", "Washing Machine 1", "Washing Machine 2", "Computer Site", "Television Site", "Microwave", "Kettle"])),
    5: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge-Freezer", "Tumble Dryer", "Washing Machine", "Dishwasher", "Computer Site", "Television Site", "Combination Microwave", "Kettle", "Toaster"])),
    6: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Freezer Utility Room", "Washing Machine", "Dishwasher", "MJY Computer", "Television Site", "Microwave", "Kettle", "Toaster", "PGM Computer"])),
    7: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge", "Freezer Garage", "Freezer", "Tumble Dryer", "Washing Machine", "Dishwasher", "Television Site", "Toaster", "Kettle"])),
    8: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge", "Freezer", "Dryer", "Washing Machine", "Toaster", "Computer", "Television Site", "Microwave", "Kettle"])),
    9: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge-Freezer", "Washer Dryer", "Washing Machine", "Dishwasher", "Television Site", "Microwave", "Kettle", "Hi-Fi", "Electric Heater"])),
    10: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Magimix Blender", "Freezer", "Chest Freezer Garage", "Fridge-Freezer", "Washing Machine", "Dishwasher", "Television Site", "Microwave", "Kenwood KMix"])),
    11: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge", "Fridge-Freezer", "Washing Machine", "Dishwasher", "Computer Site", "Microwave", "Kettle", "Router", "Hi-Fi"])),
    12: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge-Freezer", "Television Site Lounge", "Microwave", "Kettle", "Toaster", "Television Site Bedroom", "Not Used", "Not Used", "Not Used"])),
    13: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Television Site", "Unknown", "Washing Machine", "Dishwasher", "Tumble Dryer", "Television Site", "Computer Site", "Microwave", "Kettle"])),
    15: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge-Freezer", "Tumble Dryer", "Washing Machine", "Dishwasher", "Computer Site", "Television Site", "Microwave", "Kettle", "Toaster"])),
    16: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge-Freezer 1", "Fridge-Freezer 2", "Electric Heater 1", "Electric Heater 2", "Washing Machine", "Dishwasher", "Computer Site", "Television Site", "Dehumidifier / Heater"])),
    17: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Freezer Garage", "Fridge-Freezer", "Tumble Dryer Garage", "Washing Machine", "Computer Site", "Television Site", "Microwave", "Kettle", "Plug Site Bedroom"])),
    18: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge Garage", "Freezer Garage", "Fridge-Freezer", "Washer Dryer Garage", "Washing Machine", "Dishwasher", "Desktop Computer", "Television Site", "Microwave"])),
    19: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge and Freezer", "Washing Machine", "Television Site", "Microwave", "Kettle", "Toaster", "Bread-maker", "Lamp 80W", "Hi-Fi"])),
    20: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge", "Freezer", "Tumble Dryer", "Washing Machine", "Dishwasher", "Computer Site", "Television Site", "Microwave", "Kettle"])),
    21: dict(zip([f"Appliance{i}" for i in range(1, 10)], ["Fridge-Freezer", "Tumble Dryer", "Washing Machine", "Dishwasher", "Food Mixer", "Television", "Kettle / Toaster", "Vivarium", "Pond Pump"])),
}


def real_refit_name(house, refit_column):
    try:
        house_id = int(house)
    except Exception:
        return str(refit_column).replace("_", " ").title()
    col = str(refit_column).strip()
    return REFIT_APPLIANCE_NAME_MAP.get(house_id, {}).get(col, col.replace("_", " ").title())


def apply_refit_names(df):
    if df.empty or "house" not in df.columns:
        return df
    df = df.copy()
    if "refit_column" in df.columns:
        df["original_refit_column"] = df["refit_column"]
        df["real_appliance_name"] = df.apply(lambda r: real_refit_name(r.get("house"), r.get("refit_column")), axis=1)
        df["appliance_label"] = df["real_appliance_name"]
        df["appliance_type"] = df["real_appliance_name"]
    return df


def first_existing(paths):
    for p in paths:
        if p.exists():
            return p
    return None


def load_csv(paths):
    path = first_existing(paths)
    if path is None:
        return pd.DataFrame(), None
    df = pd.read_csv(path)
    for c in ["date", "Time", "timestamp", "window_start", "window_end"]:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df, path


def ensure_numeric(df, cols):
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def snum(v):
    try:
        if pd.isna(v):
            return 0.0
        return float(v)
    except Exception:
        return 0.0


def money(v):
    try:
        if pd.isna(v):
            return "n/a"
        return f"${float(v):.2f}"
    except Exception:
        return "n/a"


def section(title, subtitle=""):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-sub'>{subtitle}</div>", unsafe_allow_html=True)


def metric_card(col, label, value, sub):
    with col:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div><div class='metric-sub'>{sub}</div></div>",
            unsafe_allow_html=True,
        )


def appliance_name(row):
    if "real_appliance_name" in row and pd.notna(row["real_appliance_name"]):
        return str(row["real_appliance_name"])
    if "house" in row and "refit_column" in row and pd.notna(row["refit_column"]):
        return real_refit_name(row["house"], row["refit_column"])
    for c in ["appliance_label", "appliance_type", "appliance", "refit_column"]:
        if c in row and pd.notna(row[c]):
            return str(row[c]).replace("_", " ").title()
    return "Appliance"


def _make_day_series_from_daily(daily_house, appliance_daily_house, raw_house, selected_refit_cols, start_day, end_day):
    house_series = pd.Series(dtype=float)
    app_series_map = {}

    if not daily_house.empty and "date" in daily_house.columns:
        hd = daily_house.copy()
        hd["date"] = pd.to_datetime(hd["date"], errors="coerce")
        hd = hd.dropna(subset=["date"]).sort_values("date")
        if not hd.empty:
            first_date = hd["date"].min()
            hd["day_number"] = ((hd["date"] - first_date).dt.days + 1).astype(int)
            hd = hd[(hd["day_number"] >= start_day) & (hd["day_number"] <= end_day)]
            house_value_col = "aggregate_kwh" if "aggregate_kwh" in hd.columns else "mains_daily_kwh" if "mains_daily_kwh" in hd.columns else None
            if house_value_col:
                house_series = pd.Series(pd.to_numeric(hd[house_value_col], errors="coerce").values, index=hd["day_number"].astype(int)).sort_index()

    if not appliance_daily_house.empty and "date" in appliance_daily_house.columns and "refit_column" in appliance_daily_house.columns:
        ad = appliance_daily_house.copy()
        ad["date"] = pd.to_datetime(ad["date"], errors="coerce")
        ad = ad.dropna(subset=["date"]).sort_values("date")
        if not ad.empty:
            first_date = daily_house["date"].min() if not daily_house.empty and "date" in daily_house.columns else ad["date"].min()
            first_date = pd.to_datetime(first_date, errors="coerce")
            ad["day_number"] = ((ad["date"] - first_date).dt.days + 1).astype(int)
            ad = ad[(ad["day_number"] >= start_day) & (ad["day_number"] <= end_day)]
            for refit_col in selected_refit_cols:
                one = ad[ad["refit_column"].astype(str) == str(refit_col)].copy()
                if not one.empty and "daily_kwh" in one.columns:
                    vals = pd.to_numeric(one["daily_kwh"], errors="coerce").fillna(0).clip(lower=0)
                    app_series_map[str(refit_col)] = pd.Series(vals.values, index=one["day_number"].astype(int)).sort_index()

    if (house_series.empty or len(app_series_map) < len(selected_refit_cols)) and not raw_house.empty:
        time_col = "timestamp" if "timestamp" in raw_house.columns else "Time" if "Time" in raw_house.columns else None
        if time_col:
            tmp = raw_house.copy()
            tmp[time_col] = pd.to_datetime(tmp[time_col], errors="coerce")
            tmp = tmp.dropna(subset=[time_col]).sort_values(time_col)
            if not tmp.empty:
                first_time = tmp[time_col].min()
                tmp["day_number"] = ((tmp[time_col] - first_time).dt.total_seconds() // 86400).astype(int) + 1
                tmp = tmp[(tmp["day_number"] >= start_day) & (tmp["day_number"] <= end_day)].copy()
                if house_series.empty and "Aggregate" in tmp.columns:
                    house_series = tmp.groupby("day_number")["Aggregate"].mean().apply(lambda w: max(float(w), 0) * 24 / 1000.0)
                for refit_col in selected_refit_cols:
                    if str(refit_col) in tmp.columns and str(refit_col) not in app_series_map:
                        app_series_map[str(refit_col)] = tmp.groupby("day_number")[str(refit_col)].mean().apply(lambda w: max(float(w), 0) * 24 / 1000.0)

    return house_series, app_series_map


def _aggregate_by_period(series, period_label):
    if series is None or len(series) == 0:
        return series
    s = pd.to_numeric(series, errors="coerce").dropna().sort_index()
    if s.empty:
        return s
    if period_label == "Day by day":
        return s
    days_per_bin = {"Weekly": 7, "Monthly": 30, "Three months": 90}.get(period_label, 1)
    bins = ((s.index.astype(int) - 1) // days_per_bin) * days_per_bin + 1
    grouped = s.groupby(bins).sum()
    grouped.index = [f"Day {int(i)}-{int(i + days_per_bin - 1)}" for i in grouped.index]
    return grouped


def _cap_appliance_to_household(app_series, household_series):
    if app_series is None or len(app_series) == 0:
        return app_series
    app = pd.to_numeric(app_series, errors="coerce").dropna().sort_index()
    if app.empty or household_series is None or len(household_series) == 0:
        return app

    house = pd.to_numeric(household_series, errors="coerce").dropna().sort_index()
    if house.empty:
        return app

    common_index = app.index.intersection(house.index)
    if len(common_index) > 0:
        app = app.loc[common_index]
        house_aligned = house.loc[common_index]
        capped = np.minimum(app.values, house_aligned.values)
        return pd.Series(capped, index=common_index)

    n = min(len(app), len(house))
    if n <= 0:
        return app
    capped = np.minimum(app.iloc[:n].values, house.iloc[:n].values)
    return pd.Series(capped, index=app.index[:n])


def _make_raw_8_second_series(raw_house, selected_refit_cols, start_day, end_day):
    house_series = pd.Series(dtype=float)
    app_series_map = {}
    x_labels_map = {}

    if raw_house.empty:
        return house_series, app_series_map, x_labels_map

    time_col = "timestamp" if "timestamp" in raw_house.columns else "Time" if "Time" in raw_house.columns else None
    if time_col is None:
        return house_series, app_series_map, x_labels_map

    tmp = raw_house.copy()
    tmp[time_col] = pd.to_datetime(tmp[time_col], errors="coerce")
    tmp = tmp.dropna(subset=[time_col]).sort_values(time_col)
    if tmp.empty:
        return house_series, app_series_map, x_labels_map

    first_time = tmp[time_col].min()
    tmp["day_number"] = ((tmp[time_col] - first_time).dt.total_seconds() // 86400).astype(int) + 1
    tmp = tmp[(tmp["day_number"] >= start_day) & (tmp["day_number"] <= end_day)].copy()
    if tmp.empty:
        return house_series, app_series_map, x_labels_map

    max_points = 5000
    if len(tmp) > max_points:
        tmp = tmp.iloc[::max(1, len(tmp) // max_points)].copy()

    plot_index = range(len(tmp))
    labels = tmp[time_col].dt.strftime("Day %j %H:%M:%S").tolist()

    if "Aggregate" in tmp.columns:
        vals = pd.to_numeric(tmp["Aggregate"], errors="coerce").fillna(0).clip(lower=0)
        house_series = pd.Series(vals.values, index=plot_index)
        x_labels_map["household"] = labels

    for refit_col in selected_refit_cols:
        col = str(refit_col)
        if col in tmp.columns:
            vals = pd.to_numeric(tmp[col], errors="coerce").fillna(0).clip(lower=0)
            app_series_map[col] = pd.Series(vals.values, index=plot_index)
            x_labels_map[col] = labels

    return house_series, app_series_map, x_labels_map


def plot_owner_usage_trend(raw_house, daily_house, appliance_daily_house, selected_appliances, day_range, period_label, show_household=True, compact=False):
    fig_size = (10.4, 2.7) if compact else (11.2, 4.15)
    fig, ax = plt.subplots(figsize=fig_size)
    fig.patch.set_facecolor("#f0fdf4")
    ax.set_facecolor("#f9fffe")
    start_day, end_day = day_range
    selected_refit_cols = [str(item[0]) for item in selected_appliances]

    use_raw_8s = period_label == "8 seconds"
    if use_raw_8s:
        house_series, app_series_map, raw_x_labels = _make_raw_8_second_series(raw_house, selected_refit_cols, start_day, end_day)
        household_reference = house_series.copy() if not house_series.empty else pd.Series(dtype=float)
    else:
        house_series, app_series_map = _make_day_series_from_daily(daily_house, appliance_daily_house, raw_house, selected_refit_cols, start_day, end_day)
        raw_x_labels = {}
        household_reference = _aggregate_by_period(house_series, period_label) if not house_series.empty else pd.Series(dtype=float)

    plotted = False
    x_labels = None

    if show_household and not household_reference.empty:
        hs = household_reference
        ax.plot(range(len(hs)), hs.values, linewidth=2.4, label="Whole household aggregate", color="#14532d")
        plotted = True
        x_labels = raw_x_labels.get("household", list(hs.index))

    for idx, (refit_col, display_name) in enumerate(selected_appliances):
        s = app_series_map.get(str(refit_col), pd.Series(dtype=float))
        if s.empty:
            continue
        s = s.where(s > 0.0001, np.nan).dropna()
        if s.empty:
            continue
        ag = s if use_raw_8s else _aggregate_by_period(s, period_label)
        ag = _cap_appliance_to_household(ag, household_reference)
        ag = ag.where(ag > 0.0001, np.nan).dropna()
        if ag.empty:
            continue
        if x_labels is None:
            if use_raw_8s:
                labels = raw_x_labels.get(str(refit_col), list(ag.index))
                x_labels = labels[:len(ag)]
            else:
                x_labels = list(ag.index)
        ax.plot(range(len(ag)), ag.values, linewidth=1.9, label=display_name, color=COLORS[(idx + 1) % len(COLORS)])
        plotted = True

    if not plotted:
        plt.close(fig)
        return None

    ax.grid(True, alpha=0.15, color="#16a34a")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#bbf7d0")
    ax.spines["bottom"].set_color("#bbf7d0")
    ax.tick_params(labelsize=8.5, colors="#374151")
    if period_label == "8 seconds":
        ax.set_ylabel("Power (W at native REFIT 8-second samples)", color="#374151")
        ax.set_xlabel("Native REFIT timestamp samples", color="#374151")
    else:
        ax.set_ylabel("Energy (kWh per selected period)", color="#374151")
        ax.set_xlabel("Selected 365-day window", color="#374151")
    title_text = f"Mini usage overview · {period_label} · Days {start_day}-{end_day}" if compact else f"Household and appliance comparison · {period_label} view · Days {start_day}-{end_day}"
    ax.set_title(title_text, fontsize=9.5 if compact else 11, color="#14532d", fontweight="bold")
    if x_labels:
        max_ticks = 10
        step = max(1, len(x_labels) // max_ticks)
        tick_positions = list(range(0, len(x_labels), step))
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([str(x_labels[i]) for i in tick_positions], rotation=35, ha="right")
    ax.legend(frameon=False, fontsize=7.3 if compact else 8.5, loc="upper right")
    plt.tight_layout(pad=0.35 if compact else 0.7)
    return fig


def plot_appliance_pie(apps):
    fig, ax = plt.subplots(figsize=(7.2, 2.75))
    fig.patch.set_facecolor("#f0fdf4")
    ax.set_facecolor("#f0fdf4")
    if apps.empty:
        plt.close(fig)
        return None

    value_col = "cost_month_aud" if "cost_month_aud" in apps.columns else "avg_kwh_day" if "avg_kwh_day" in apps.columns else "total_kwh_window"
    pie_apps = apps.copy().head(9)
    labels = [appliance_name(row) for _, row in pie_apps.iterrows()]
    vals = pd.to_numeric(pie_apps[value_col], errors="coerce").fillna(0)
    valid_mask = vals > 0.01
    vals = vals.loc[valid_mask]
    pie_apps = pie_apps.loc[valid_mask]
    labels = [labels[i] for i, keep in enumerate(valid_mask.tolist()) if keep]

    if vals.empty or vals.sum() <= 0:
        plt.close(fig)
        return None

    green_shades = ["#14532d", "#15803d", "#16a34a", "#22c55e", "#4ade80", "#86efac", "#bbf7d0", "#dcfce7", "#f0fdf4"]

    def autopct(pct):
        return f"{pct:.1f}%" if pct >= 3 else ""

    wedges, texts, autotexts = ax.pie(
        vals,
        labels=None,
        autopct=autopct,
        startangle=90,
        pctdistance=0.75,
        colors=green_shades[:len(vals)],
    )
    ax.axis("equal")

    legend_labels = []
    for label, val in zip(labels, vals):
        if value_col == "cost_month_aud":
            legend_labels.append(f"{label}: ${float(val):.2f}/month")
        else:
            legend_labels.append(f"{label}: {float(val):.4f} kWh/day")

    ax.legend(wedges, legend_labels, title="Appliance share", loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=6.8, title_fontsize=7.3)
    ax.set_title("Cost share by appliance", fontsize=8.8, color="#14532d", fontweight="bold")
    plt.tight_layout(pad=0.5)
    return fig


# ── LOAD ALL DATA ─────────────────────────────────────────────────────────────
house_df, house_path = load_csv(HOUSE_SUMMARY_PATHS)
appliance_df, app_path = load_csv(APPLIANCE_PATHS)
daily_df, daily_path = load_csv(DAILY_PATHS)
appliance_daily_df, appliance_daily_path = load_csv(APPLIANCE_DAILY_PATHS)
raw_df, raw_path = load_csv(RAW_PATHS)
rec_df, rec_path = load_csv(RECOMMENDATION_PATHS)
product_df, product_path = load_csv(PRODUCT_RECOMMENDATION_PATHS)

for df in [house_df, appliance_df, daily_df, appliance_daily_df, raw_df, rec_df, product_df]:
    ensure_numeric(df, [
        "house", "Aggregate", "avg_kwh_day", "cost_month_aud", "cost_day_aud", "total_kwh_window",
        "usage_events_est", "avg_power_w", "max_power_w", "selected_appliances",
        "estimated_total_cost_day_aud_from_selected", "estimated_total_cost_month_aud_from_selected",
        "house_window_days_covered", "mains_days_covered", "aggregate_kwh", "estimated_behaviour_saving_aud_month",
        "estimated_monthly_saving_aud", "estimated_annual_saving_aud", "recommended_price_aud", "payback_months",
        "product_match_score", "current_avg_kwh_day", "current_annual_kwh_est", "current_cost_year_aud",
        "recommended_annual_kwh", "recommended_cost_month_aud", "estimated_energy_saving_kwh_year",
        "saving_score", "energy_efficiency_score", "affordability_score", "payback_score",
        "usage_percentile_vs_similar_houses", "above_similar_house_avg_pct", "benchmark_avg_kwh_day",
        "benchmark_avg_cost_month_aud", "behaviour_saving_pct_of_appliance_cost",
        "combined_behaviour_product_saving_aud_month", "best_product_saving_aud_month",
        "balanced_intelligent_score", "budget_user_score", "eco_user_score", "fast_payback_score"
    ])

appliance_df = apply_refit_names(appliance_df)
rec_df = apply_refit_names(rec_df)
appliance_daily_df = apply_refit_names(appliance_daily_df)
product_df = apply_refit_names(product_df)

# ── PAGE HEADER MOVED INTO HOME OVERVIEW TAB ───────────────────────────────

if appliance_df.empty or "house" not in appliance_df.columns:
    st.error("No REFIT output files found. Run your REFIT 365-day pipeline first, then refresh this app.")
    st.stop()

available_houses = sorted(appliance_df["house"].dropna().astype(int).unique().tolist())

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🌿 House Settings")
    selected_house = st.selectbox("Select your house", available_houses, index=0)
    user_goal = st.selectbox(
        "My main goal",
        ["Balanced", "Lowest upfront cost", "Energy saving", "Fastest payback"],
        index=0,
        help="Changes how product options are ranked in the recommendation system.",
    )
    budget_limit = st.slider("Maximum product budget (AUD)", 25, 1000, 300, step=25)
    show_owner_table = st.checkbox("Show raw data table", value=False)
    st.caption("Intelligent behaviour, product and cross-house recommendations for your home.")

# ── FILTER DATA FOR SELECTED HOUSE ───────────────────────────────────────────
apps = appliance_df[appliance_df["house"].astype(int) == int(selected_house)].copy()
if "cost_month_aud" not in apps.columns:
    if "avg_kwh_day" in apps.columns:
        apps["cost_month_aud"] = apps["avg_kwh_day"] * TARIFF_AUD * 30
    elif "total_kwh_window" in apps.columns:
        apps["cost_month_aud"] = apps["total_kwh_window"] * TARIFF_AUD * 30
    else:
        apps["cost_month_aud"] = 0.0
if "avg_kwh_day" not in apps.columns:
    apps["avg_kwh_day"] = apps["total_kwh_window"] if "total_kwh_window" in apps.columns else 0.0
for _col in ["avg_kwh_day", "cost_day_aud", "cost_month_aud", "total_kwh_window", "avg_power_w"]:
    if _col in apps.columns:
        apps[_col] = pd.to_numeric(apps[_col], errors="coerce").fillna(0).clip(lower=0.01)
apps = apps.sort_values("cost_month_aud", ascending=False).reset_index(drop=True)

house_row = house_df[house_df["house"].astype(int) == int(selected_house)].copy() if not house_df.empty and "house" in house_df.columns else pd.DataFrame()
daily_house = daily_df[daily_df["house"].astype(int) == int(selected_house)].copy() if not daily_df.empty and "house" in daily_df.columns else pd.DataFrame()
appliance_daily_house = appliance_daily_df[appliance_daily_df["house"].astype(int) == int(selected_house)].copy() if not appliance_daily_df.empty and "house" in appliance_daily_df.columns else pd.DataFrame()
raw_house = raw_df[raw_df["house"].astype(int) == int(selected_house)].copy() if not raw_df.empty and "house" in raw_df.columns else pd.DataFrame()
rec_house = rec_df[rec_df["house"].astype(int) == int(selected_house)].copy() if not rec_df.empty and "house" in rec_df.columns else pd.DataFrame()
product_house = product_df[product_df["house"].astype(int) == int(selected_house)].copy() if not product_df.empty and "house" in product_df.columns else pd.DataFrame()

tracked_appliances = len(apps)
total_kwh = float(pd.to_numeric(apps["avg_kwh_day"], errors="coerce").fillna(0).sum())
monthly_cost = float(pd.to_numeric(apps["cost_month_aud"], errors="coerce").fillna(0).sum())
events = int(pd.to_numeric(apps["usage_events_est"], errors="coerce").fillna(0).sum()) if "usage_events_est" in apps.columns else 0
avg_power = float(pd.to_numeric(apps["avg_power_w"], errors="coerce").fillna(0).mean()) if "avg_power_w" in apps.columns else 0.0
daily_cost = monthly_cost / 30 if monthly_cost else total_kwh * TARIFF_AUD

if not house_row.empty:
    if "estimated_total_cost_day_aud_from_selected" in house_row.columns:
        daily_cost = snum(house_row.iloc[0]["estimated_total_cost_day_aud_from_selected"])
    if "estimated_total_cost_month_aud_from_selected" in house_row.columns:
        monthly_cost = snum(house_row.iloc[0]["estimated_total_cost_month_aud_from_selected"])

# ══════════════════════════════════════════════════════════════════════════════
#  MAIN NAVIGATION TABS
# ══════════════════════════════════════════════════════════════════════════════
tab_home, tab_trends, tab_advisor, tab_picks = st.tabs([
    "🏠  Home Overview",
    "📊  Usage Trends",
    "💡  Appliance Advisor",
    "🏆  Best Picks & Savings",
])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — BEST PICKS & SAVINGS
#  (Hero product cards + top behaviour + top product summary)
# ══════════════════════════════════════════════════════════════════════════════
with tab_picks:
    st.markdown(f"### 🏆 Best Product Replacements — House {selected_house}")
    st.markdown("<div class='soft-note' style='margin-bottom:0.9rem;'>The three cards below show the best product replacements for this house — sorted by your goal. Price, appliance, and store are shown front and centre.</div>", unsafe_allow_html=True)

    if product_house.empty:
        st.markdown("""
        <div class='phero-empty'>
            🌿 No product recommendation data was found for this house.<br>
            Run the advanced pipeline first, then reload this app.
        </div>
        """, unsafe_allow_html=True)
    else:
        ph_top = product_house.copy()
        for col in ["recommended_price_aud", "recommended_annual_kwh", "estimated_monthly_saving_aud",
                    "estimated_annual_saving_aud", "payback_months", "product_match_score",
                    "estimated_energy_saving_kwh_year", "balanced_intelligent_score",
                    "budget_user_score", "eco_user_score", "fast_payback_score"]:
            if col in ph_top.columns:
                ph_top[col] = pd.to_numeric(ph_top[col], errors="coerce")

        budget_filtered_top = ph_top[ph_top["recommended_price_aud"].fillna(999999) <= budget_limit].copy()
        if budget_filtered_top.empty:
            budget_filtered_top = ph_top.copy()

        top_score_col = {
            "Balanced": "balanced_intelligent_score",
            "Lowest upfront cost": "budget_user_score",
            "Energy saving": "eco_user_score",
            "Fastest payback": "fast_payback_score",
        }.get(user_goal, "balanced_intelligent_score")
        if top_score_col not in budget_filtered_top.columns:
            top_score_col = "product_match_score" if "product_match_score" in budget_filtered_top.columns else "estimated_monthly_saving_aud"

        cheapest_top = budget_filtered_top.sort_values("recommended_price_aud", ascending=True).iloc[0]
        if "recommended_annual_kwh" in budget_filtered_top.columns:
            energy_top = budget_filtered_top.sort_values(["recommended_annual_kwh", "recommended_price_aud"], ascending=[True, True]).iloc[0]
        else:
            energy_top = budget_filtered_top.sort_values("estimated_monthly_saving_aud", ascending=False).iloc[0]
        overall_top = budget_filtered_top.sort_values([top_score_col, "estimated_monthly_saving_aud"], ascending=[False, False]).iloc[0]

        def _hero_card(row, badge_label, icon, is_best=False):
            best_class = "phero phero-best" if is_best else "phero"
            prod_name = appliance_name(row) if appliance_name(row) != "Appliance" else str(row.get("recommended_product", "Recommended Product"))
            store = str(row.get("recommended_store", "Store"))
            price_raw = row.get("recommended_price_aud", np.nan)
            price_str = money(price_raw)
            saving_mo = money(row.get("estimated_monthly_saving_aud", np.nan))
            saving_yr = money(row.get("estimated_annual_saving_aud", np.nan))
            payback_raw = row.get("payback_months", np.nan)
            payback_str = "n/a" if pd.isna(payback_raw) else f"{float(payback_raw):.1f} mo"
            energy_kwh = row.get("estimated_energy_saving_kwh_year", row.get("recommended_annual_kwh", np.nan))
            energy_str = "n/a" if pd.isna(energy_kwh) else f"{float(energy_kwh):.0f} kWh/yr"
            product_line = str(row.get("recommended_product", ""))
            brand_line = str(row.get("recommended_brand", ""))
            product_detail = f"{product_line}" + (f" · {brand_line}" if brand_line and brand_line != "nan" else "")

            return f"""
            <div class='{best_class}'>
                <div class='phero-badge'>{icon} {badge_label}</div>
                <div class='phero-appliance'>{prod_name}</div>
                <div><span class='phero-store'>🏪 {store}</span></div>
                <div class='phero-price-label'>Price</div>
                <div class='phero-price'>{price_str}</div>
                <hr class='phero-divider'>
                <div style='font-size:0.82rem; color:#4b5563; margin-bottom:0.65rem;'>{product_detail}</div>
                <div class='phero-stats'>
                    <div class='phero-stat'>
                        <div class='phero-stat-label'>Save / Month</div>
                        <div class='phero-stat-value'>{saving_mo}</div>
                    </div>
                    <div class='phero-stat'>
                        <div class='phero-stat-label'>Energy Saving</div>
                        <div class='phero-stat-value'>{energy_str}</div>
                    </div>
                    <div class='phero-stat'>
                        <div class='phero-stat-label'>Payback</div>
                        <div class='phero-stat-value'>{payback_str}</div>
                    </div>
                </div>
            </div>
            """

        hero_col1, hero_col2, hero_col3 = st.columns(3)
        with hero_col1:
            st.markdown(_hero_card(cheapest_top, "Cost Option", "💰", is_best=False), unsafe_allow_html=True)
        with hero_col2:
            st.markdown(_hero_card(overall_top, "Overall Best", "🏆", is_best=True), unsafe_allow_html=True)
        with hero_col3:
            st.markdown(_hero_card(energy_top, "Energy Wise", "🌱", is_best=False), unsafe_allow_html=True)

    # ── Top Behaviour + Product Summary ──────────────────────────────────────
    st.markdown("---")

    def _short_action(text, max_words=16):
        if pd.isna(text):
            return "Reduce avoidable usage and monitor this appliance."
        clean = " ".join(str(text).strip().split())
        if not clean:
            return "Reduce avoidable usage and monitor this appliance."
        words = clean.split()
        return " ".join(words[:max_words]) + ("..." if len(words) > max_words else "")

    def _safe(value, fallback=""):
        if pd.isna(value):
            return fallback
        return escape(str(value))

    def _render_html(markup):
        """Render custom HTML safely without Markdown treating indented HTML as a code block."""
        clean = dedent(markup).strip()
        clean = "\n".join(line.strip() for line in clean.splitlines())
        st.markdown(clean, unsafe_allow_html=True)

    # Behaviour recommendations: show only the strongest 3 wins.
    if rec_house.empty:
        rec_show = pd.DataFrame()
        top_behaviour_name = "No data"
        top_behaviour_saving = 0.0
        top3_behaviour_total = 0.0
    else:
        sort_col = "estimated_behaviour_saving_aud_month" if "estimated_behaviour_saving_aud_month" in rec_house.columns else "cost_month_aud"
        rec_show = rec_house.copy()
        if sort_col in rec_show.columns:
            rec_show[sort_col] = pd.to_numeric(rec_show[sort_col], errors="coerce").fillna(0)
            rec_show = rec_show.sort_values(sort_col, ascending=False)
        rec_show = rec_show.head(3)
        top_behaviour_name = appliance_name(rec_show.iloc[0]) if not rec_show.empty else "No data"
        top_behaviour_saving = snum(rec_show.iloc[0].get("estimated_behaviour_saving_aud_month", 0)) if not rec_show.empty else 0.0
        top3_behaviour_total = rec_show["estimated_behaviour_saving_aud_month"].apply(snum).sum() if "estimated_behaviour_saving_aud_month" in rec_show.columns else 0.0

    # Product recommendations: rank by selected goal, then show a compact top 3.
    if product_house.empty:
        ph_show = pd.DataFrame()
        top_product_name = "No data"
        top_product_saving = 0.0
        top_product_payback = np.nan
    else:
        ph = product_house.copy()
        for col in ["estimated_monthly_saving_aud", "recommended_price_aud", "payback_months", "balanced_intelligent_score", "product_match_score"]:
            if col in ph.columns:
                ph[col] = pd.to_numeric(ph[col], errors="coerce")
        top_score_col = "balanced_intelligent_score" if "balanced_intelligent_score" in ph.columns else "product_match_score" if "product_match_score" in ph.columns else "estimated_monthly_saving_aud"
        if top_score_col in ph.columns and "estimated_monthly_saving_aud" in ph.columns:
            ph = ph.sort_values([top_score_col, "estimated_monthly_saving_aud"], ascending=[False, False])
        elif "estimated_monthly_saving_aud" in ph.columns:
            ph = ph.sort_values("estimated_monthly_saving_aud", ascending=False)

        # Avoid showing repeated versions of the same appliance where possible.
        unique_key = next((c for c in ["appliance_label", "appliance_type", "real_appliance_name", "refit_column"] if c in ph.columns), None)
        if unique_key:
            ph_unique = ph.drop_duplicates(subset=[unique_key]).head(3)
            if len(ph_unique) < 3:
                ph_show = pd.concat([ph_unique, ph.drop(ph_unique.index, errors="ignore")]).head(3)
            else:
                ph_show = ph_unique
        else:
            unique_product_cols = [c for c in ["recommended_product", "recommended_store"] if c in ph.columns]
            ph_show = ph.drop_duplicates(subset=unique_product_cols).head(3) if unique_product_cols else ph.head(3)

        if not ph_show.empty:
            top_row = ph_show.iloc[0]
            top_product_name = top_row.get("recommended_product", appliance_name(top_row))
            top_product_saving = snum(top_row.get("estimated_monthly_saving_aud", 0))
            top_product_payback = top_row.get("payback_months", np.nan)
        else:
            top_product_name = "No data"
            top_product_saving = 0.0
            top_product_payback = np.nan

    payback_summary = "n/a" if pd.isna(top_product_payback) else f"{float(top_product_payback):.1f} mo"

    _render_html(f"""
    <div class='glance-header'>
        <div class='glance-kicker'>Savings at a glance</div>
        <div class='glance-title'>Top behaviour + product opportunities</div>
        <div class='glance-sub'>A shorter card summary of the best actions for this selected house.</div>
    </div>
    """)

    sum_col1, sum_col2, sum_col3 = st.columns(3)
    with sum_col1:
        _render_html(f"""
        <div class='summary-stat-card'>
            <div class='summary-label'>Best behaviour win</div>
            <div class='summary-value'>{money(top_behaviour_saving)}</div>
            <div class='summary-name'>🧠 {_safe(top_behaviour_name)}</div>
            <div class='summary-note'>Estimated monthly saving, no purchase needed</div>
        </div>
        """)
    with sum_col2:
        _render_html(f"""
        <div class='summary-stat-card'>
            <div class='summary-label'>Top 3 behaviour total</div>
            <div class='summary-value'>{money(top3_behaviour_total)}</div>
            <div class='summary-name'>Quick actions combined</div>
            <div class='summary-note'>Use this as the practical monthly target</div>
        </div>
        """)
    with sum_col3:
        _render_html(f"""
        <div class='summary-stat-card'>
            <div class='summary-label'>Best product payback</div>
            <div class='summary-value'>{payback_summary}</div>
            <div class='summary-name'>🛒 {_safe(top_product_name)}</div>
            <div class='summary-note'>{money(top_product_saving)}/month estimated saving</div>
        </div>
        """)

    rec_left, rec_right = st.columns([1.05, 1.05])
    with rec_left:
        if rec_show.empty:
            _render_html("""
            <div class='summary-panel'>
                <div class='summary-panel-title'>
                    <div><div class='summary-panel-title-main'>🧠 Quickest behaviour wins</div><div class='summary-panel-sub'>No purchase needed</div></div>
                    <span class='summary-count-pill'>0 actions</span>
                </div>
                <div class='soft-note'>No behaviour recommendation file found. Run the pipeline first.</div>
            </div>
            """)
        else:
            cards_html = []
            for _, row in rec_show.iterrows():
                name = appliance_name(row)
                priority = str(row.get("behaviour_priority", "normal")).title()
                saving = snum(row.get("estimated_behaviour_saving_aud_month", 0))
                text = _short_action(row.get("behaviour_recommendation", "Monitor this appliance and reduce unnecessary usage where possible."))
                cards_html.append(dedent(f"""
                <div class='compact-rec-card'>
                    <div class='compact-rec-top'>
                        <div class='compact-rec-name'>🧠 {_safe(name)}</div>
                        <span class='compact-rec-price'>{money(saving)}/mo</span>
                    </div>
                    <div class='compact-rec-body'>{_safe(text)}</div>
                    <div class='compact-rec-meta'>
                        <span class='compact-rec-pill'>{_safe(priority)}</span>
                        <span class='compact-rec-pill'>No purchase</span>
                    </div>
                </div>
                """).strip())
            _render_html(f"""
            <div class='summary-panel'>
                <div class='summary-panel-title'>
                    <div><div class='summary-panel-title-main'>🧠 Quickest behaviour wins</div><div class='summary-panel-sub'>Top 3 actions you can try today</div></div>
                    <span class='summary-count-pill'>{len(rec_show)} actions</span>
                </div>
                {''.join(cards_html)}
            </div>
            """)

    with rec_right:
        if ph_show.empty:
            _render_html("""
            <div class='summary-panel'>
                <div class='summary-panel-title'>
                    <div><div class='summary-panel-title-main'>🛒 Best product upgrades</div><div class='summary-panel-sub'>Ranked by selected goal</div></div>
                    <span class='summary-count-pill'>0 options</span>
                </div>
                <div class='soft-note'>No product recommendation file found. Run the pipeline first.</div>
            </div>
            """)
        else:
            cards_html = []
            for _, row in ph_show.iterrows():
                name = appliance_name(row)
                store = row.get("recommended_store", "Store")
                product = row.get("recommended_product", "Recommended product")
                price = money(row.get("recommended_price_aud", np.nan))
                saving = money(row.get("estimated_monthly_saving_aud", np.nan))
                payback = row.get("payback_months", np.nan)
                payback_text = "n/a" if pd.isna(payback) else f"{float(payback):.1f} mo"
                cards_html.append(dedent(f"""
                <div class='compact-rec-card'>
                    <div class='compact-rec-top'>
                        <div class='compact-rec-name'>🛒 {_safe(name)}</div>
                        <span class='compact-rec-price'>{price}</span>
                    </div>
                    <div class='compact-rec-body'><b>{_safe(product)}</b></div>
                    <div class='compact-rec-meta'>
                        <span class='compact-rec-pill'>{_safe(store)}</span>
                        <span class='compact-rec-pill'>{saving}/mo</span>
                        <span class='compact-rec-pill'>Payback {payback_text}</span>
                    </div>
                </div>
                """).strip())
            _render_html(f"""
            <div class='summary-panel'>
                <div class='summary-panel-title'>
                    <div><div class='summary-panel-title-main'>🛒 Best product upgrades</div><div class='summary-panel-sub'>Top 3, ranked by your selected goal</div></div>
                    <span class='summary-count-pill'>{len(ph_show)} options</span>
                </div>
                {''.join(cards_html)}
            </div>
            """)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — HOME OVERVIEW
#  (Two-column landing dashboard: overview/trends left, picks/pie/advice right)
# ══════════════════════════════════════════════════════════════════════════════
with tab_home:
    def _landing_html(markup):
        clean = dedent(markup).strip()
        clean = "\n".join(line.strip() for line in clean.splitlines())
        st.markdown(clean, unsafe_allow_html=True)

    def _safe_text(value, fallback=""):
        if pd.isna(value):
            return fallback
        return escape(str(value))

    def _pick_rows_for_house():
        if product_house.empty:
            return None, None, None
        ph = product_house.copy()
        numeric_cols = [
            "recommended_price_aud", "estimated_monthly_saving_aud", "estimated_annual_saving_aud",
            "payback_months", "estimated_energy_saving_kwh_year", "recommended_annual_kwh",
            "balanced_intelligent_score", "budget_user_score", "eco_user_score", "fast_payback_score",
            "product_match_score"
        ]
        for col in numeric_cols:
            if col in ph.columns:
                ph[col] = pd.to_numeric(ph[col], errors="coerce")

        if "recommended_price_aud" in ph.columns:
            budget_ph = ph[ph["recommended_price_aud"].fillna(999999) <= budget_limit].copy()
            if budget_ph.empty:
                budget_ph = ph.copy()
        else:
            budget_ph = ph.copy()

        score_col = {
            "Balanced": "balanced_intelligent_score",
            "Lowest upfront cost": "budget_user_score",
            "Energy saving": "eco_user_score",
            "Fastest payback": "fast_payback_score",
        }.get(user_goal, "balanced_intelligent_score")
        if score_col not in budget_ph.columns:
            score_col = "product_match_score" if "product_match_score" in budget_ph.columns else "estimated_monthly_saving_aud"

        cheapest = budget_ph.sort_values("recommended_price_aud", ascending=True).iloc[0] if "recommended_price_aud" in budget_ph.columns else budget_ph.iloc[0]
        if "estimated_energy_saving_kwh_year" in budget_ph.columns:
            energy = budget_ph.sort_values(["estimated_energy_saving_kwh_year", "estimated_monthly_saving_aud"], ascending=[False, False]).iloc[0]
        elif "recommended_annual_kwh" in budget_ph.columns:
            energy = budget_ph.sort_values(["recommended_annual_kwh", "recommended_price_aud"], ascending=[True, True]).iloc[0]
        else:
            energy = budget_ph.sort_values("estimated_monthly_saving_aud", ascending=False).iloc[0]
        if score_col in budget_ph.columns and "estimated_monthly_saving_aud" in budget_ph.columns:
            overall = budget_ph.sort_values([score_col, "estimated_monthly_saving_aud"], ascending=[False, False]).iloc[0]
        elif "estimated_monthly_saving_aud" in budget_ph.columns:
            overall = budget_ph.sort_values("estimated_monthly_saving_aud", ascending=False).iloc[0]
        else:
            overall = budget_ph.iloc[0]
        return cheapest, overall, energy

    def _right_pick_card(row, title, icon, highlight=False):
        if row is None:
            return ""
        appliance = appliance_name(row)
        store = _safe_text(row.get("recommended_store", "Store"), "Store")
        price = money(row.get("recommended_price_aud", np.nan))
        saving = money(row.get("estimated_monthly_saving_aud", np.nan))
        payback_raw = row.get("payback_months", np.nan)
        payback = "n/a" if pd.isna(payback_raw) else f"{float(payback_raw):.1f} mo"
        energy_raw = row.get("estimated_energy_saving_kwh_year", row.get("recommended_annual_kwh", np.nan))
        energy = "n/a" if pd.isna(energy_raw) else f"{float(energy_raw):.0f} kWh/yr"
        product = _safe_text(row.get("recommended_product", "Recommended product"), "Recommended product")
        brand = _safe_text(row.get("recommended_brand", ""), "")
        detail = product + (f" · {brand}" if brand and brand.lower() != "nan" else "")
        badge_style = "background:#14532d;" if highlight else ""
        return dedent(f"""
        <div class='right-pick-card'>
            <div class='right-pick-head'>
                <div>
                    <span class='right-pick-badge' style='{badge_style}'>{icon} {title}</span>
                    <div class='right-pick-appliance'>{_safe_text(appliance)}</div>
                    <div class='right-pick-store'>🏪 {store}</div>
                </div>
                <div class='right-pick-price'>{price}</div>
            </div>
            <div class='right-pick-product'>{detail}</div>
            <div class='right-pick-stats'>
                <div class='right-pick-stat'><div class='right-pick-stat-label'>Save / mo</div><div class='right-pick-stat-value'>{saving}</div></div>
                <div class='right-pick-stat'><div class='right-pick-stat-label'>Energy</div><div class='right-pick-stat-value'>{energy}</div></div>
                <div class='right-pick-stat'><div class='right-pick-stat-label'>Payback</div><div class='right-pick-stat-value'>{payback}</div></div>
            </div>
        </div>
        """).strip()

    def _render_home_usage_trends(key_prefix="home"):
        trend_apps = apps.copy().reset_index(drop=True)
        trend_apps["_display_name"] = [appliance_name(row) for _, row in trend_apps.iterrows()] if not trend_apps.empty else []
        if trend_apps.empty:
            st.markdown("<div class='soft-note'>No appliance records found for this house.</div>", unsafe_allow_html=True)
            return

        c1, c2, c3 = st.columns([0.95, 1.25, 1.05], gap="small")
        with c1:
            period_label = st.radio(
                "Summary scale",
                ["Weekly", "Monthly", "Three months"],
                horizontal=True,
                index=1,
                key=f"{key_prefix}_usage_period_mode",
                help="The home page only shows clean summary views. Open Usage Trends for 8-second and day-by-day charts.",
            )
        with c2:
            day_range = st.slider(
                "Dashboard day window",
                min_value=1,
                max_value=365,
                value=(1, 365),
                step=1,
                key=f"{key_prefix}_owner_usage_trend_days",
            )
        appliance_options = trend_apps["_display_name"].tolist()
        with c3:
            selected_trend_name = st.selectbox(
                "Highlight appliance",
                appliance_options,
                index=0,
                key=f"{key_prefix}_owner_usage_single_appliance_select",
            )

        st.markdown("<div class='home-trend-note'>Home overview uses weekly/monthly/three-month summaries to keep the dashboard clean. Use the Usage Trends tab for the full 8-second and daily view.</div>", unsafe_allow_html=True)

        selected_pairs = []
        one = trend_apps[trend_apps["_display_name"] == selected_trend_name]
        if not one.empty:
            row = one.iloc[0]
            refit_col = row.get("original_refit_column", row.get("refit_column", selected_trend_name))
            selected_pairs.append((refit_col, selected_trend_name))

        fig = plot_owner_usage_trend(
            raw_house,
            daily_house,
            appliance_daily_house,
            selected_pairs,
            day_range,
            period_label,
            show_household=True,
            compact=True,
        )
        if fig is not None:
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.markdown("<div class='soft-note'>No matching trend data was available for the selected day range/appliance.</div>", unsafe_allow_html=True)

    left_col, right_col = st.columns([1.08, 0.92], gap="medium")

    with left_col:
        _landing_html(f"""
        <div class='landing-header-card'>
            <div class='landing-header-eyebrow'>REFIT household dashboard</div>
            <div class='landing-header-title'>Smart House Energy Advisor</div>
            <div class='landing-header-sub'>A compact owner dashboard for costs, trends, savings, and next actions.</div>
            <span class='landing-house-pill'>House {selected_house}</span>
        </div>
        """)

        _landing_html(f"""
        <div class='landing-kpi-grid'>
            <div class='landing-kpi-card'><div class='landing-kpi-label'>Appliances tracked</div><div class='landing-kpi-value'>{tracked_appliances}</div><div class='landing-kpi-sub'>Real REFIT appliance names</div></div>
            <div class='landing-kpi-card'><div class='landing-kpi-label'>Cost per day</div><div class='landing-kpi-value'>{money(daily_cost)}</div><div class='landing-kpi-sub'>Estimated from your house data</div></div>
            <div class='landing-kpi-card'><div class='landing-kpi-label'>Monthly bill impact</div><div class='landing-kpi-value'>{money(monthly_cost)}</div><div class='landing-kpi-sub'>Estimated owner bill</div></div>
            <div class='landing-kpi-card'><div class='landing-kpi-label'>Usage events</div><div class='landing-kpi-value'>{events}</div><div class='landing-kpi-sub'>Estimated active samples / events</div></div>
            <div class='landing-kpi-card'><div class='landing-kpi-label'>Average draw</div><div class='landing-kpi-value'>{avg_power:.1f} W</div><div class='landing-kpi-sub'>Mean appliance power across house</div></div>
        </div>
        """)

        top_left = apps.iloc[0] if not apps.empty else None
        second_left = apps.iloc[1] if len(apps) > 1 else top_left
        top_left_name = appliance_name(top_left) if top_left is not None else "No data"
        second_left_name = appliance_name(second_left) if second_left is not None else "No data"
        top_left_cost = snum(top_left.get("cost_month_aud", 0)) if top_left is not None else 0
        second_left_events = int(snum(second_left.get("usage_events_est", 0))) if second_left is not None else 0
        best_daily_kwh = snum(top_left.get("avg_kwh_day", 0)) if top_left is not None else 0

        _landing_html(f"""
        <div class='home-mini-grid'>
            <div class='home-mini-card'>
                <div class='home-mini-label'>Main cost driver</div>
                <div class='home-mini-value'>💸 {_safe_text(top_left_name)}</div>
                <div class='home-mini-note'>Highest current monthly impact: <b>{money(top_left_cost)}/month</b>.</div>
            </div>
            <div class='home-mini-card'>
                <div class='home-mini-label'>Usage signal</div>
                <div class='home-mini-value'>🔁 {_safe_text(second_left_name)}</div>
                <div class='home-mini-note'>Detected activity count shown as <b>{second_left_events}</b> events/samples.</div>
            </div>
            <div class='home-mini-card'>
                <div class='home-mini-label'>Energy focus</div>
                <div class='home-mini-value'>⚡ {best_daily_kwh:.3f} kWh/day</div>
                <div class='home-mini-note'>Use the snapshot below to compare household vs highlighted appliance.</div>
            </div>
        </div>
        """)

        st.markdown("<div class='landing-panel'><div class='landing-panel-title'>📊 Usage Snapshot</div><div class='landing-panel-sub'>Clean weekly, monthly, or three-month trend summary for the selected house.</div></div>", unsafe_allow_html=True)
        _render_home_usage_trends(key_prefix="home_landing")

        if show_owner_table:
            st.markdown("<div class='landing-panel'><div class='landing-panel-title'>Raw Appliance Data Table</div><div class='landing-panel-sub'>Detailed appliance-level values used by the dashboard.</div></div>", unsafe_allow_html=True)
            show_cols = [c for c in ["real_appliance_name", "original_refit_column", "appliance_label", "appliance_type", "refit_column", "avg_power_w", "max_power_w", "avg_kwh_day", "cost_day_aud", "cost_month_aud", "usage_events_est", "intelligent_efficiency_class", "usage_percentile_vs_similar_houses", "above_similar_house_avg_pct", "behaviour_recommendation", "estimated_behaviour_saving_aud_month", "intelligent_recommendation_summary", "recommendation"] if c in apps.columns]
            st.dataframe(apps[show_cols], use_container_width=True, height=300)

    with right_col:
        cheapest_row, overall_row, energy_row = _pick_rows_for_house()
        if product_house.empty:
            _landing_html(f"""
            <div class='landing-panel'>
                <div class='landing-panel-title'>🏆 Best Picks — House {selected_house}</div>
                <div class='landing-panel-sub'>No product recommendation data found for this house. Run the product recommendation pipeline first.</div>
            </div>
            """)
        else:
            _landing_html(f"""
            <div class='landing-panel'>
                <div class='landing-panel-title'>🏆 Best Picks — House {selected_house}</div>
                <div class='landing-panel-sub'>Three compact upgrade views based on your selected goal and budget.</div>
                <div class='right-picks-grid'>
                    {_right_pick_card(cheapest_row, "Cost", "💰")}
                    {_right_pick_card(overall_row, "Best", "🏆", highlight=True)}
                    {_right_pick_card(energy_row, "Energy", "🌱")}
                </div>
            </div>
            """)

        st.markdown(f"<div class='landing-panel'><div class='landing-panel-title'>🥧 Cost Share</div><div class='landing-panel-sub'>Largest appliance contributors to the monthly cost.</div></div>", unsafe_allow_html=True)
        fig = plot_appliance_pie(apps.head(9))
        if fig is not None:
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
        else:
            st.markdown("<div class='soft-note'>No pie chart could be created for this house.</div>", unsafe_allow_html=True)

        if apps.empty:
            _landing_html(f"""
            <div class='landing-panel'>
                <div class='landing-panel-title'>📝 Plain-Language Advice — House {selected_house}</div>
                <div class='landing-panel-sub'>No advice can be generated because no appliance data is available.</div>
            </div>
            """)
        else:
            top = apps.iloc[0]
            top_name = appliance_name(top)
            top_cost = snum(top.get("cost_month_aud", 0))
            intel_class = str(top.get("intelligent_efficiency_class", "Needs review"))
            similar_pct = top.get("above_similar_house_avg_pct", np.nan)
            peak_pct = snum(top.get("peak_hour_active_share", top.get("peak_usage_share", 0))) * 100
            events_top = int(snum(top.get("usage_events_est", 0)))
            if pd.notna(similar_pct):
                benchmark_text = f"{top_name} is classified as {intel_class}. It is {abs(float(similar_pct)):.1f}% {'above' if float(similar_pct) >= 0 else 'below'} the similar-appliance average."
            else:
                benchmark_text = f"{top_name} is classified as {intel_class}. Use the appliance advisor for deeper comparison."
            _landing_html(f"""
            <div class='landing-panel'>
                <div class='landing-panel-title'>📝 Plain-Language Advice — House {selected_house}</div>
                <div class='landing-panel-sub'>What the data says about your home's energy use.</div>
                <div class='advice-stack'>
                    <div class='advice-item'><div class='advice-title'>Cost driver</div><div class='advice-text'><b>{_safe_text(top_name)}</b> is the highest cost appliance at about <b>{money(top_cost)}/month</b>.</div></div>
                    <div class='advice-item'><div class='advice-title'>Usage benchmark</div><div class='advice-text'>{_safe_text(benchmark_text)} Events: <b>{events_top}</b>{' · Peak: <b>' + f'{peak_pct:.1f}%' + '</b>' if peak_pct > 0 else ''}.</div></div>
                    <div class='advice-item'><div class='advice-title'>Next action</div><div class='advice-text'>Open <b>Appliance Advisor</b> for behaviour, product, and combined savings options.</div></div>
                </div>
            </div>
            """)

# ══════════════════════════════════════════════════════════════════════════════
#  TAB 3 — USAGE TRENDS
#  (Trend chart full-width)
# ══════════════════════════════════════════════════════════════════════════════
with tab_trends:
    st.markdown(f"### 📊 Energy Usage Trends — House {selected_house}")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    section("Household & Appliance Usage Over Time", "Compare whole-house aggregate and individual appliances across the 365-day window")

    trend_apps = apps.copy().reset_index(drop=True)
    trend_apps["_display_name"] = [appliance_name(row) for _, row in trend_apps.iterrows()] if not trend_apps.empty else []

    if trend_apps.empty:
        st.markdown("<div class='soft-note'>No appliance records found for this house.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='chart-title-card'>House " + str(selected_house) + " — Household and appliance line comparison</div>", unsafe_allow_html=True)
        c_period, c_house_chk = st.columns([1.0, 1.0])
        with c_period:
            period_label = st.radio(
                "Time resolution",
                ["8 seconds", "Day by day", "Weekly", "Monthly", "Three months"],
                horizontal=True,
                index=0,
                key="owner_usage_period_mode",
                help="8 seconds shows native REFIT power samples. Day by day shows each day individually. Weekly/Monthly/Three months aggregate data for a cleaner overview.",
            )
        with c_house_chk:
            show_household_line = st.checkbox("Show whole-house total line", value=True, key="show_household_line")

        st.markdown("<div class='slider-heading'>Navigate the 365-day window</div>", unsafe_allow_html=True)
        day_range = st.slider(
            "Day range",
            min_value=1,
            max_value=365,
            value=(1, 45),
            step=1,
            key="owner_usage_trend_days",
            help="Drag the handles to focus on a specific part of the year.",
        )

        st.markdown("<div class='slider-heading'>Select appliances to overlay on the chart</div>", unsafe_allow_html=True)
        appliance_options = trend_apps["_display_name"].tolist()
        default_appliances = appliance_options[:1]
        selected_trend_names = st.multiselect(
            "Choose appliances",
            appliance_options,
            default=default_appliances,
            key="owner_usage_multi_appliance_select",
            help="Pick one or more appliances. Each adds a coloured line to the chart.",
        )

        selected_pairs = []
        for trend_name in selected_trend_names:
            trend_row = trend_apps[trend_apps["_display_name"] == trend_name].iloc[0]
            trend_refit_col = str(trend_row.get("refit_column", trend_row.get("original_refit_column", ""))).strip()
            selected_pairs.append((trend_refit_col, trend_name))

        fig = plot_owner_usage_trend(
            raw_house=raw_house,
            daily_house=daily_house,
            appliance_daily_house=appliance_daily_house,
            selected_appliances=selected_pairs,
            day_range=day_range,
            period_label=period_label,
            show_household=show_household_line,
        )
        if fig is not None:
            st.pyplot(fig, use_container_width=True)
            plt.close(fig)
            selected_text = ", ".join(selected_trend_names) if selected_trend_names else "no appliances selected"
            st.markdown(
                f"<div class='soft-note'>Showing Day {day_range[0]} to Day {day_range[1]} for House {selected_house}. Resolution: <b>{period_label}</b>. Lines shown: <b>{'whole household, ' if show_household_line else ''}{selected_text}</b>.</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown("<div class='soft-note'>No trend data available for this selection. Keep the whole-house line checked or select at least one appliance that has daily data available.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 4 — APPLIANCE ADVISOR
#  (Interactive per-appliance deep dive with sub-tabs)
# ══════════════════════════════════════════════════════════════════════════════
with tab_advisor:
    def _advisor_safe(value, fallback=""):
        try:
            if pd.isna(value):
                return fallback
        except Exception:
            pass
        text = str(value).strip()
        return escape(text) if text else fallback

    def _advisor_snippet(value, words=18, fallback="No extra explanation available."):
        text = _advisor_safe(value, fallback)
        plain = " ".join(text.split())
        parts = plain.split()
        return " ".join(parts[:words]) + ("..." if len(parts) > words else "")

    def _advisor_html(markup):
        clean = dedent(markup).strip()
        clean = "\n".join(line.strip() for line in clean.splitlines())
        st.markdown(clean, unsafe_allow_html=True)

    def _metric_block(label, value, note=""):
        return f"""
        <div class='advisor-mini-metric'>
            <div class='advisor-mini-label'>{_advisor_safe(label)}</div>
            <div class='advisor-mini-value'>{_advisor_safe(value)}</div>
            <div class='advisor-mini-note'>{_advisor_safe(note)}</div>
        </div>
        """

    _advisor_html(f"""
    <div class='advisor-header-card'>
        <div class='advisor-header-title'>💡 Appliance Advisor — House {selected_house}</div>
        <div class='advisor-header-sub'>Select one appliance and instantly compare behaviour savings, product options, cross-house performance, and recommendation reasoning.</div>
    </div>
    """)

    if apps.empty:
        st.warning("No appliance data available for this house.")
    else:
        apps_for_select = apps.copy().reset_index(drop=True)
        apps_for_select["_display_name"] = [appliance_name(row) for _, row in apps_for_select.iterrows()]

        select_col, note_col = st.columns([0.45, 0.55])
        with select_col:
            selected_appliance_name = st.selectbox(
                "Choose an appliance to analyse",
                apps_for_select["_display_name"].tolist(),
                index=0,
                key="selected_appliance_detail",
            )
        selected_app_row = apps_for_select[apps_for_select["_display_name"] == selected_appliance_name].iloc[0]
        selected_refit_col = selected_app_row.get("refit_column", selected_app_row.get("original_refit_column", None))
        selected_label = selected_app_row.get("appliance_label", selected_appliance_name)

        if not rec_house.empty:
            if selected_refit_col is not None and "refit_column" in rec_house.columns:
                rec_selected = rec_house[rec_house["refit_column"].astype(str) == str(selected_refit_col)].copy()
            elif "appliance_label" in rec_house.columns:
                rec_selected = rec_house[rec_house["appliance_label"].astype(str) == str(selected_label)].copy()
            else:
                rec_selected = pd.DataFrame()
        else:
            rec_selected = pd.DataFrame()

        if not product_house.empty:
            if selected_refit_col is not None and "refit_column" in product_house.columns:
                prod_selected = product_house[product_house["refit_column"].astype(str) == str(selected_refit_col)].copy()
            elif "appliance_label" in product_house.columns:
                prod_selected = product_house[product_house["appliance_label"].astype(str) == str(selected_label)].copy()
            else:
                prod_selected = pd.DataFrame()
        else:
            prod_selected = pd.DataFrame()

        app_kwh_day = snum(selected_app_row.get("avg_kwh_day", selected_app_row.get("total_kwh_window", 0)))
        app_cost_day = snum(selected_app_row.get("cost_day_aud", app_kwh_day * TARIFF_AUD))
        app_cost_month = snum(selected_app_row.get("cost_month_aud", app_cost_day * 30))
        app_cost_year = app_cost_month * 12
        app_events = int(snum(selected_app_row.get("usage_events_est", 0)))
        app_peak = snum(selected_app_row.get("peak_usage_ratio", 0))
        app_offpeak = snum(selected_app_row.get("offpeak_usage_ratio", 0))
        eff_class = selected_app_row.get("intelligent_efficiency_class", "Average")
        benchmark_text = selected_app_row.get("intelligent_recommendation_summary", "Benchmark information will appear after running the intelligent pipeline.")
        reason_text = selected_app_row.get("recommendation_reason_codes", "normal usage pattern")

        behaviour_saving = 0.0
        behaviour_text = "Monitor this appliance and reduce unnecessary usage where possible."
        behaviour_priority = "Normal"
        best_product_save = 0.0
        combined_possible = 0.0
        if not rec_selected.empty:
            behaviour_saving = snum(rec_selected.iloc[0].get("estimated_behaviour_saving_aud_month", 0))
            behaviour_text = rec_selected.iloc[0].get("behaviour_recommendation", behaviour_text)
            behaviour_priority = str(rec_selected.iloc[0].get("behaviour_priority", behaviour_priority)).title()
            best_product_save = snum(rec_selected.iloc[0].get("best_product_saving_aud_month", 0))
            combined_possible = snum(rec_selected.iloc[0].get("combined_behaviour_product_saving_aud_month", behaviour_saving + best_product_save))
        else:
            combined_possible = behaviour_saving + best_product_save

        with note_col:
            _advisor_html(f"""
            <div class='advisor-insight-card' style='padding:0.68rem 0.8rem;'>
                <span class='advisor-role'>Selected appliance</span>
                <div class='advisor-product-name'>{_advisor_safe(selected_appliance_name)}</div>
                <div class='advisor-insight-text'>Efficiency class: <b>{_advisor_safe(eff_class)}</b> · Suggested priority: <b>{_advisor_safe(behaviour_priority)}</b> · Max combined saving: <b>{money(combined_possible)}/mo</b></div>
            </div>
            """)

        _advisor_html(f"""
        <div class='advisor-summary-strip'>
            {_metric_block('Energy / Day', f'{app_kwh_day:.3f} kWh', 'Average daily use')}
            {_metric_block('Cost / Month', money(app_cost_month), 'Current estimate')}
            {_metric_block('Usage Events', f'{app_events}', 'Detected active samples')}
            {_metric_block('Peak Usage', f'{app_peak*100:.0f}%', 'Peak-hour share')}
            {_metric_block('Combined Save', f'{money(combined_possible)}/mo', 'Behaviour + product')}
        </div>
        """)

        explorer_tab, products_tab, compare_tab, explain_tab = st.tabs([
            "💰 Behaviour Summary",
            "🛒 Best Product Options",
            "🏘 Cross-House Insight",
            "🔍 Why this recommendation?",
        ])

        with explorer_tab:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            section("Behaviour Savings Summary", "A quick view of what the selected appliance is doing and what action can reduce cost.")
            adoption = st.slider("Assumed behaviour change followed by user (%)", 0, 100, 100, step=5)
            adjusted_saving = behaviour_saving * (adoption / 100.0)
            _advisor_html(f"""
            <div class='advisor-grid-3'>
                <div class='advisor-explain-card'>
                    <span class='advisor-role'>Action</span>
                    <div class='advisor-product-name'>🧠 {_advisor_safe(selected_appliance_name)}</div>
                    <div class='advisor-explain-text'>{_advisor_snippet(behaviour_text, 26)}</div>
                    <div class='advisor-reason-pills'><span class='advisor-reason-pill'>{_advisor_safe(behaviour_priority)}</span><span class='advisor-reason-pill'>No purchase</span></div>
                </div>
                <div class='advisor-explain-card'>
                    <span class='advisor-role'>Saving estimate</span>
                    <div class='advisor-insight-number'>{money(adjusted_saving)}/mo</div>
                    <div class='advisor-explain-text'>Based on {adoption}% adoption. Full behaviour-only saving is <b>{money(behaviour_saving)}/month</b>, or about <b>{money(behaviour_saving*12)}/year</b>.</div>
                </div>
                <div class='advisor-explain-card'>
                    <span class='advisor-role'>Usage pattern</span>
                    <div class='advisor-insight-number'>{app_events}</div>
                    <div class='advisor-explain-text'>Detected events with <b>{app_peak*100:.0f}%</b> peak-hour activity and <b>{app_offpeak*100:.0f}%</b> off-peak activity. Repeated/peak usage increases priority.</div>
                </div>
            </div>
            """)
            st.markdown("</div>", unsafe_allow_html=True)

        with products_tab:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            section("Best Product Options", "Three simple views: cheapest option, best overall choice, and strongest energy-saving option.")
            if prod_selected.empty:
                st.markdown("<div class='soft-note'>No product options were generated for this appliance. Run the advanced pipeline first.</div>", unsafe_allow_html=True)
            else:
                prod_selected = prod_selected.copy()
                numeric_cols = [
                    "recommended_price_aud", "recommended_annual_kwh", "estimated_monthly_saving_aud",
                    "estimated_annual_saving_aud", "payback_months", "product_match_score",
                    "estimated_energy_saving_kwh_year", "balanced_intelligent_score", "budget_user_score",
                    "eco_user_score", "fast_payback_score"
                ]
                for col in numeric_cols:
                    if col in prod_selected.columns:
                        prod_selected[col] = pd.to_numeric(prod_selected[col], errors="coerce")

                if "recommended_price_aud" in prod_selected.columns:
                    budget_filtered = prod_selected[prod_selected["recommended_price_aud"].fillna(999999) <= budget_limit].copy()
                    if budget_filtered.empty:
                        budget_filtered = prod_selected.copy()
                else:
                    budget_filtered = prod_selected.copy()

                score_col = {
                    "Balanced": "balanced_intelligent_score",
                    "Lowest upfront cost": "budget_user_score",
                    "Energy saving": "eco_user_score",
                    "Fastest payback": "fast_payback_score",
                }.get(user_goal, "balanced_intelligent_score")
                if score_col not in budget_filtered.columns:
                    score_col = "product_match_score" if "product_match_score" in budget_filtered.columns else "estimated_monthly_saving_aud"

                if "recommended_price_aud" in budget_filtered.columns:
                    cheapest = budget_filtered.sort_values("recommended_price_aud", ascending=True).iloc[0]
                else:
                    cheapest = budget_filtered.iloc[0]
                if "estimated_energy_saving_kwh_year" in budget_filtered.columns:
                    energy_best = budget_filtered.sort_values(["estimated_energy_saving_kwh_year", "estimated_monthly_saving_aud"], ascending=[False, False]).iloc[0]
                elif "recommended_annual_kwh" in budget_filtered.columns:
                    energy_best = budget_filtered.sort_values(["recommended_annual_kwh", "recommended_price_aud"], ascending=[True, True]).iloc[0]
                else:
                    energy_best = budget_filtered.sort_values("estimated_monthly_saving_aud", ascending=False).iloc[0]
                if score_col in budget_filtered.columns:
                    overall = budget_filtered.sort_values([score_col, "estimated_monthly_saving_aud"], ascending=[False, False]).iloc[0]
                else:
                    overall = budget_filtered.sort_values("estimated_monthly_saving_aud", ascending=False).iloc[0]

                def _product_card(row, title, icon):
                    store = _advisor_safe(row.get("recommended_store", "Store"), "Store")
                    product = _advisor_safe(row.get("recommended_product", "Recommended product"), "Recommended product")
                    brand = _advisor_safe(row.get("recommended_brand", "Generic"), "Generic")
                    price = money(row.get("recommended_price_aud", np.nan))
                    saving = money(row.get("estimated_monthly_saving_aud", np.nan))
                    annual_save = money(row.get("estimated_annual_saving_aud", np.nan))
                    kwh_save = row.get("estimated_energy_saving_kwh_year", np.nan)
                    if pd.isna(kwh_save):
                        kwh_text = "n/a"
                    else:
                        kwh_text = f"{float(kwh_save):.0f} kWh/yr"
                    payback = row.get("payback_months", np.nan)
                    payback_text = "n/a" if pd.isna(payback) else f"{float(payback):.1f} mo"
                    note = _advisor_snippet(row.get("explainable_product_reason", row.get("suitability_note", row.get("product_recommendation", "Matched to price, saving and payback."))), 16)
                    return f"""
                    <div class='advisor-product-card'>
                        <span class='advisor-role'>{icon} {title}</span>
                        <div class='advisor-product-name'>{product}</div>
                        <div class='advisor-product-store'>🏪 {store} · {brand}</div>
                        <div class='advisor-price-big'>{price}</div>
                        <div class='advisor-stat-row'>
                            <div class='advisor-stat'><div class='advisor-stat-label'>Save / mo</div><div class='advisor-stat-value'>{saving}</div></div>
                            <div class='advisor-stat'><div class='advisor-stat-label'>Energy</div><div class='advisor-stat-value'>{kwh_text}</div></div>
                            <div class='advisor-stat'><div class='advisor-stat-label'>Payback</div><div class='advisor-stat-value'>{payback_text}</div></div>
                        </div>
                        <div class='advisor-short-note'>{note}</div>
                    </div>
                    """

                _advisor_html(f"""
                <div class='advisor-grid-3'>
                    {_product_card(cheapest, 'Cost Option', '💰')}
                    {_product_card(overall, 'Overall Best', '🏆')}
                    {_product_card(energy_best, 'Energy Wise', '🌱')}
                </div>
                """)

                if score_col in budget_filtered.columns:
                    ranked_options = budget_filtered.sort_values([score_col, "estimated_monthly_saving_aud"], ascending=[False, False]).head(6)
                else:
                    ranked_options = budget_filtered.sort_values("estimated_monthly_saving_aud", ascending=False).head(6)
                option_cards = []
                for rank, (_, option_row) in enumerate(ranked_options.iterrows(), start=1):
                    store = _advisor_safe(option_row.get("recommended_store", "Store"), "Store")
                    product = _advisor_safe(option_row.get("recommended_product", "Recommended product"), "Recommended product")
                    brand = _advisor_safe(option_row.get("recommended_brand", "Generic"), "Generic")
                    price = money(option_row.get("recommended_price_aud", np.nan))
                    saving = money(option_row.get("estimated_monthly_saving_aud", np.nan))
                    payback = option_row.get("payback_months", np.nan)
                    payback_text = "n/a" if pd.isna(payback) else f"{float(payback):.1f} mo"
                    option_cards.append(f"""
                    <div class='advisor-option-card'>
                        <div class='advisor-option-top'>
                            <div class='advisor-option-name'>{rank}. {product}</div>
                            <div class='advisor-option-price'>{price}</div>
                        </div>
                        <div class='advisor-option-meta'>{store} · {brand}<br><b>Saving:</b> {saving}/mo · <b>Payback:</b> {payback_text}</div>
                    </div>
                    """)
                _advisor_html(f"""
                <div class='advisor-list-title'>Other strong options</div>
                <div class='advisor-grid-3'>{''.join(option_cards)}</div>
                """)
            st.markdown("</div>", unsafe_allow_html=True)

        with compare_tab:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            section("Cross-House Insight", "A summary comparison against similar appliances across the REFIT houses loaded in the app.")
            if "appliance_label" in appliance_df.columns:
                selected_category = str(selected_appliance_name).lower().split("(")[0].strip()
                key_word = selected_category.split()[0] if selected_category.split() else selected_category
                comparison = appliance_df[appliance_df["appliance_label"].astype(str).str.lower().str.contains(key_word, na=False)].copy()
                if comparison.empty and selected_refit_col is not None and "refit_column" in appliance_df.columns:
                    comparison = appliance_df[appliance_df["refit_column"].astype(str) == str(selected_refit_col)].copy()
                if not comparison.empty:
                    if "avg_kwh_day" in comparison.columns:
                        comparison["avg_kwh_day"] = pd.to_numeric(comparison["avg_kwh_day"], errors="coerce")
                    avg_other = pd.to_numeric(comparison.get("avg_kwh_day", pd.Series(dtype=float)), errors="coerce").mean() if "avg_kwh_day" in comparison.columns else 0
                    diff_pct = ((app_kwh_day - avg_other) / avg_other * 100) if avg_other else 0
                    msg = "above" if diff_pct >= 0 else "below"
                    percentile = snum(selected_app_row.get("usage_percentile_vs_similar_houses", 0))
                    _advisor_html(f"""
                    <div class='advisor-grid-3'>
                        <div class='advisor-insight-card'><span class='advisor-role'>Your use</span><div class='advisor-insight-number'>{app_kwh_day:.3f}</div><div class='advisor-insight-text'>kWh/day for {_advisor_safe(selected_appliance_name)}.</div></div>
                        <div class='advisor-insight-card'><span class='advisor-role'>REFIT average</span><div class='advisor-insight-number'>{avg_other:.3f}</div><div class='advisor-insight-text'>kWh/day across similar loaded appliances.</div></div>
                        <div class='advisor-insight-card'><span class='advisor-role'>Position</span><div class='advisor-insight-number'>{abs(diff_pct):.1f}%</div><div class='advisor-insight-text'>Your appliance is <b>{msg}</b> the similar-appliance average. Percentile: <b>{percentile:.1f}%</b>.</div></div>
                    </div>
                    """)
                    ranked = comparison.copy()
                    if "avg_kwh_day" in ranked.columns:
                        ranked = ranked.sort_values("avg_kwh_day", ascending=False)
                    compact_cards = []
                    for _, comp_row in ranked.head(6).iterrows():
                        comp_house = int(snum(comp_row.get("house", 0)))
                        comp_name = _advisor_safe(appliance_name(comp_row), "Appliance")
                        comp_kwh = snum(comp_row.get("avg_kwh_day", 0))
                        comp_cost = snum(comp_row.get("cost_month_aud", comp_kwh * TARIFF_AUD * 30))
                        comp_events = int(snum(comp_row.get("usage_events_est", 0)))
                        comp_peak = snum(comp_row.get("peak_usage_ratio", 0))
                        compact_cards.append(f"""
                        <div class='advisor-option-card'>
                            <div class='advisor-option-top'><div class='advisor-option-name'>House {comp_house}: {comp_name}</div><div class='advisor-option-price'>{comp_kwh:.3f} kWh</div></div>
                            <div class='advisor-option-meta'><b>{money(comp_cost)}/mo</b> · {comp_events} events · Peak usage {comp_peak*100:.0f}%</div>
                        </div>
                        """)
                    _advisor_html(f"""
                    <div class='advisor-list-title'>Comparable REFIT examples</div>
                    <div class='advisor-grid-3'>{''.join(compact_cards)}</div>
                    """)
                else:
                    st.markdown("<div class='soft-note'>No similar appliance was found across other houses in this dataset.</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='soft-note'>Cross-house comparison requires appliance labels in the appliance breakdown file.</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with explain_tab:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            section("Why This Recommendation?", "Plain-language reasoning behind the appliance flag and the suggested saving pathway.")
            benchmark_avg = snum(selected_app_row.get("benchmark_avg_kwh_day", 0))
            percentile = snum(selected_app_row.get("usage_percentile_vs_similar_houses", 0))
            diff_pct = snum(selected_app_row.get("above_similar_house_avg_pct", 0))
            reason_parts = []
            for part in str(reason_text).replace(";", ",").replace("|", ",").split(","):
                part = part.strip().replace("_", " ").title()
                if part:
                    reason_parts.append(part)
            if not reason_parts:
                reason_parts = ["Normal Usage Pattern"]
            reason_pills = "".join(f"<span class='advisor-reason-pill'>{_advisor_safe(x)}</span>" for x in reason_parts[:6])
            _advisor_html(f"""
            <div class='advisor-grid-3'>
                <div class='advisor-explain-card'>
                    <span class='advisor-role'>Data trigger</span>
                    <div class='advisor-product-name'>Cross-house benchmark</div>
                    <div class='advisor-explain-text'>Similar-house benchmark is <b>{benchmark_avg:.4f} kWh/day</b>. This appliance is at <b>{percentile:.1f}%</b> percentile and <b>{diff_pct:.1f}%</b> from the similar-house average.</div>
                </div>
                <div class='advisor-explain-card'>
                    <span class='advisor-role'>Saving pathway</span>
                    <div class='advisor-product-name'>Best route to reduce cost</div>
                    <div class='advisor-explain-text'>Behaviour-only: <b>{money(behaviour_saving)}/mo</b><br>Product-only: <b>{money(best_product_save)}/mo</b><br>Combined: <b>{money(combined_possible)}/mo</b></div>
                </div>
                <div class='advisor-explain-card'>
                    <span class='advisor-role'>Decision logic</span>
                    <div class='advisor-product-name'>What the system checks</div>
                    <div class='advisor-explain-text'>Energy use, monthly cost, repeated events, peak-hour activity, product price, payback, and your selected goal: <b>{_advisor_safe(user_goal)}</b>.</div>
                </div>
            </div>
            <div class='advisor-list-title'>Reason codes</div>
            <div class='advisor-reason-pills'>{reason_pills}<span class='advisor-reason-pill'>Goal: {_advisor_safe(user_goal)}</span><span class='advisor-reason-pill'>Budget: {money(budget_limit)}</span></div>
            <div class='soft-note' style='margin-top:0.65rem;'>Summary: {_advisor_snippet(benchmark_text, 28)}</div>
            """)
            st.markdown("</div>", unsafe_allow_html=True)



st.caption("🌿 REFIT House Owner Energy Advisor · 365-day intelligent recommendation system · behaviour + product ranking + cross-house insight")
