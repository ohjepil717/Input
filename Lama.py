import streamlit as st
import sqlite3
from datetime import datetime, timedelta

# SQLite 데이터베이스 초기화
def init_db():
    try:
        conn = sqlite3.connect("conversation.db")
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS conversations 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT, user_input TEXT, ai_response TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS car_numbers 
                     (id INTEGER PRIMARY KEY AUTOINCREMENT, car_number TEXT)''')
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"데이터베이스 초기화 실패: {str(e)}")
    finally:
        conn.close()

# 대화 저장
def save_conversation(user_input, ai_response):
    try:
        conn = sqlite3.connect("conversation.db")
        c = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO conversations (timestamp, user_input, ai_response) VALUES (?, ?, ?)", 
                  (timestamp, user_input, ai_response))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"대화 저장 실패: {str(e)}")
    finally:
        conn.close()

# 대화 불러오기
def load_conversations(date_filter=None):
    try:
        conn = sqlite3.connect("conversation.db")
        c = conn.cursor()
        if date_filter:
            c.execute("SELECT timestamp, user_input, ai_response FROM conversations WHERE date(timestamp) = ?", (date_filter,))
        else:
            c.execute("SELECT timestamp, user_input, ai_response FROM conversations")
        data = c.fetchall()
        return data
    except sqlite3.Error as e:
        st.error(f"대화 불러오기 실패: {str(e)}")
        return []
    finally:
        conn.close()

# 자동차 번호 업로드
def upload_car_numbers(car_list):
    try:
        conn = sqlite3.connect("conversation.db")
        c = conn.cursor()
        for car_number in car_list:
            c.execute("INSERT INTO car_numbers (car_number) VALUES (?)", (car_number,))
        conn.commit()
    except sqlite3.Error as e:
        st.error(f"자동차 번호 업로드 실패: {str(e)}")
    finally:
        conn.close()

# 자동차 번호 조회
def get_car_numbers():
    try:
        conn = sqlite3.connect("conversation.db")
        c = conn.cursor()
        c.execute("SELECT car_number FROM car_numbers")
        data = c.fetchall()
        return [row[0] for row in data]
    except sqlite3.Error as e:
        st.error(f"자동차 번호 조회 실패: {str(e)}")
        return []
    finally:
        conn.close()

# AI 응답 생성 (모델 로딩 제거, 기본 응답으로 대체)
def get_ai_response(user_input):
    yesterday = (datetime.now() - timedelta(days=1)).date()
    
    if "SQLite에 내정보를 저장해서 내일 알려줘" in user_input:
        save_conversation(user_input, "내일 알려드릴게요!")
        return "내일 알려드릴게요! 내일 이 앱을 다시 열어주세요."
    
    elif "내일 알려줘" in user_input or "내정보 보여줘" in user_input:
        conversations = load_conversations(yesterday)
        if conversations:
            return f"어제 저장된 정보: {', '.join([d[1] for d in conversations[:5]])}..."
        return "어제 저장된 정보가 없습니다."
    
    elif "자동차 번호" in user_input:
        car_numbers = get_car_numbers()
        if car_numbers:
            return f"저장된 자동차 번호: {', '.join(car_numbers[:5])}..."
        return "저장된 자동차 번호가 없습니다."
    
    return f"당신이 말한 것: {user_input}"

# Streamlit 앱
st.title("LLaMA와 대화하기 (SQLite 저장)")

init_db()

user_input = st.text_input("하고 싶은 말:")

if user_input:
    ai_response = get_ai_response(user_input)
    st.write(f"AI: {ai_response}")
    save_conversation(user_input, ai_response)

if st.button("저장된 대화 보기"):
    conversations = load_conversations()
    if conversations:
        for timestamp, user, ai in conversations:
            st.write(f"[{timestamp}] 사용자: {user} | AI: {ai}")
    else:
        st.write("저장된 대화가 없습니다.")

if st.button("자동차 번호 100개 업로드"):
    car_numbers = [f"12가 {i:04d}" for i in range(1, 101)]
    upload_car_numbers(car_numbers)
    st.success("자동차 번호 100개 업로드 완료!")
