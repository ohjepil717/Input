import streamlit as st
import sqlite3

# SQLite에서 데이터 불러오기
def fetch_memories():
    conn = sqlite3.connect('ai_memory.db')
    c = conn.cursor()
    c.execute('SELECT * FROM memories ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def store_memory(text):
    conn = sqlite3.connect('ai_memory.db')
    c = conn.cursor()
    c.execute('INSERT INTO memories (text) VALUES (?)', (text,))
    conn.commit()
    conn.close()

# Streamlit 인터페이스
st.title('AI Memory')

# 입력란
memory_input = st.text_input('Add a new memory')

# 메모리 추가 버튼
if st.button('Save Memory'):
    if memory_input:
        store_memory(memory_input)
        st.success('Memory saved successfully!')

# 저장된 메모리 출력
memories = fetch_memories()
for memory in memories:
    st.write(f"ID: {memory[0]}, Memory: {memory[1]}, Timestamp: {memory[2]}")
