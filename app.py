import streamlit as st
import pandas as pd

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL Combined Tool", layout="wide")
st.title("📦 DHL Inventory Combined Filter")
st.markdown("ระบบจะกรองข้อมูลทั้ง 2 เงื่อนไขให้ทันทีหลังอัปโหลดไฟล์")

# ส่วนอัปโหลดไฟล์ (รองรับทั้ง CSV และ Excel)
uploaded_file = st.file_uploader("อัปโหลดไฟล์ (CSV, XLSX, XLS)", type=["csv", "xlsx", "xls"])

if uploaded_file:
    try:
        # 1. อ่านไฟล์
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)

        # --- ส่วนที่ 1: กรองแบบ Return Part 1 (AU -> AE) ---
        st.divider() # เส้นคั่น
        st.subheader("🔍 ผลลัพธ์: Return (TH_RD_Ageing)")
        
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
                st.warning("ไม่พบข้อมูล THPKD1 ในคอลัมน์ AU")
        else:
            st.error("ไม่พบข้อมูล")

        # --- ส่วนที่ 2: กรองแบบ Return Part 2 (Ageing 5 + O Shopping) ---
        st.divider() # เส้นคั่น
        st.subheader("🔍 ผลลัพธ์: Return Part 2 (inventory_report)")
        
        if len(df.columns) >= 14:
            # กรอง M=12 เป็น 5 และ N=13 เป็น O Shopping
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
                st.warning("ไม่พบรายการที่ตรงเงื่อนไข")
        else:
            st.error("ไม่พบรายการที่ตรงเงื่อนไข")

    except Exception as e:
        st.error(f"❌ เกิดข้อผิดพลาด: {e}")
else:
    st.info("💡 กรุณาอัปโหลดไฟล์เพื่อดูผลลัพธ์")
