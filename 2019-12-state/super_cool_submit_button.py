import streamlit as st
import st_state_patch

genres = ['pop', 'rock', 'electro', 'hip-hop', 'classical', 'jazz']

name = st.text_input("Name")
repetitions = st.slider("Repetitions", 1, 100)

def changed(*args):
    change_state = st.State()
    if not change_state:
        change_state.hash = 0
    hashed_args = hash(args)
    args_changed = hashed_args != change_state.hash
    change_state.hash = hashed_args
    return args_changed

def submit_button(*args):
    if changed(*args):
        if not st.button('Submit'):
            raise st.ScriptRunner.StopException

submit_button(name, repetitions)

st.write(' '.join([name] * repetitions))