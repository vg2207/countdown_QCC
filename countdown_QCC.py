# App created by Data Professor http://youtube.com/dataprofessor
# GitHub repo of this app 
# Demo of this app

import streamlit as st
from streamlit_option_menu import option_menu 
from streamlit_extras.stylable_container import stylable_container
import time
import numpy as np

sample_rate = 44100 
duration = 0.9 #seconds
frequency = 150



# # CSS by andfanilo
# # Source: https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804
# def local_css(file_name):
#     with open(file_name) as f:
#         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# #def remote_css(url):
# #    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

# #def icon(icon_name):
# #    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

# local_css("style.css")
# #remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

st.set_page_config(layout="wide")

with st.sidebar:
    selected_main_menu = option_menu(
                            menu_title = None, #"Main Menu"
                            options = ["Presentation", "Q&A"],
                            icons = ["display", "question-circle"],
                            menu_icon = "cast",
                            default_index = 0,
                            orientation = "vertical",
                            styles={
                                "container": {"padding": "0!important", "background-color": "#fafafa"},
                                "nav-link": {"--hover-color": "#eee"},
                                "nav-link-selected": {"background-color": "#0349b3"},
                                }
                        )

if selected_main_menu == "Presentation" :


    col_1, col_2 = st.columns(2)
    with col_1 :
        with stylable_container(
                    "blue",
                    css_styles="""
                    button {
                        background-color: #0349b3;
                        color: white;
                    }""",
                ):
            button_clicked = st.button("Start", type="primary", use_container_width=True)
    with col_2 :
        with stylable_container(
                    "grey",
                    css_styles="""
                    button {
                        background-color: #86a3be;
                        color: white;
                    }""",
                ):
            button_clicked_2 = st.button("Reset", type="secondary", use_container_width=True)

    t1 = 3
    t2 = 15*60


    st.markdown("""
            <style>
            .big-font {
                font-size:200px !important;
                text-align: center;
                }
            .big-font-red {
                font-size:200px !important;
                text-align: center;
                color: #fb4c4c;
                }
            .dot-grey {
                height: 200px;
                width: 200px;
                background-color: #bbb;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            .dot-red {
                height: 200px;
                width: 200px;
                background-color: #fb4c4c;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            .dot-yellow {
                height: 200px;
                width: 200px;
                background-color: yellow;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            .dot-green {
                height: 200px;
                width: 200px;
                background-color: green;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            </style>
            """, unsafe_allow_html=True)



    if button_clicked:
        with st.empty():
            if button_clicked_2:
                st.empty()
            else :
                st.markdown('<p class="big-font">READY ?</p>', unsafe_allow_html=True)

                time.sleep(1)
                
                while t1:
                    mins, secs = divmod(t1, 60)
                    timer = t1
                    st.markdown(f'<p class="big-font">{timer}</p>', unsafe_allow_html=True)
                    st.audio(np.sin((frequency*3) * np.linspace(0, seconds, seconds * sample_rate, False) * 2 * np.pi),
                             sample_rate=sample_rate,
                             autoplay=True)
                    time.sleep(0.1)
                    t1 -= 1
                
                st.markdown('<p class="big-font">GO !</p>', unsafe_allow_html=True)
                st.audio(np.sin((frequency*4) * np.linspace(0, seconds*2, seconds*2 * sample_rate, False) * 2 * np.pi),
                             sample_rate=sample_rate,
                             autoplay=True)
                time.sleep(1)
                st.empty()

        with st.empty():
            if button_clicked_2:
                st.empty()
            else :
                while t2:
                    mins2, secs2 = divmod(t2, 60)
                    timer2 = '{:02d}:{:02d}'.format(mins2, secs2)
                    
                    
                    with st.container():
                        if t2 == 300 or t2 == 600 :
                            with st.empty():
                                st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
                            left_col, middle_col, right_col = st.columns(3)
                            with left_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-green"></p>', unsafe_allow_html=True)
                            with middle_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with right_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            st.audio(np.sin((frequency*3) * np.linspace(0, seconds, seconds * sample_rate, False) * 2 * np.pi),
                                     sample_rate=sample_rate,
                                     autoplay=True)
                            time.sleep(0.1)
                            t2 -= 1
                        elif t2 > 300 :
                            with st.empty() :
                                st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
                            left_col, middle_col, right_col = st.columns(3)
                            with left_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-green"></p>', unsafe_allow_html=True)
                            with middle_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with right_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            time.sleep(1)
                            t2 -= 1
                        # elif t2 == 300 :
                        #     with st.empty():
                        #         st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
                        #     left_col, middle_col, right_col = st.columns(3)
                        #     with left_col:
                        #         with st.empty():
                        #             st.markdown(f'<p class="dot-green"></p>', unsafe_allow_html=True)
                        #     with middle_col:
                        #         with st.empty():
                        #             st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                        #     with right_col:
                        #         with st.empty():
                        #             st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                        #     winsound.Beep(frequency*2, duration)
                        #     time.sleep(0.1)
                        #     t2 -= 1
                        elif t2 > 60 :
                            with st.empty() :
                                st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
                            left_col, middle_col, right_col = st.columns(3)
                            with left_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with middle_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-yellow"></p>', unsafe_allow_html=True)
                            with right_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            time.sleep(1)
                            t2 -= 1
                        elif t2 == 60 :
                            with st.empty():
                                st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
                            left_col, middle_col, right_col = st.columns(3)
                            with left_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with middle_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with right_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-red"></p>', unsafe_allow_html=True)
                            st.audio(np.sin((frequency*3) * np.linspace(0, seconds, seconds * sample_rate, False) * 2 * np.pi),
                                     sample_rate=sample_rate,
                                     autoplay=True)
                            time.sleep(0)
                            t2 -= 1
                        elif t2 > 5 :
                            with st.empty() :
                                st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
                            left_col, middle_col, right_col = st.columns(3)
                            with left_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with middle_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with right_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-red"></p>', unsafe_allow_html=True)
                            time.sleep(1)
                            t2 -= 1
                        else :
                            with st.empty():
                                st.markdown(f'<p class="big-font-red">{timer2}</p>', unsafe_allow_html=True)
                            
                            left_col, middle_col, right_col = st.columns(3)
                            with left_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with middle_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
                            with right_col:
                                with st.empty():
                                    st.markdown(f'<p class="dot-red"></p>', unsafe_allow_html=True)
                            st.audio(np.sin((frequency*2) * np.linspace(0, seconds, seconds * sample_rate, False) * 2 * np.pi),
                                     sample_rate=sample_rate,
                                     autoplay=True)
                            time.sleep(0.1)
                            t2 -= 1


                with st.empty():        
                    st.markdown('<p class="big-font">TIME IS UP !</p>', unsafe_allow_html=True)
                    st.audio(np.sin((frequency*4) * np.linspace(0, seconds*2, seconds*2 * sample_rate, False) * 2 * np.pi),
                             sample_rate=sample_rate,
                             autoplay=True)
                    time.sleep(0)
                    
    if button_clicked_2:
        st.empty()





elif selected_main_menu == "Q&A" :



    col_10, col_20, col_30 = st.columns(3)
    with col_10 :
        with stylable_container(
                    "blue",
                    css_styles="""
                    button {
                        background-color: #0349b3;
                        color: white;
                    }""",
                ):
            button_clicked_10 = st.button("Question", type="primary", use_container_width=True)
    with col_20 :
        with stylable_container(
                    "grey",
                    css_styles="""
                    button {
                        background-color: #86a3be;
                        color: white;
                    }""",
                ):
            button_clicked_20 = st.button("Reset", type="secondary", use_container_width=True)
    with col_30 :
        with stylable_container(
                    "blue",
                    css_styles="""
                    button {
                        background-color: #0349b3;
                        color: white;
                    }""",
                ):
            button_clicked_30 = st.button("Answer", type="primary", use_container_width=True)

    t10 = 2*60
    t20 = 3*60


    st.markdown("""
            <style>
            .big-font {
                font-size:200px !important;
                text-align: center;
                }
            .big-font-red {
                font-size:200px !important;
                text-align: center;
                color: #fb4c4c;
                }
            .dot-grey {
                height: 200px;
                width: 200px;
                background-color: #bbb;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            .dot-red {
                height: 200px;
                width: 200px;
                background-color: #fb4c4c;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            .dot-yellow {
                height: 200px;
                width: 200px;
                background-color: yellow;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            .dot-green {
                height: 200px;
                width: 200px;
                background-color: green;
                border-radius: 50%;
                display: inline-block;
                left: 28%;
                position: relative;
                }
            </style>
            """, unsafe_allow_html=True)



    if button_clicked_10:
        with st.empty():
            if button_clicked_20:
                st.empty()
            else :

                st.markdown('<p class="big-font">GO !</p>', unsafe_allow_html=True)

                time.sleep(1)
                
                while t10:

                    mins10, secs10 = divmod(t10, 60)
                    timer10 = '{:02d}:{:02d}'.format(mins10, secs10)
                    st.markdown(f'<p class="big-font">{timer10}</p>', unsafe_allow_html=True)
                    # winsound.Beep(frequency, duration)
                    time.sleep(1)
                    t10 -= 1

                with st.empty():        
                    st.markdown('<p class="big-font">TIME IS UP !</p>', unsafe_allow_html=True)
                    st.audio(np.sin((frequency*3) * np.linspace(0, seconds*2, seconds*2 * sample_rate, False) * 2 * np.pi),
                             sample_rate=sample_rate,
                             autoplay=True)
                    time.sleep(0)


    if button_clicked_30 :
        with st.empty():
            if button_clicked_20:
                st.empty()
            else :

                while t20:
                    mins20, secs20 = divmod(t20, 60)
                    timer20 = '{:02d}:{:02d}'.format(mins20, secs20)
                    
                    
                    with st.container():
                        if t20 > 3 :
                            with st.empty() :
                                st.markdown(f'<p class="big-font">{timer20}</p>', unsafe_allow_html=True)
                            time.sleep(1)
                            t20 -= 1
                    
                        else :
                            with st.empty():
                                st.markdown(f'<p class="big-font-red">{timer20}</p>', unsafe_allow_html=True)
                            st.audio(np.sin((frequency) * np.linspace(0, seconds, seconds * sample_rate, False) * 2 * np.pi),
                             sample_rate=sample_rate,
                             autoplay=True)
                            time.sleep(0.1)
                            t20 -= 1


                with st.empty():        
                    st.markdown('<p class="big-font">TIME IS UP !</p>', unsafe_allow_html=True)
                    st.audio(np.sin((frequency*4) * np.linspace(0, seconds*2, seconds*2 * sample_rate, False) * 2 * np.pi),
                             sample_rate=sample_rate,
                             autoplay=True)
                    time.sleep(0)
                    
    if button_clicked_20:
        st.empty()
