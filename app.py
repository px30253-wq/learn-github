import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL Multi-File Processing", layout="wide")

st.title("📦 DHL Inventory Filter (Multiple Files)")
st.write("อัปโหลดหลายไฟล์พร้อมกัน ระบบจะแสดงผลลัพธ์ทั้งหมดเรียงต่อกันลงมา")

# 2. ช่องอัปโหลดไฟล์ (รับได้หลายไฟล์พร้อมกัน)
uploaded_files = st.file_uploader(
    "เลือกไฟล์ Inventory Report (CSV, XLSX, XLS)", 
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # แสดงหัวข้อชื่อไฟล์ให้ชัดเจน
        st.markdown(f"## 📄 ไฟล์: {uploaded_file.name}")
        
        try:
            # อ่านไฟล์
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
            else:
                df = pd.read_excel(uploaded_file)

            # --- ส่วนที่ 1: Return Part 1 ---
            st.subheader("🔍 1. Return Part 1 (THPKD1)")
            if len(df.columns) >= 47:
                mask1 = df.iloc[:, 46].astype(str).str.strip() == "THPKD1"
                res1 = df[mask1].copy()
                if not res1.empty:
                    cols1 = res1.columns.tolist()
                    ae_col = cols1.pop(30)
                    res1 = res1[[ae_col] + cols1]
                    st.success(f"ไฟล์ {uploaded_file.name} : พบ Part 1 จำนวน {len(res1)} รายการ")
                    st.dataframe(res1, use_container_width=True)
                else:
                    st.warning(f"ไฟล์ {uploaded_file.name} : ไม่พบข้อมูล THPKD1")
            else:
                st.error(f"ไฟล์ {uploaded_file.name} : คอลัมน์ไม่ถึง AU (47)")

            # --- ส่วนที่ 2: Return Part 2 ---
            st.subheader("🔍 2. Return Part 2 (Ageing 5 & O Shopping)")
            if len(df.columns) >= 14:
                mask2 = (df.iloc[:, 12].astype(str).str.contains('5')) & \
                        (df.iloc[:, 13].astype(str).str.strip() == "O Shopping Co.,Ltd.")
                res2 = df[mask2].copy()
                if not res2.empty:
                    cols2 = res2.columns.tolist()
                    b_col = cols2.pop(1)
                    res2 = res2[[b_col] + cols2]
                    st.success(f"ไฟล์ {uploaded_file.name} : พบ Part 2 จำนวน {len(res2)} รายการ")
                    st.dataframe(res2, use_container_width=True)
                else:
                    st.warning(f"ไฟล์ {uploaded_file.name} : ไม่พบรายการ Ageing 5 & O Shopping")
            else:
                st.error(f"ไฟล์ {uploaded_file.name} : คอลัมน์ไม่ถึง N (14)")
            
            # ขีดเส้นคั่นหนาๆ ระหว่างไฟล์
            st.markdown("---")
            st.markdown("---")

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในไฟล์ {uploaded_file.name}: {e}")
else:
    st.info("💡 กรุณาอัปโหลดไฟล์ (คุณสามารถลากลงมาวางพร้อมกันหลายไฟล์ได้)")
