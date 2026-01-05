import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- ตั้งค่า Email (แก้ไขตรงนี้) ---
SENDER_EMAIL = "sd9268102@gmail.com"
APP_PASSWORD = "pczdwxidblvxitnq"    # รหัส 16 หลักจาก Google
RECEIVER_EMAIL = "px30253@gmail.com" 

# 1. ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DELIVERY ALERT SYSTEM", layout="wide")

st.title("📱 ระบบกรองข้อมูลและแจ้งเตือน")
st.write("ฟิลเตอร์รายการ DELIVERY_FAILED และส่งรายงานเข้า Email")

# 2. ส่วนอัปโหลดไฟล์
uploaded_file = st.file_uploader("อัปโหลดไฟล์ Inventory Report", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)

        # 3. เตรียมตัวแปรวันที่
        tomorrow = datetime.now() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%d-%b-%Y') 

        # 4. การกรองข้อมูล
        col_status = df.columns[3]
        col_date = df.columns[5]
        mask = (df[col_status] == 'DELIVERY_FAILED') & (df[col_date].astype(str).str.strip() == tomorrow_str)
        filtered_df = df[mask].copy()

        # 5. แสดงผล
        if not filtered_df.empty:
            st.success(f"✅ พบข้อมูลสำหรับวันพรุ่งนี้ ({tomorrow_str}) ทั้งหมด {len(filtered_df)} รายการ")
            
            display_cols = [1, 4, 5, 15]
            final_df = filtered_df.iloc[:, display_cols]
            final_df.columns = ['Parcel ID', 'Failure Reason', 'Next Delivery Date', 'TourID']
            st.dataframe(final_df, use_container_width=True)

            # --- ส่วนการส่ง Email ---
            st.divider()
            st.subheader("✉️ ส่งรายงานเข้า Email")
            
            # เตรียมข้อความที่จะส่งในเมล
            email_content = f"รายการพัสดุเสียที่ต้องจัดส่งใหม่วันที่ {tomorrow_str}:\n\n"
            for _, row in final_df.iterrows():
                email_content += f"- พัสดุ: {row['Parcel ID']} | สาเหตุ: {row['Failure Reason']} | สายส่ง: {row['TourID']}\n"

            if st.button("📧 กดเพื่อส่งรายงานเข้า Email พนักงาน"):
                try:
                    msg = MIMEMultipart()
                    msg['From'] = SENDER_EMAIL
                    msg['To'] = RECEIVER_EMAIL
                    msg['Subject'] = f"แจ้งเตือนพัสดุ DELIVERY_FAILED ({tomorrow_str})"
                    msg.attach(MIMEText(email_content, 'plain'))

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server.login(SENDER_EMAIL, APP_PASSWORD)
                    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
                    server.quit()
                    
                    st.success(f"ส่งอีเมลไปที่ {RECEIVER_EMAIL} เรียบร้อยแล้ว!")
                except Exception as e:
                    st.error(f"ส่งเมลไม่สำเร็จ: {e}")

        else:
            st.warning(f"❌ ไม่พบข้อมูลสำหรับวันที่ {tomorrow_str}")

    except Exception as e:
        st.error(f"เกิดข้อผิดพลาด: {e}")
else:
    st.info("💡 กรุณาอัปโหลดไฟล์เพื่อเริ่มทำงาน")
