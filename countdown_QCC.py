import base64
import io
import time
import wave

import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.stylable_container import stylable_container
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

FREQ = 150          # base frequency (Hz)
DURATION = 0.9      # base beep length (seconds)
SAMPLE_RATE = 44100

# ---------------------------------------------------------------- styles
st.markdown(
    """
    <style>
    .big-font, .big-font-red {
        font-size: 200px !important;
        text-align: center;
        line-height: 1.1;
        margin: 0;
    }
    .big-font-red { color: #fb4c4c; }
    .dots {
        display: flex;
        justify-content: center;
        gap: 80px;
        margin-top: 20px;
    }
    .dot {
        height: 200px;
        width: 200px;
        border-radius: 50%;
        display: inline-block;
    }
    .dot-grey   { background-color: #bbb; }
    .dot-red    { background-color: #fb4c4c; }
    .dot-yellow { background-color: yellow; }
    .dot-green  { background-color: green; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------- sound
# Placeholder that holds the (invisible) audio player. It lives in the sidebar
# so it doesn't push the main layout around.
beep_slot = st.sidebar.empty()


@st.cache_data
def make_wav_b64(freq: float, duration: float) -> str:
    """Build a sine-wave WAV file and return it base64-encoded."""
    n = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, n, endpoint=False)  # seconds, not ms
    wave_data = 0.3 * np.sin(2 * np.pi * freq * t)

    # short fade in/out to avoid clicking
    fade = int(SAMPLE_RATE * 0.01)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)

    pcm = (wave_data * env * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(pcm.tobytes())
    return base64.b64encode(buf.getvalue()).decode()


def play_beep(freq: float = FREQ, duration: float = DURATION):
    """Play a beep. Every call renders a brand-new player (unique comment),
    so the browser autoplays it even if the sound is identical to the last."""
    st.session_state["beep_n"] = st.session_state.get("beep_n", 0) + 1
    b64 = make_wav_b64(freq, duration)
    html = (
        f'<audio autoplay><source src="data:audio/wav;base64,{b64}" '
        f'type="audio/wav"></audio><!-- beep {st.session_state["beep_n"]} -->'
    )
    with beep_slot:
        components.html(html, height=0)


# --------------------------------------------------------------- helpers
def show(slot, text, dots=None, red=False):
    """Draw the big text (and optional 3 dots) into one placeholder."""
    cls = "big-font-red" if red else "big-font"
    html = f'<p class="{cls}">{text}</p>'
    if dots:
        html += '<div class="dots">'
        html += "".join(f'<span class="dot dot-{c}"></span>' for c in dots)
        html += "</div>"
    slot.markdown(html, unsafe_allow_html=True)


def fmt(sec):
    return "{:02d}:{:02d}".format(*divmod(sec, 60))


def run_countdown(slot, seconds, frame_fn):
    """Call frame_fn(remaining) once per second, without clock drift."""
    start = time.monotonic()
    for i, remaining in enumerate(range(seconds, 0, -1)):
        frame_fn(remaining)
        time.sleep(max(0, start + (i + 1) - time.monotonic()))


def blue_button(key, label):
    with stylable_container(
        key, css_styles="button {background-color: #0349b3; color: white;}"
    ):
        return st.button(label, type="secondary", use_container_width=True, key=key + "_btn")


def grey_button(key, label):
    with stylable_container(
        key, css_styles="button {background-color: #86a3be; color: white;}"
    ):
        return st.button(label, type="secondary", use_container_width=True, key=key + "_btn")


# --------------------------------------------------------------- sidebar
with st.sidebar:
    selected_main_menu = option_menu(
        menu_title=None,
        options=["Presentation", "Q&A"],
        icons=["display", "question-circle"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "nav-link": {"--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#0349b3"},
        },
    )

# NOTE: In Streamlit, clicking *any* button interrupts the running script and
# reruns it. So pressing "Reset" automatically stops a running timer – no extra
# logic needed; the page just comes back to its idle state.

# ---------------------------------------------------------- Presentation
if selected_main_menu == "Presentation":
    col_1, col_2 = st.columns(2)
    with col_1:
        start_clicked = blue_button("pres_start", "Start")
    with col_2:
        grey_button("pres_reset", "Reset")

    display = st.empty()

    if start_clicked:
        # --- READY ? 3 2 1 GO !
        show(display, "READY ?")
        time.sleep(1)

        def intro_frame(n):
            show(display, n)
            play_beep(FREQ * 3, DURATION)

        run_countdown(display, 3, intro_frame)

        show(display, "GO !")
        play_beep(FREQ * 4, DURATION * 2)
        time.sleep(2)

        # --- 15 minute main timer
        def main_frame(remaining):
            if remaining >= 300:
                dots = ["green", "grey", "grey"]
            elif remaining > 60:
                dots = ["grey", "yellow", "grey"]
            else:
                dots = ["grey", "grey", "red"]

            show(display, fmt(remaining), dots, red=remaining <= 5)

            if remaining in (600, 300, 60):
                play_beep(FREQ * 3, DURATION)
            elif remaining <= 5:
                play_beep(FREQ * 2, DURATION)

        run_countdown(display, 15 * 60, main_frame)

        show(display, "TIME IS UP !")
        play_beep(FREQ * 4, DURATION * 2)
        time.sleep(2)

# ------------------------------------------------------------------- Q&A
else:
    col_10, col_20, col_30 = st.columns(3)
    with col_10:
        question_clicked = blue_button("qa_question", "Question")
    with col_20:
        grey_button("qa_reset", "Reset")
    with col_30:
        answer_clicked = blue_button("qa_answer", "Answer")

    display = st.empty()

    if question_clicked:
        show(display, "GO !")
        time.sleep(1)

        def q_frame(remaining):
            show(display, fmt(remaining))
            # play_beep(FREQ, DURATION)

        run_countdown(display, 2 * 60, q_frame)

        show(display, "TIME IS UP !")
        play_beep(FREQ * 3, DURATION * 2)
        time.sleep(2)

    if answer_clicked:

        def a_frame(remaining):
            show(display, fmt(remaining), red=remaining <= 3)
            if remaining <= 3:
                play_beep(FREQ, DURATION)

        run_countdown(display, 3 * 60, a_frame)

        show(display, "TIME IS UP !")
        play_beep(FREQ * 4, DURATION * 2)
        time.sleep(2)



# # App created by Data Professor http://youtube.com/dataprofessor
# # GitHub repo of this app 
# # Demo of this app

# import streamlit as st
# from streamlit_option_menu import option_menu 
# from streamlit_extras.stylable_container import stylable_container
# import time
# import numpy as np

# def play_beep(freq=150, duration=900, sample_rate=44100):
#     t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
#     wave = 0.3 * np.sin(2 * np.pi * freq * t)
#     st.audio(wave, sample_rate=sample_rate, autoplay=True)
    



# frequency = 150  # Set Frequency To 2500 Hertz
# duration = 900  # Set Duration To 1000 ms == 1 second


# # # CSS by andfanilo
# # # Source: https://discuss.streamlit.io/t/creating-a-nicely-formatted-search-field/1804
# # def local_css(file_name):
# #     with open(file_name) as f:
# #         st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# # #def remote_css(url):
# # #    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

# # #def icon(icon_name):
# # #    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

# # local_css("style.css")
# # #remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

# st.set_page_config(layout="wide")

# with st.sidebar:
#     selected_main_menu = option_menu(
#                             menu_title = None, #"Main Menu"
#                             options = ["Presentation", "Q&A"],
#                             icons = ["display", "question-circle"],
#                             menu_icon = "cast",
#                             default_index = 0,
#                             orientation = "vertical",
#                             styles={
#                                 "container": {"padding": "0!important", "background-color": "#fafafa"},
#                                 "nav-link": {"--hover-color": "#eee"},
#                                 "nav-link-selected": {"background-color": "#0349b3"},
#                                 }
#                         )

# if selected_main_menu == "Presentation" :


#     col_1, col_2 = st.columns(2)
#     with col_1 :
#         with stylable_container(
#                     "blue",
#                     css_styles="""
#                     button {
#                         background-color: #0349b3;
#                         color: white;
#                     }""",
#                 ):
#             button_clicked = st.button("Start", type="primary", use_container_width=True)
#     with col_2 :
#         with stylable_container(
#                     "grey",
#                     css_styles="""
#                     button {
#                         background-color: #86a3be;
#                         color: white;
#                     }""",
#                 ):
#             button_clicked_2 = st.button("Reset", type="secondary", use_container_width=True)

#     t1 = 3
#     t2 = 15*60


#     st.markdown("""
#             <style>
#             .big-font {
#                 font-size:200px !important;
#                 text-align: center;
#                 }
#             .big-font-red {
#                 font-size:200px !important;
#                 text-align: center;
#                 color: #fb4c4c;
#                 }
#             .dot-grey {
#                 height: 200px;
#                 width: 200px;
#                 background-color: #bbb;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             .dot-red {
#                 height: 200px;
#                 width: 200px;
#                 background-color: #fb4c4c;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             .dot-yellow {
#                 height: 200px;
#                 width: 200px;
#                 background-color: yellow;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             .dot-green {
#                 height: 200px;
#                 width: 200px;
#                 background-color: green;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             </style>
#             """, unsafe_allow_html=True)



#     if button_clicked:
#         with st.empty():
#             if button_clicked_2:
#                 st.empty()
#             else :
#                 st.markdown('<p class="big-font">READY ?</p>', unsafe_allow_html=True)

#                 time.sleep(1)
                
#                 while t1:
#                     mins, secs = divmod(t1, 60)
#                     timer = t1
#                     st.markdown(f'<p class="big-font">{timer}</p>', unsafe_allow_html=True)
#                     play_beep(frequency*3, duration)
#                     # winsound.Beep(frequency*3, duration)
#                     # time.sleep(0.1)
#                     time.sleep(1)
#                     t1 -= 1
                
#                 st.markdown('<p class="big-font">GO !</p>', unsafe_allow_html=True)
#                 play_beep(frequency*4, duration*2)
#                 # winsound.Beep(frequency*4, duration*2)
#                 # time.sleep(1)
#                 time.sleep(2)
#                 st.empty()

#         with st.empty():
#             if button_clicked_2:
#                 st.empty()
#             else :
#                 while t2:
#                     mins2, secs2 = divmod(t2, 60)
#                     timer2 = '{:02d}:{:02d}'.format(mins2, secs2)
                    
                    
#                     with st.container():
#                         if t2 == 300 or t2 == 600 :
#                             with st.empty():
#                                 st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
#                             left_col, middle_col, right_col = st.columns(3)
#                             with left_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-green"></p>', unsafe_allow_html=True)
#                             with middle_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with right_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             play_beep(frequency*3, duration)
#                             # winsound.Beep(frequency*3, duration)
#                             # time.sleep(0.1)
#                             time.sleep(1)
#                             t2 -= 1
#                         elif t2 > 300 :
#                             with st.empty() :
#                                 st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
#                             left_col, middle_col, right_col = st.columns(3)
#                             with left_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-green"></p>', unsafe_allow_html=True)
#                             with middle_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with right_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             time.sleep(1)
#                             t2 -= 1
#                         # elif t2 == 300 :
#                         #     with st.empty():
#                         #         st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
#                         #     left_col, middle_col, right_col = st.columns(3)
#                         #     with left_col:
#                         #         with st.empty():
#                         #             st.markdown(f'<p class="dot-green"></p>', unsafe_allow_html=True)
#                         #     with middle_col:
#                         #         with st.empty():
#                         #             st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                         #     with right_col:
#                         #         with st.empty():
#                         #             st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                         #     winsound.Beep(frequency*2, duration)
#                         #     time.sleep(0.1)
#                         #     t2 -= 1
#                         elif t2 > 60 :
#                             with st.empty() :
#                                 st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
#                             left_col, middle_col, right_col = st.columns(3)
#                             with left_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with middle_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-yellow"></p>', unsafe_allow_html=True)
#                             with right_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             time.sleep(1)
#                             t2 -= 1
#                         elif t2 == 60 :
#                             with st.empty():
#                                 st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
#                             left_col, middle_col, right_col = st.columns(3)
#                             with left_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with middle_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with right_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-red"></p>', unsafe_allow_html=True)
#                             play_beep(frequency*3, duration)
#                             # winsound.Beep(frequency*3, duration)
#                             # time.sleep(0)
#                             time.sleep(1)
#                             t2 -= 1
#                         elif t2 > 5 :
#                             with st.empty() :
#                                 st.markdown(f'<p class="big-font">{timer2}</p>', unsafe_allow_html=True)
                            
#                             left_col, middle_col, right_col = st.columns(3)
#                             with left_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with middle_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with right_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-red"></p>', unsafe_allow_html=True)
#                             time.sleep(1)
#                             t2 -= 1
#                         else :
#                             with st.empty():
#                                 st.markdown(f'<p class="big-font-red">{timer2}</p>', unsafe_allow_html=True)
                            
#                             left_col, middle_col, right_col = st.columns(3)
#                             with left_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with middle_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-grey"></p>', unsafe_allow_html=True)
#                             with right_col:
#                                 with st.empty():
#                                     st.markdown(f'<p class="dot-red"></p>', unsafe_allow_html=True)
#                             play_beep(frequency*2, duration)
#                             # winsound.Beep(frequency*2, duration)
#                             # time.sleep(0.1)
#                             time.sleep(1)
#                             t2 -= 1


#                 with st.empty():        
#                     st.markdown('<p class="big-font">TIME IS UP !</p>', unsafe_allow_html=True)
#                     play_beep(frequency*4, duration*2)
#                     # winsound.Beep(frequency*4, duration*2)
#                     # time.sleep(0)
#                     time.sleep(2)
                    
#     if button_clicked_2:
#         st.empty()





# elif selected_main_menu == "Q&A" :



#     col_10, col_20, col_30 = st.columns(3)
#     with col_10 :
#         with stylable_container(
#                     "blue",
#                     css_styles="""
#                     button {
#                         background-color: #0349b3;
#                         color: white;
#                     }""",
#                 ):
#             button_clicked_10 = st.button("Question", type="primary", use_container_width=True)
#     with col_20 :
#         with stylable_container(
#                     "grey",
#                     css_styles="""
#                     button {
#                         background-color: #86a3be;
#                         color: white;
#                     }""",
#                 ):
#             button_clicked_20 = st.button("Reset", type="secondary", use_container_width=True)
#     with col_30 :
#         with stylable_container(
#                     "blue",
#                     css_styles="""
#                     button {
#                         background-color: #0349b3;
#                         color: white;
#                     }""",
#                 ):
#             button_clicked_30 = st.button("Answer", type="primary", use_container_width=True)

#     t10 = 2*60
#     t20 = 3*60


#     st.markdown("""
#             <style>
#             .big-font {
#                 font-size:200px !important;
#                 text-align: center;
#                 }
#             .big-font-red {
#                 font-size:200px !important;
#                 text-align: center;
#                 color: #fb4c4c;
#                 }
#             .dot-grey {
#                 height: 200px;
#                 width: 200px;
#                 background-color: #bbb;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             .dot-red {
#                 height: 200px;
#                 width: 200px;
#                 background-color: #fb4c4c;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             .dot-yellow {
#                 height: 200px;
#                 width: 200px;
#                 background-color: yellow;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             .dot-green {
#                 height: 200px;
#                 width: 200px;
#                 background-color: green;
#                 border-radius: 50%;
#                 display: inline-block;
#                 left: 28%;
#                 position: relative;
#                 }
#             </style>
#             """, unsafe_allow_html=True)



#     if button_clicked_10:
#         with st.empty():
#             if button_clicked_20:
#                 st.empty()
#             else :

#                 st.markdown('<p class="big-font">GO !</p>', unsafe_allow_html=True)

#                 time.sleep(1)
                
#                 while t10:

#                     mins10, secs10 = divmod(t10, 60)
#                     timer10 = '{:02d}:{:02d}'.format(mins10, secs10)
#                     st.markdown(f'<p class="big-font">{timer10}</p>', unsafe_allow_html=True)
#                     play_beep(frequency, duration)
#                     # winsound.Beep(frequency, duration)
#                     time.sleep(1)
#                     t10 -= 1

#                 with st.empty():        
#                     st.markdown('<p class="big-font">TIME IS UP !</p>', unsafe_allow_html=True)
#                     play_beep(frequency*3, duration*2)
#                     # winsound.Beep(frequency*3, duration*2)
#                     # time.sleep(0)
#                     time.sleep(2)


#     if button_clicked_30 :
#         with st.empty():
#             if button_clicked_20:
#                 st.empty()
#             else :

#                 while t20:
#                     mins20, secs20 = divmod(t20, 60)
#                     timer20 = '{:02d}:{:02d}'.format(mins20, secs20)
                    
                    
#                     with st.container():
#                         if t20 > 3 :
#                             with st.empty() :
#                                 st.markdown(f'<p class="big-font">{timer20}</p>', unsafe_allow_html=True)
#                             time.sleep(1)
#                             t20 -= 1
                    
#                         else :
#                             with st.empty():
#                                 st.markdown(f'<p class="big-font-red">{timer20}</p>', unsafe_allow_html=True)
#                             play_beep(frequency, duration)
#                             # winsound.Beep(frequency, duration)
#                             # time.sleep(0.1)
#                             time.sleep(1)
#                             t20 -= 1


#                 with st.empty():        
#                     st.markdown('<p class="big-font">TIME IS UP !</p>', unsafe_allow_html=True)
#                     play_beep(frequency*4, duration*2)
#                     # winsound.Beep(frequency*4, duration*2)
#                     # time.sleep(0)
#                     time.sleep(2)
                    
#     if button_clicked_20:
#         st.empty()
