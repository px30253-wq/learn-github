import streamlit as st
import pandas as pd

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL RETURN FILTER", layout="wide")

st.title("📦 DHL RETURN FILTER")


# 2. ช่องอัปโหลดไฟล์ (รับได้หลายไฟล์พร้อมกัน)
uploaded_files = st.file_uploader(
    "เลือกไฟล์", 
    type=["csv", "xlsx", "xls"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        try:
            # อ่านไฟล์
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
            else:
                df = pd.read_excel(uploaded_file)

            # ตรวจสอบว่าไฟล์มีข้อมูลหรือไม่ก่อนแสดงหัวข้อไฟล์
            has_part1 = len(df.columns) >= 47 and not df[df.iloc[:, 46].astype(str).str.strip() == "THPKD1"].empty
            
            mask_p2 = (df.iloc[:, 12].astype(str).str.contains('5')) & \
                      (df.iloc[:, 13].astype(str).str.strip() == "O Shopping Co.,Ltd.") if len(df.columns) >= 14 else pd.Series([False]*len(df))
            has_part2 = not df[mask_p2].empty if len(df.columns) >= 14 else False

            # ถ้าไฟล์นี้มีข้อมูลอย่างใดอย่างหนึ่ง ถึงจะแสดงชื่อไฟล์และตาราง
            if has_part1 or has_part2:
                st.markdown(f"## 📄 ไฟล์: {uploaded_file.name}")

                # --- ส่วนที่ 1: Return Part 1 ---
                if has_part1:
                    st.subheader("🔍 1. Return (TH_RD_Ageing)")
                    mask1 = df.iloc[:, 46].astype(str).str.strip() == "THPKD1"
                    res1 = df[mask1].copy()
                    
                    # จัดการย้ายคอลัมน์
                    cols1 = res1.columns.tolist()
                    ae_col = cols1.pop(30)
                    res1 = res1[[ae_col] + cols1]
                    
                    st.success(f"พบข้อมูล Part 1 จำนวน {len(res1)} รายการ")
                    st.dataframe(res1, use_container_width=True)

                # --- ส่วนที่ 2: Return Part 2 ---
                if has_part2:
                    st.subheader("🔍 2. Return (inventory_report)")
                    res2 = df[mask_p2].copy()
                    
                    # จัดการย้ายคอลัมน์
                    cols2 = res2.columns.tolist()
                    b_col = cols2.pop(1)
                    res2 = res2[[b_col] + cols2]
                    
                    st.success(f"พบข้อมูล Part 2 จำนวน {len(res2)} รายการ")
                    st.dataframe(res2, use_container_width=True)
                
                st.markdown("---")

        except Exception:
            # หากไฟล์มีปัญหาเรื่อง Format หรืออ่านไม่ได้ จะข้ามไปเงียบๆ ไม่โชว์ Error สีแดง
            pass
else:
    st.info("💡 กรุณาอัปโหลดไฟล์เพื่อเริ่มการทำงาน")
