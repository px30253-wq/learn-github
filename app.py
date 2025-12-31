import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL Advanced Search", layout="wide")

st.title("📦 DHL Inventory Filter System")

# ส่วนเมนูเลือกโหมด
mode = st.sidebar.selectbox(
    "เลือกรูปแบบการกรองข้อมูล:",
    ["ค้นหา THPKD1 (AU -> AE)", "ค้นหา Ageing 5 + O Shopping (B)"]
)

uploaded_file = st.file_uploader("อัปโหลดไฟล์ CSV", type=["csv"])

if uploaded_file:
    try:
        # อ่านไฟล์ CSV
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        
        # --- โหมดที่ 1: ค้นหา THPKD1 ---
        if mode == "ค้นหา THPKD1 (AU -> AE)":
            if len(df.columns) >= 47:
                # กรอง AU (Index 46) และย้าย AE (Index 30)
                mask = df.iloc[:, 46].astype(str).str.strip() == "THPKD1"
                res = df[mask].copy()
                if not res.empty:
                    cols = res.columns.tolist()
                    ae_col = cols.pop(30)
                    res = res[[ae_col] + cols]
                    st.success(f"✅ พบข้อมูล {len(res)} รายการ")
                    st.dataframe(res)
                else:
                    st.warning("ไม่พบข้อมูล THPKD1 ในคอลัมน์ AU")
            else:
                st.error("ไฟล์มีจำนวนคอลัมน์ไม่ถึง 47 คอลัมน์ (AU)")

        # --- โหมดที่ 2: Ageing 5 + O Shopping ---
        else:
            if len(df.columns) >= 14:
                # กรอง M (Index 12) เป็น 5 และ N (Index 13) เป็น O Shopping
                # ย้าย B (Index 1) มาหน้าสุด
                mask = (df.iloc[:, 12] == 5) & (df.iloc[:, 13].astype(str).str.strip() == "O Shopping Co.,Ltd.")
                res = df[mask].copy()
                if not res.empty:
                    cols = res.columns.tolist()
                    b_col = cols.pop(1)
                    res = res[[b_col] + cols]
                    st.success(f"✅ พบข้อมูล {len(res)} รายการ")
                    st.dataframe(res)
                else:
                    st.warning("ไม่พบรายการที่ตรงเงื่อนไข (Ageing 5 และ O Shopping)")
            else:
                st.error("ไฟล์มีจำนวนคอลัมน์ไม่ถึง 14 คอลัมน์ (N)")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
