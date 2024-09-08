# ---- EXTERNAL MODULES ----
import streamlit as st

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

# ---- INTERNAL MODULES ----
from utils.progress_bars import track_progress, remove_progress_bar

# ---- GLOBAL VARIABLES ----
SS = st.session_state  # Make a shorthand for session state
PRIMARY_COLOR = "blue"
SECONDARY_COLOR = "violet"
SIDEBAR_COLOR = "gray"


def main():
    # -- DEFAULT SECTIONS --
    print("\n# ---- MAIN() ---- ")
    set_banner()
    set_header()
    set_sidebar()

    # -- DATA PREP --
    check_statefulness()
    if SS.fresh_query_p1:
        print(f"Query marked as FRESH, running...")
        data_query()

    # -- DATA PARSE --
    apply_filters()
    apply_exclusions()

    # -- DATA SECTIONS --
    set_section_metrics()
    set_section_plots()
    set_section_tables()

    # -- CLEANUP --
    remove_progress_bar()


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
    st.header("Header", divider=PRIMARY_COLOR)


# ---- SIDEBAR ----
@track_progress
def set_sidebar():
    st.sidebar.header("Filters:", divider=SIDEBAR_COLOR)


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


# ---- TABLES ----
@track_progress
def set_section_tables():
    st.header("Tables", divider=SECONDARY_COLOR)


# ---- METRICS ----
@track_progress
def set_section_metrics():
    st.header("Metrics", divider=SECONDARY_COLOR)


# ---- PLOTS ----
@track_progress
def set_section_plots():
    st.header("Plots", divider=SECONDARY_COLOR)


# ---- QUERIES ----
@track_progress
def data_query():
    print(f"data_query()")
    SS.fresh_query_p1 = False


if __name__ == "__main__":
    main()
