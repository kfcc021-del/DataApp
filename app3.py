import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 기본 설정
st.set_page_config(page_title="업무지원요청 데이터 시각화", layout="wide")

st.title("📊 업무지원요청 현황 대시보드")
st.write("CSV 파일을 업로드하면 요청 분류, 긴급도, 처리 상태별 현황을 확인할 수 있습니다.")

# 파일 업로더
uploaded_file = st.file_uploader("업무지원요청_합성자료.csv 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    try:
        # 데이터 불러오기
        df = pd.read_csv(uploaded_file)
        
        # 1. 데이터 미리보기
        st.subheader("📋 전체 데이터 미리보기")
        st.dataframe(df)
        
        st.markdown("---")
        st.subheader("📈 업무 요청 요약 통계 및 시각화")
        
        # 2. 분석할 컬럼 선택 (범주형 데이터 집계용)
        # 파일에 존재하는 컬럼만 선택지에 표시
        target_columns = [col for col in ['category', 'urgency', 'status', 'ai_handling'] if col in df.columns]
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("#### 분석 기준 선택")
            selected_col = st.selectbox(
                "어떤 기준으로 데이터를 볼까요?", 
                target_columns, 
                format_func=lambda x: {"category": "요청 분류별", "urgency": "긴급도별", "status": "처리 상태별", "ai_handling": "AI 처리 여부별"}.get(x, x)
            )
            
            # 선택한 컬럼의 항목별 건수 계산 (Value Counts)
            count_df = df[selected_col].value_counts().reset_index()
            count_df.columns = [selected_col, 'count']
            
            # 표 형태로 간단히 표시
            st.dataframe(count_df, use_container_width=True)

        with col2:
            st.write(f"#### {selected_col} 데이터 차트")
            
            # 차트 종류 선택
            chart_type = st.radio("차트 종류", ["막대 그래프 (Bar)", "파이 차트 (Pie)"], horizontal=True)
            
            # Plotly를 이용한 시각화
            if chart_type == "막대 그래프 (Bar)":
                fig = px.bar(count_df, x=selected_col, y='count', color=selected_col,
                             title=f"항목별 건수 ({selected_col})", text_auto=True)
                fig.update_layout(showlegend=False)
            else:
                fig = px.pie(count_df, names=selected_col, values='count', 
                             title=f"비중 분석 ({selected_col})", hole=0.3)
                
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"파일을 읽거나 처리하는 중 오류가 발생했습니다: {e}")
        
else:
    st.info("👆 위 영역에 CSV 파일을 업로드해 주세요.")
