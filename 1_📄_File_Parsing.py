# pip install --upgrade streamlit
import streamlit as st
import time, random


# ---- RENAME STREAMLIT VARIABLES ----
SS = st.session_state

# ---- CONFIG ----
st.set_page_config(
    page_title="MACU Parser",
    page_icon="assets/icons/indicode_favicon.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://www.example.com/help",
        "Report a Bug": "https://www.example.com/bug_report",
        "About": None,  # Removes the "About" menu item
    },
)

# ---- GLOBAL VARIABLES ----

# ---- GLOBAL REFRESHES ----
ITEM_UPDATE_SLEEP = 30
PROGRESS = 0
PROGRESS_INCREMENT = 0.03
PROGRESS_PLACEHOLDER = st.empty()
PROGRESS_BAR = PROGRESS_PLACEHOLDER.progress(PROGRESS)

# ---- GLOBAL LISTS ----
LOADING_STRINGS = ["Loadin' stuff..."]


def main():
    print("\n# ---- MAIN() ---- ")
    set_banner()
    set_header()
    set_sidebar()
    check_statefulness()

    if SS.fresh_query_p1:
        print(f"Query marked as FRESH, running...")
        data_query()

    apply_filters()
    apply_exclusions()
    set_section_metrics()
    set_section_plots()
    set_section_dataframes()
    remove_progress_bar()


# ---- WRAPPERS ----
def track_progress(func):
    def wrapper(*args, **kwargs):
        auto_increase_progress_bar()
        result = func(*args, **kwargs)
        auto_increase_progress_bar()
        return result

    return wrapper


# ---- BANNER ----
@track_progress
def set_banner():
    print("set_banner()")
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.image("assets/images/indicode_darkmode.png", use_column_width=True)


# ---- HEADER ----
@track_progress
def set_header():
    print("set_header()")
    st.header("Header", divider="blue")


# ---- SIDEBAR ----
@track_progress
def set_sidebar():
    st.sidebar.header("Filters:", divider="gray")


@track_progress
def check_statefulness():
    if "init_session_globals_p1" not in SS:
        SS.init_session_globals_p1 = True
    if SS.init_session_globals_p1:
        init_session_globals_p1()


# ---- APPLY EXCLUSIONS ----
@track_progress
def apply_exclusions():
    print("apply_exclusions()")


# ---- APPLY FILTERS ----
@track_progress
def apply_filters():
    print("apply_filters()")


# ---- SESSION GLOBALS ----
@track_progress
def init_session_globals_p1():
    print("init_session_globals_p1()")
    if "fresh_query_p1" not in SS:
        SS.fresh_query_p1 = True
    SS.init_session_globals_p1 = False


# ---- DATAFRAMES ----
@track_progress
def set_section_dataframes():
    st.header("Tables", divider="violet")


# ---- METRICS ----
@track_progress
def set_section_metrics():
    st.header("Metrics", divider="violet")


# ---- PLOTS ----
@track_progress
def set_section_plots():
    st.header("Plots", divider="violet")


# ---- QUERIES ----
@track_progress
def data_query():
    print(f"data_query()")
    SS.fresh_query_p1 = False


# ---- PROGRESS BAR FUNCS ----
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


if __name__ == "__main__":
    main()
