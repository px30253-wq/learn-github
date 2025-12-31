import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL Multi-Format Tool", layout="wide")
st.title("📦 DHL Filter (CSV & Excel Support)")

# เมนูเลือกโหมด
mode = st.sidebar.selectbox(
    "เลือกรูปแบบการกรองข้อมูล:",
    ["ค้นหา THPKD1 (AU -> AE)", "ค้นหา Ageing 5 + O Shopping (B)"]
)

# เพิ่มนามสกุลไฟล์ให้รองรับทั้ง csv, xlsx, xls
uploaded_file = st.file_uploader("อัปโหลดไฟล์ (CSV, XLSX, XLS)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        # ตรวจสอบนามสกุลไฟล์เพื่อเลือกวิธีอ่าน
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            # สำหรับ Excel (.xlsx, .xls)
            df = pd.read_excel(uploaded_file)
        
        # --- โหมดที่ 1 ---
        if mode == "ค้นหา THPKD1 (AU -> AE)":
            if len(df.columns) >= 47:
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
                st.error("ไฟล์นี้มีจำนวนคอลัมน์ไม่ถึง AU (47)")

        # --- โหมดที่ 2 ---
        else:
            if len(df.columns) >= 14:
                # กรอง M (Index 12) และ N (Index 13)
                mask = (df.iloc[:, 12].astype(str).str.contains('5')) & \
                       (df.iloc[:, 13].astype(str).str.strip() == "O Shopping Co.,Ltd.")
                res = df[mask].copy()
                if not res.empty:
                    cols = res.columns.tolist()
                    b_col = cols.pop(1) # คอลัมน์ B
                    res = res[[b_col] + cols]
                    st.success(f"✅ พบข้อมูล {len(res)} รายการ")
                    st.dataframe(res)
                else:
                    st.warning("ไม่พบรายการที่ตรงเงื่อนไข")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
