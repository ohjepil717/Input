import streamlit as st
import pandas as pd
import re

# 🔒 비밀번호 입력
password = st.text_input("암호 입력:", type="password")

if password == "369369":
    st.success("접속 성공! 자동 입력 시스템 시작합니다.")
    
    # 🔹 기존 데이터 저장용
    if "data" not in st.session_state:
        st.session_state.data = []

    st.title("자동 입력 프로그램")
    st.write("메모장에서 복사한 텍스트를 자동으로 분류하여 입력합니다.")

    # 🔹 사용자 입력
    user_text = st.text_area("메모장 내용 입력", "")

    # 🔹 정규식 패턴
    date_pattern = r"\d{4}[-/]\d{2}[-/]\d{2}"  # YYYY-MM-DD 또는 YYYY/MM/DD
    time_pattern = r"\d{1,2}:\d{2}"  # HH:MM
    phone_pattern = r"010[-\d]{8,9}"  # 010-xxxx-xxxx 또는 010xxxxxxxx
    price_pattern = r"(\d{1,3}(?:,\d{3})+원|\d+원|만원|천만원)"  # 10,000원, 만원, 천만원

    # 🔹 데이터 추출
    dates = re.findall(date_pattern, user_text)
    times = re.findall(time_pattern, user_text)
    phones = re.findall(phone_pattern, user_text)
    prices = re.findall(price_pattern, user_text)

    # 🔹 가격 숫자로 변환
    price_map = {"만원": 10000, "천만원": 10000000}
    clean_prices = []
    for p in prices:
        p = p.replace(",", "").replace("원", "")
        clean_prices.append(price_map.get(p, int(p)))

    # 🔹 데이터 저장
    new_entry = {
        "날짜": ", ".join(dates) if dates else "-",
        "시간": ", ".join(times) if times else "-",
        "전화번호": ", ".join(phones) if phones else "-",
        "가격": ", ".join(map(str, clean_prices)) if clean_prices else "-"
    }
    st.session_state.data.append(new_entry)

    # 🔹 현재 데이터 표시
    st.write("### 자동 입력 결과")
    df = pd.DataFrame(st.session_state.data)
    st.dataframe(df)

    # 🔹 엑셀 저장 버튼
    if st.button("📂 엑셀로 저장"):
        df.to_excel("자동입력_결과.xlsx", index=False)
        st.success("✅ 엑셀 저장 완료! '자동입력_결과.xlsx' 파일을 확인하세요.")

else:
    st.error("🚨 암호가 틀렸습니다.")