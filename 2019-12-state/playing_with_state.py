import streamlit as st
import st_state_patch
import st_rerun_patch

data = ["eins", "zwei", "drei", "vier", "fünf"]
categories = ["good", "bad"]

s = st.State()
if not s:
    s.annotations = {} # <- prefer direct initializer?

st.show(s.annotations)

annotating_index = len(s.annotations)
if annotating_index >= len(data):
    st.success('No more annotations!')
else:
    item = data[annotating_index]
    category = st.selectbox('Category for %s?' % item, categories)

    if st.button('Submit'):
        s.annotations[item] = category
        st.write('About to rerun...')
        st.rerun()  # REQUIRED otherwise we get an off-by-one error
