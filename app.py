import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL Multi-File Tool", layout="wide")

st.title("📦 DHL Inventory Filter (Multiple Files)")
st.write("คุณสามารถอัปโหลดไฟล์หลายไฟล์พร้อมกันได้ ระบบจะแยกผลลัพธ์ให้ทีละไฟล์")

# ปรับปรุงช่องอัปโหลดให้รับได้หลายไฟล์ (accept_multiple_files=True)
uploaded_files = st.file_uploader(
    "เลือกไฟล์ Inventory Report (อัปโหลดได้หลายไฟล์พร้อมกัน)", 
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        # แสดงชื่อไฟล์ที่กำลังประมวลผล
        st.markdown(f"### 📄 กำลังประมวลผลไฟล์: `{uploaded_file.name}`")
        
        try:
            # 1. อ่านไฟล์
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
            else:
                df = pd.read_excel(uploaded_file)

            # สร้าง Tab เพื่อประหยัดเนื้อที่หน้าจอ
            tab1, tab2 = st.tabs(["🔍 Return Part 1 (THPKD1)", "🔍 Return Part 2 (Ageing 5 & O Shopping)"])

            # --- ส่วนที่ 1: Return Part 1 ---
            with tab1:
                if len(df.columns) >= 47:
                    mask1 = df.iloc[:, 46].astype(str).str.strip() == "THPKD1"
                    res1 = df[mask1].copy()
                    if not res1.empty:
                        cols1 = res1.columns.tolist()
                        ae_col = cols1.pop(30)
                        res1 = res1[[ae_col] + cols1]
                        st.success(f"พบข้อมูล Part 1 ทั้งหมด {len(res1)} รายการ")
                        st.dataframe(res1, use_container_width=True)
                    else:
                        st.warning("ไม่พบคำว่า 'THPKD1' ในคอลัมน์ AU")
                else:
                    st.error("ไฟล์นี้มีจำนวนคอลัมน์ไม่ถึง 47 (AU)")

            # --- ส่วนที่ 2: Return Part 2 ---
            with tab2:
                if len(df.columns) >= 14:
                    mask2 = (df.iloc[:, 12].astype(str).str.contains('5')) & \
                            (df.iloc[:, 13].astype(str).str.strip() == "O Shopping Co.,Ltd.")
                    res2 = df[mask2].copy()
                    if not res2.empty:
                        cols2 = res2.columns.tolist()
                        b_col = cols2.pop(1)
                        res2 = res2[[b_col] + cols2]
                        st.success(f"พบข้อมูล Part 2 ทั้งหมด {len(res2)} รายการ")
                        st.dataframe(res2, use_container_width=True)
                    else:
                        st.warning("ไม่พบรายการที่ตรงเงื่อนไข (Ageing 5 & O Shopping)")
                else:
                    st.error("ไฟล์นี้มีจำนวนคอลัมน์ไม่ถึง 14 (N)")
            
            st.markdown("---") # เส้นคั่นระหว่างแต่ละไฟล์

        except Exception as e:
            st.error(f"❌ เกิดข้อผิดพลาดในไฟล์ {uploaded_file.name}: {e}")
else:
    st.info("💡 กรุณาอัปโหลดไฟล์ (สามารถเลือกหลายไฟล์พร้อมกันได้)")
