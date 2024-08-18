import streamlit as st
from datetime import datetime
import pandas as pd

# 앱 제목
st.title("👣 맨발 걷기 진행 상황 기록 앱")

# 세션 상태 초기화
if 'users' not in st.session_state:
    st.session_state.users = {}

# 사용자 이름 입력
user_name = st.text_input("사용자 이름을 입력하세요:")

# 사용자 정보 초기화
if user_name:
    if user_name not in st.session_state.users:
        st.session_state.users[user_name] = {'records': {}, 'total_steps': 0}
        st.success(f"사용자 '{user_name}'가 등록되었습니다.")
    else:
        st.info(f"환영합니다, '{user_name}'님!")

    user_data = st.session_state.users[user_name]

    # 날짜 입력
    input_date = st.date_input("기록할 날짜를 선택하세요:", datetime.now())

    # 장소 및 걸음 수 입력
    place_input = st.text_input("장소를 입력하세요:")
    steps_input = st.number_input("걸음 수를 입력하세요:", min_value=0)

    # 기록 추가
    if st.button("📥 기록 추가"):
        if place_input and steps_input > 0:
            date_str = input_date.strftime("%Y-%m-%d")  # 날짜 포맷
            if date_str not in user_data['records']:
                user_data['records'][date_str] = []
            user_data['records'][date_str].append({'place': place_input, 'steps': steps_input})
            user_data['total_steps'] += steps_input  # 누계 걸음 수 업데이트
            st.success(f"✅ '{place_input}'에서 {steps_input} 걸음이 추가되었습니다.")
        else:
            st.error("❌ 장소와 걸음 수 정보를 입력해 주세요.")

    # 수정 기능
    st.subheader("기록 수정")
    if user_data['records']:
        edit_date = st.selectbox("수정할 날짜를 선택하세요:", list(user_data['records'].keys()))
        if edit_date:
            selected_records = user_data['records'][edit_date]
            record_to_edit = st.selectbox("수정할 기록을 선택하세요:", range(len(selected_records)))
            selected_record = selected_records[record_to_edit]

            new_place = st.text_input("새로운 장소:", value=selected_record['place'])
            new_steps = st.number_input("새로운 걸음 수:", value=selected_record['steps'], min_value=0)

            if st.button("🔄 수정하기"):
                if new_place and new_steps >= 0:
                    step_difference = new_steps - selected_record['steps']
                    # 기록 수정
                    user_data['records'][edit_date][record_to_edit] = {'place': new_place, 'steps': new_steps}
                    user_data['total_steps'] += step_difference  # 누계 걸음 수 업데이트
                    st.success("✅ 기록이 수정되었습니다.")
                else:
                    st.error("❌ 장소와 걸음 수 정보를 입력해 주세요.")

    # 누계 걸음 수 표시
    st.subheader("누계 기록")
    st.write(f"🏆 총 걸음 수: {user_data['total_steps']} 걸음")

    # 과거 기록 표시
    st.subheader("과거 기록")
    if user_data['records']:
        records_df = []
        for date, records in user_data['records'].items():
            for record in records:
                records_df.append({'날짜': date, '장소': record['place'], '걸음 수': record['steps']})

        # 데이터프레임으로 변환 및 날짜 정렬 (오름차순)
        records_df = pd.DataFrame(records_df)
        records_df['날짜'] = pd.to_datetime(records_df['날짜'])  # 날짜 데이터로 변환
        records_df = records_df.sort_values(by='날짜', ascending=True)  # 날짜 오름차순 정렬
        st.table(records_df)  # 데이터를 테이블 형식으로 표시
    else:
        st.write("📉 기록이 없습니다.")

    # 한 장소의 모든 기록 보기
    st.subheader("특정 장소 기록 보기")
    if user_data['records']:
        unique_places = set()
        for records in user_data['records'].values():
            for record in records:
                unique_places.add(record['place'])
        selected_place = st.selectbox("장소를 선택하세요:", list(unique_places))

        # 선택된 장소에 대한 모든 기록
        place_records_df = []
        for date, records in user_data['records'].items():
            for record in records:
                if record['place'] == selected_place:
                    place_records_df.append({'날짜': date, '걸음 수': record['steps']})

        # 장소별 기록 테이블
        if place_records_df:
            place_records_df = pd.DataFrame(place_records_df)
            place_records_df['날짜'] = pd.to_datetime(place_records_df['날짜'])  # 날짜 데이터로 변환
            place_records_df = place_records_df.sort_values(by='날짜', ascending=True)  # 날짜 오름차순 정렬
            st.write(f"📍 '{selected_place}'에서의 기록:")
            st.table(place_records_df)  # 장소별 기록을 테이블로 표시
        else:
            st.write(f"📉 '{selected_place}'에 대한 기록이 없습니다.")
else:
    st.warning("사용자 이름을 입력해 주세요.")