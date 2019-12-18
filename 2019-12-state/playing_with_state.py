# import streamlit as st
# import st_state_patch

# def f(x):
#     s = st.State()
#     if not s:
#         s.count = 0
#     s.count += x
#     return s.count

# st.show(f(1))
# st.show(f(1))

import streamlit as st
import st_state_patch

def counter(key):
    st.subheader('Counter %s' % key)
    s = st.State()
    if not s:
        s.counter = 0
    if st.button('Increment %s' % key):
        s.counter += 1
    if st.button('Decrement %s' % key):
        s.counter -= 1
    st.write('Counter %s: `%i`' %(key, s.counter))
    

counter('A')
counter('B')
