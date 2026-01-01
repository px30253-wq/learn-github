import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL All-in-One Filter", layout="wide")

st.title("📦 DHL Inventory Filter (Single Upload)")
st.write("อัปโหลดไฟล์เดียว เพื่อดูผลลัพธ์ทั้ง Part 1 และ Part 2 พร้อมกัน")

# 2. ช่องอัปโหลดไฟล์เดียว (รองรับ CSV และ Excel)
uploaded_file = st.file_uploader("เลือกไฟล์ Inventory Report (CSV, XLSX, XLS)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        # ตรวจสอบนามสกุลไฟล์เพื่ออ่านข้อมูล
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)

        # --- ส่วนที่ 1: การประมวลผล Return Part 1 (AU -> AE) ---
        st.markdown("---")
        st.header("🔍 1. Return Part 1 (THPKD1)")
        
        if len(df.columns) >= 47:
            # คอลัมน์ AU คือ Index 46
            mask1 = df.iloc[:, 46].astype(str).str.strip() == "THPKD1"
            res1 = df[mask1].copy()
            
            if not res1.empty:
                # ย้ายคอลัมน์ AE (Index 30) มาหน้าสุด
                cols1 = res1.columns.tolist()
                ae_col = cols1.pop(30)
                res1 = res1[[ae_col] + cols1]
                st.success(f"พบข้อมูล Part 1 ทั้งหมด {len(res1)} รายการ")
                st.dataframe(res1, use_container_width=True)
            else:
                st.warning("ไม่พบรายการที่ตรงเงื่อนไข")
        else:
            st.error("ไม่พบรายการที่ตรงเงื่อนไข")

        # --- ส่วนที่ 2: การประมวลผล Return Part 2 (Ageing 5 & O Shopping) ---
        st.markdown("---")
        st.header("🔍 2. Return Part 2 (Ageing 5 & O Shopping)")
        
        if len(df.columns) >= 14:
            # คอลัมน์ M=12 (Ageing), N=13 (Customer Name)
            # ใช้ .astype(str).str.contains('5') เพื่อความยืดหยุ่นในไฟล์ Excel
            mask2 = (df.iloc[:, 12].astype(str).str.contains('5')) & \
                    (df.iloc[:, 13].astype(str).str.strip() == "O Shopping Co.,Ltd.")
            res2 = df[mask2].copy()
            
            if not res2.empty:
                # ย้ายคอลัมน์ B (Index 1) มาหน้าสุด
                cols2 = res2.columns.tolist()
                b_col = cols2.pop(1)
                res2 = res2[[b_col] + cols2]
                st.success(f"พบข้อมูล Part 2 ทั้งหมด {len(res2)} รายการ")
                st.dataframe(res2, use_container_width=True)
            else:
                st.warning("ไม่พบรายการที่ตรงเงื่อนไข")
        else:
            st.error("ไฟล์มีจำนวนคอลัมน์ไม่ถึง 14 (N)")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาดในการประมวลผล: {e}")
else:
    st.info("💡 กรุณาอัปโหลดไฟล์ Inventory Report เพื่อเริ่มการกรองข้อมูล")
