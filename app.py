import streamlit as st
from driver_code import analysis_chain
import time

st.title('Fashion Store Assistant 🤖 💅🏼')

info = st.text_input('What do you want to know ?')

if info:
    progress_bar = st.progress(0)
    analysis_chain_var = analysis_chain()
    
    with st.spinner('Running LLM...'):
        for percent_complete in range(0, 101, 10):
            progress_bar.progress(percent_complete)
            time.sleep(0.5)

    answer = analysis_chain_var.run(info)

    st.success('Analysis Complete!')
    st.header("Answer")
    st.write(answer)
