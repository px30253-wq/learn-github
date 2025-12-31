import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL Unified Filter", layout="wide")

st.title("📦 DHL Multi-Function Filter Portal")

# 2. ส่วนเลือกโหมดการทำงานด้านข้าง
st.sidebar.header("เมนูการใช้งาน")
mode = st.sidebar.radio(
    "เลือกโหมดการกรองข้อมูล:",
    ["โหมด 1: ค้นหา THPKD1 (AU -> AE)", 
     "โหมด 2: Ageing 5 + O Shopping (B)"]
)

# 3. ส่วนอัปโหลดไฟล์
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Inventory Report (CSV)", type=["csv"])

if uploaded_file:
    try:
        # อ่านไฟล์ CSV รองรับภาษาไทย
        df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        
        if mode == "โหมด 1: ค้นหา THPKD1 (AU -> AE)":
            st.subheader("🔍 โหมด 1: ค้นหา THPKD1 ในคอลัมน์ AU")
            # ตรวจสอบจำนวนคอลัมน์ (AU อยู่ลำดับที่ 47 หรือ Index 46)
            if len(df.columns) >= 47:
                col_ae_idx = 30  # คอลัมน์ AE
                col_au_idx = 46  # คอลัมน์ AU
                
                # กรองข้อมูล
                mask = df.iloc[:, col_au_idx].astype(str).str.strip() == "THPKD1"
                filtered_df = df[mask].copy()
                
                if not filtered_df.empty:
                    # ย้าย AE มาหน้าสุด
                    cols = filtered_df.columns.tolist()
                    ae_col = cols.pop(col_ae_idx)
                    filtered_df = filtered_df[[ae_col] + cols]
                    
                    st.success(f"✅ พบข้อมูล {len(filtered_df)} รายการ")
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("ไม่พบคำว่า 'THPKD1' ในคอลัมน์ AU")
            else:
                st.error(f"ไฟล์มีคอลัมน์ไม่ถึง AU (มีแค่ {len(df.columns)} คอลัมน์)")

        else:  # โหมด 2
            st.subheader("🔍 โหมด 2: Ageing 5 + O Shopping")
            # คอลัมน์ B=1, M=12, N=13
            if len(df.columns) >= 14:
                col_b_idx = 1
                col_m_idx = 12
                col_n_idx = 13
                
                # กรองข้อมูล (Ageing == 5 และ Customer == O Shopping)
                mask = (df.iloc[:, col_m_idx] == 5) & \
                       (df.iloc[:, col_n_idx].astype(str).str.strip() == "O Shopping Co.,Ltd.")
                
                filtered_df = df[mask].copy()
                
                if not filtered_df.empty:
                    # ย้าย B มาหน้าสุด
                    cols = filtered_df.columns.tolist()
                    b_col = cols.pop(col_b_idx)
                    filtered_df = filtered_df[[b_col] + cols]
                    
                    st.success(f"✅ พบข้อมูล {len(filtered_df)} รายการ")
                    st.dataframe(filtered_df, use_container_width=True)
                else:
                    st.warning("ไม่พบรายการที่ตรงตามเงื่อนไข (Ageing 5 และ O Shopping)")
            else:
                st.error("ไฟล์มีคอลัมน์ไม่ถึงคอลัมน์ N")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการอ่านไฟล์: {e}")
