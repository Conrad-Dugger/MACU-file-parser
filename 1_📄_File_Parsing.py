# ---- EXTERNAL MODULES ----
import streamlit as st
import pandas as pd
from io import BytesIO


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
from scrapers import pdf_demo as PDF_SCRAPER

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

    # -- DEMO AREA --
    print("\n# ---- PDF_DEMO() ---- ")
    pdf_demo()

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


# ---- PDF DEMO ----
@track_progress
def pdf_demo():
    st.header("PDF Scraper Demo", divider="red")

    # Button to upload multiple files
    uploaded_files = st.file_uploader(
        "Upload PDF files", type="pdf", accept_multiple_files=True
    )

    scraped_df = pd.DataFrame()
    # Only scrape when files get uploaded
    if uploaded_files:
        # Get a Panda DataFrame of all pdfs and the text we extract
        if st.button("Scrape Uploaded PDFs", key="scrape_pdfs"):
            print("Scraping uploaded PDFs...")
            scraped_data = PDF_SCRAPER.scrape(uploaded_files)

            # Debugging scraped_data
            print("Scraped data type:", type(scraped_data))
            print("Scraped data content:", scraped_data)

            # Convert the scraped data to a DataFrame
            print("Converting scraped data to DataFrame...")
            try:
                scraped_df = pd.DataFrame(scraped_data)
                print(f"Scraped DataFrame: {scraped_df}")
            except Exception as e:
                print(f"Error converting to DataFrame: {e}")
                st.error(f"Error converting to DataFrame: {e}")
                return

            # Check if DataFrame is empty
            if scraped_df.empty:
                print("DataFrame is empty.")
                st.write("No data scraped from PDFs.")
                return

            # Option to download the DataFrame as an Excel file
            if not scraped_df.empty:
                # Display scraped data
                print("Displaying scraped data...")
                st.write(scraped_df)

                # Convert DataFrame to Excel file
                print("Converting scraped data to Excel file...")
                output = BytesIO()
                try:
                    print("Before ExcelWriter")
                    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                        scraped_df.to_excel(writer, index=False, sheet_name="Sheet1")
                    print("After ExcelWriter")
                    output.seek(0)
                    # Provide user a download button
                    print("Providing download button...")
                    st.download_button(
                        label="Download Excel file",
                        data=output,
                        file_name="parsed_timesheets.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                except Exception as e:
                    print(f"Error during Excel file creation: {e}")
                    st.error(f"Error during Excel file creation: {e}")


if __name__ == "__main__":
    main()
