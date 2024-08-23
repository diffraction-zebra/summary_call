import pathlib
import streamlit as st

from typing import Literal, IO

from pipeline.speech_model import accepted_formats
from pipeline.run import run_pipeline


if 'state' not in st.session_state:
    st.session_state['state']: Literal['upload', 'summarize'] = 'upload'
if 'audio' not in st.session_state:
    st.session_state['audio']: IO[bytes] | None = None

if st.session_state['state'] == 'upload':
    uploaded_file = st.file_uploader(
        "Choose an audio file", accept_multiple_files=False
    )

    summarize = st.button('Сделать рeзюме.')

    if summarize:
        if uploaded_file is None:
            st.write('Загрузите файл, чтобы начать суммаризацию.')
        elif pathlib.Path(uploaded_file.name).suffix not in accepted_formats:
            st.write(f'''На данный момент мы поддерживаем только определенные форматы аудио: {' '.join(accepted_formats)}. Попробуйте перeвести аудио в допустимый формат.''')
        else:
            st.session_state['audio'] = uploaded_file

elif st.session_state['state'] == 'summarize':
    with st.spinner('Мы уже начали обрабатывать ваше аудио.'):
        summary = run_pipeline(st.session_state['audio'])
    st.code(summary, language="markdown")

    back = st.button('Обработать другое аудио')

    if back:
        st.session_state['state'] = 'upload'
        st.session_state['audio'] = None
        st.rerun()
