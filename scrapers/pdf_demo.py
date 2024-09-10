import fitz  # PyMuPDF
import re
import pandas as pd


def scrape(pdf_files):
    print(f"User uploaded {len(pdf_files)} pdf files!")
    currPdfIndex = 1
    pdfs_data = []
    for pdf in pdf_files:
        # skip file if it's somehow not a PDF
        if pdf is None:
            currPdfIndex += 1
            continue

        print(f"\nExtracting text from PDF #{currPdfIndex}...")
        # TODO: provide folder of the PDF files used in scrape
        pdf_text = pdf_to_text(pdf)

        print(f"Regex searching employee and daterange...")
        # Process the PDF text for items that are identical per row of the DataFrame
        employee_and_daterange = extract_employee_and_daterange(pdf_text)

        print("Regex searching communities and their summed total times...")
        # Process the PDF text for items that are unique per row of the DataFrame
        community_timesums = extract_community_timesums(pdf_text)

        print(f"Creating row in dataframe for each one...")
        # iterate over each community and its total time, creating a new row for each.
        for community, total_time in community_timesums.items():
            pdfs_data.append(
                {
                    "File Name": pdf,
                    **employee_and_daterange,
                    "Community": community,
                    "Total Time": total_time,
                }
            )
        currPdfIndex += 1
    print(f"\nFinished reading all pdfs! Returning created DataFrame")
    # Return scraped data[]
    return pdfs_data


def pdf_to_text(pdf):
    text = ""
    # Since we aren't using a locally directory, convert the file to bytes for fitz to read
    pdf_bytes = pdf.read()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


def extract_employee_and_daterange(pdf_text):
    # Capture employee name and ID together since they are on the same line
    employee_info_match = re.search(
        r"([A-Za-z]+\s[A-Za-z]+)\s\(Employee Id:\s(\d+[A-Z]+\d+)\)", pdf_text
    )
    if employee_info_match:
        employee_name = employee_info_match.group(1)
        employee_id = employee_info_match.group(2)
    else:
        employee_name = None
        employee_id = None

    # Date From To "MM/DD/YYYY-MM/DD/YYYY"
    date_from_to_match = re.search(
        r"(\d{2}/\d{2}/\d{4})\s-\s(\d{2}/\d{2}/\d{4})", pdf_text
    )
    if date_from_to_match:
        date_from_to = f"{date_from_to_match.group(1)}-{date_from_to_match.group(2)}"
    else:
        date_from_to = None

    return {
        "Employee Name": employee_name,
        "Employee Id": employee_id,
        "Date From To": date_from_to,
        "Date From": date_from_to_match.group(1),
        "Date To": date_from_to_match.group(2),
    }


def extract_community_timesums(pdf_text):
    # Pattern to match Community (Named "Property" in the PDF) and Total Time
    property_time_pattern = r"\s+(\w[\w\s]+)\n\d+\.\d+\n(\d+\.\d+)"
    communities_times = re.findall(property_time_pattern, pdf_text)

    # Summing Total Time for each community
    community_time_sum = {}
    for community, time in communities_times:
        if community in community_time_sum:
            community_time_sum[community] += float(time)
        else:
            community_time_sum[community] = float(time)

    print(f"Found {len(community_time_sum)} communities!")
    return community_time_sum
