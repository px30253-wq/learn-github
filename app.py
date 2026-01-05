import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="SMS DELIVERY ALERT", layout="wide")

st.title("📱 ระบบกรองข้อมูลแจ้งเตือน SMS")
st.write("ฟิลเตอร์เฉพาะรายการ DELIVERY_FAILED ของวันพรุ่งนี้")

# 2. ส่วนอัปโหลดไฟล์
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Inventory Report", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        # อ่านไฟล์
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)

        # 3. เตรียมตัวแปรวันที่ (วันพรุ่งนี้)
        # ตัวอย่าง: ถ้าวันนี้วันที่ 5 โค้ดจะหา 06-Jan-2026
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%d-%b-%Y') 

        # 4. การกรองข้อมูล (Filtering)
        # คอลัมน์ D (index 3) = Parcel Status
        # คอลัมน์ F (index 5) = Next Delivery Date
        
        # ตรวจสอบชื่อคอลัมน์จริงเพื่อป้องกัน Error จากการสะกดผิดในไฟล์
        col_status = df.columns[3]
        col_date = df.columns[5]

        mask = (df[col_status] == 'DELIVERY_FAILED') & (df[col_date].astype(str).str.strip() == tomorrow_str)
        filtered_df = df[mask].copy()

        # 5. แสดงผล
        if not filtered_df.empty:
            st.success(f"✅ พบข้อมูลสำหรับวันพรุ่งนี้ ({tomorrow_str}) ทั้งหมด {len(filtered_df)} รายการ")
            
            # เลือกเฉพาะคอลัมน์ B, E, F, P (Index 1, 4, 5, 15)
            display_cols = [1, 4, 5, 15]
            final_df = filtered_df.iloc[:, display_cols]
            
            # ตั้งชื่อคอลัมน์ใหม่ให้อ่านง่าย
            final_df.columns = ['Parcel ID', 'Failure Reason', 'Next Delivery Date', 'TourID']
            
            # แสดงตารางข้อมูล
            st.dataframe(final_df, use_container_width=True)

            # 6. สร้างข้อความสำหรับ Copy ไปส่ง SMS
            st.subheader("💬 ข้อความสำหรับส่ง SMS")
            for _, row in final_df.iterrows():
                # คุณสามารถปรับแก้ข้อความใน f-string นี้ได้ตามต้องการ
                sms_text = f"พัสดุ {row['Parcel ID']} จัดส่งไม่สำเร็จเนื่องจาก {row['Failure Reason']} จะจัดส่งใหม่วันที่ {row['Next Delivery Date']} (สายส่ง: {row['TourID']})"
                st.code(sms_text) # ใช้ st.code เพื่อให้กดคลิก copy ได้ง่าย
                
        else:
            st.warning(f"❌ ไม่พบข้อมูล DELIVERY_FAILED ที่ระบุวันส่งใหม่เป็นวันที่ {tomorrow_str}")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("💡 กรุณาอัปโหลดไฟล์ Excel หรือ CSV เพื่อเริ่มการกรองข้อมูล")
