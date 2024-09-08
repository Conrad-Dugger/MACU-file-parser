import streamlit as st
import time, random

# Global variables for progress bar
PROGRESS = 0
PROGRESS_INCREMENT = 0.03
PROGRESS_PLACEHOLDER = st.empty()
PROGRESS_BAR = PROGRESS_PLACEHOLDER.progress(PROGRESS)
LOADING_STRINGS = ["Loadin' stuff..."]


def track_progress(func):
    def wrapper(*args, **kwargs):
        auto_increase_progress_bar()
        result = func(*args, **kwargs)
        auto_increase_progress_bar()
        return result

    return wrapper


def auto_increase_progress_bar():
    global PROGRESS_BAR
    global PROGRESS
    PROGRESS = PROGRESS + PROGRESS_INCREMENT
    if isinstance(PROGRESS_INCREMENT, float):
        if PROGRESS > 0.95:
            PROGRESS = 0.95
            PROGRESS_BAR.progress(PROGRESS, text=random.choice(LOADING_STRINGS))
    else:
        if PROGRESS > 95:
            PROGRESS = 95
            PROGRESS_BAR.progress(PROGRESS, text=random.choice(LOADING_STRINGS))
    PROGRESS_BAR.progress(PROGRESS, text=random.choice(LOADING_STRINGS))


def increase_progress_bar(increment):
    global PROGRESS_BAR
    global PROGRESS
    PROGRESS = PROGRESS + increment
    print(f"PROGRESS: {PROGRESS}")
    if PROGRESS > 100:
        PROGRESS = 100
        PROGRESS_BAR.progress(PROGRESS)
        print(f"ENDING PROGRESS BAR EARLY, ALTER INCREMENT")
        remove_progress_bar()
    PROGRESS_BAR.progress(PROGRESS)


def remove_progress_bar():
    print(f"remove_progress_bar()")
    global PROGRESS_BAR
    global PROGRESS
    global PROGRESS_PLACEHOLDER
    PROGRESS = 100
    PROGRESS_BAR.progress(PROGRESS)
    time.sleep(0.5)
    PROGRESS_PLACEHOLDER.empty()
