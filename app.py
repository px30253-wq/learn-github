import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DHL Unified Filter", layout="wide")

st.title("📦 DHL Multi-Function Filter Portal")

# สร้างส่วนเลือกโหมดการทำงานที่แถบด้านข้าง (Sidebar)
mode = st.sidebar.radio(
    "เลือกโหมดการกรองข้อมูล:",
    ("โหมด 1: ค้นหา THPKD1 (AU -> AE)", 
     "โหมด 2: Ageing 5 + O Shopping (Parcel ID)")
)

uploaded_file = st.file_uploader("อัปโหลดไฟล์ Inventory Report (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
    
    # --- โหมดที่ 1: ค้นหา THPKD1 ที่คอลัมน์ AU ---
    if mode == "โหมด 1: ค้นหา THPKD1 (AU -> AE)":
        st.subheader("🔍 กำลังทำงานในโหมด: ค้นหา THPKD1 ในคอลัมน์ AU")
        if len(df.columns) >= 47:
            # AU = Index 46, AE = Index 30
            mask = df.iloc[:, 46].astype(str).str.strip() == "THPKD1"
            res = df[mask].copy()
            if not res.empty:
                # ย้าย AE มาหน้าสุด
                cols = res.columns.tolist()
                ae = cols.pop(30)
                res = res[[ae] + cols]
                st.success(f"✅ พบข้อมูล {len(res)} รายการ")
                st.dataframe(res, use_container_width=True)
            else:
                st.warning("ไม่พบข้อมูล THPKD1 ในคอลัมน์ AU")
        else:
            st.error("ไฟล์มีคอลัมน์ไม่ถึง AU (47 คอลัมน์)")

    # --- โหมดที่ 2: Ageing 5 + O Shopping ---
    else:
        st.subheader("🔍 กำลังทำงานในโหมด: Ageing 5 + O Shopping")
        if len(df.columns) >= 14:
            # B = 1, M = 12, N = 13
            col_m = df.columns[12]
            col_n = df.columns[13]
            
            mask = (df[col_m] == 5) & (df[col_n].astype(str).str.strip() == "O Shopping Co.,Ltd.")
            res = df[mask].copy()
            
            if not res.empty:
                # ย้าย B มาหน้าสุด
                cols = res.columns.tolist()
                parcel_id = cols.pop(1)
                res = res[[parcel_id] + cols]
                st.success(f"✅ พบข้อมูล {len(res)} รายการ")
                st.dataframe(res, use_container_width=True)
            else:
                st.warning("ไม่พบรายการที่ตรงเงื่อนไข (Ageing 5 และ O Shopping)")
        else:
            st.error("ไฟล์มีคอลัมน์ไม่ถึง N (14 คอลัมน์)")

else:
    st.info("กรุณาอัปโหลดไฟล์เพื่อเริ่มต้นการกรองข้อมูล")
