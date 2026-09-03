import streamlit as st
import pickle
import pandas as pd

model=pickle.load(open('iplmodel.pkl','rb'))

df=pd.read_csv('TataIplcleaned.csv')

st.title('IPL Win Predictor')
st.text('Predicting IPL match winning in probability in eal time')

col1,col2=st.columns(2)

with col1:
    batting_team=st.selectbox('Batting Team',df['batting_team'].unique())

with col2:
    bowling_team=st.selectbox('Bowling_team',df['bowling_team'].unique())

if batting_team==bowling_team:
    st.error('Team Cannot be same')
    st.stop()

selected_city=st.selectbox('MatchCity',df['city'].dropna().unique())

target=st.number_input('Target',min_value=1,max_value=300)

st.divider()


col3, col4, col5, col6 = st.columns(4)

with col3:
    score = st.number_input('Score',min_value=0,max_value=300)

with col4:
    wickets_out = st.number_input('Wickets',min_value=0,max_value=10 )

with col5:
    overs = st.number_input('Overs',min_value=0,max_value=20)

with col6:
    balls = st.number_input( 'Balls',min_value=0,max_value=5)
if st.button("Predict Probability"):

    balls_bowled = overs * 6 + balls
    balls_left = 120 - balls_bowled

    runs_left = target - score
    wickets = 10 - wickets_out


    if balls_left <= 0:
        st.error("Match Over")
        st.stop()

    if runs_left <= 0:
        st.success(f"{batting_team} won the match!")
        st.balloons()
        st.stop()

    crr = score / (balls_bowled / 6) if balls_bowled > 0 else 0
    rrr = (runs_left * 6) / balls_left

    input_df = pd.DataFrame({'batting_team': [batting_team],'bowling_team': [bowling_team],'city': [selected_city],'runs_left': [runs_left],'balls_left': [balls_left],'wickets': [wickets],'total_runs_x': [target],'crr': [crr],'rrr': [rrr]})


    result = model.predict_proba(input_df)

    loss = result[0][0]
    win = result[0][1]


    st.divider()

    col7, col8 = st.columns(2)

    with col7:
        st.metric(batting_team, f"{round(win*100)}%")
        st.progress(int(win *100))

    with col8:
        st.metric(bowling_team, f"{round(loss*100)}%")
        st.progress(int(loss* 100))

    # Celebration
    if win > 0.65:
        st.balloons()