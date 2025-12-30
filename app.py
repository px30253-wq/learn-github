import streamlit as st
import pandas as pd

st.set_page_config(page_title="DHL Filter", layout="wide")
st.title("📦 DHL AU-to-AE Filter")

file = st.file_uploader("Upload CSV", type=["csv"])

if file:
    df = pd.read_csv(file, encoding='utf-8-sig')
    if len(df.columns) >= 47:
        # กรอง AU (Index 46) หา THPKD1
        mask = df.iloc[:, 46].astype(str).str.strip() == "THPKD1"
        res = df[mask].copy()
        
        if not res.empty:
            # ย้าย AE (Index 30) มาหน้าสุด
            cols = res.columns.tolist()
            ae = cols.pop(30)
            res = res[[ae] + cols]
            st.success(f"พบ {len(res)} รายการ")
            st.dataframe(res, use_container_width=True)
        else:
            st.warning("ไม่พบข้อมูล THPKD1 ในคอลัมน์ AU")
