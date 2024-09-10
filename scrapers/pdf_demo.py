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
        try:
            pdf_text = pdf_to_text(pdf)
        except Exception as e:
            print(f"Error extracting text from PDF #{currPdfIndex}: {e}")
            currPdfIndex += 1
            continue

        print(f"Regex searching employee and daterange...")
        try:
            employee_and_daterange = extract_employee_and_daterange(pdf_text)
        except Exception as e:
            print(
                f"Error extracting employee and daterange from PDF #{currPdfIndex}: {e}"
            )
            currPdfIndex += 1
            continue

        print("Regex searching communities and their summed total times...")
        try:
            community_timesums = extract_community_timesums(pdf_text)
        except Exception as e:
            print(f"Error extracting community timesums from PDF #{currPdfIndex}: {e}")
            currPdfIndex += 1
            continue

        print(f"Creating row in dataframe for each one...")
        try:
            for community, total_time in community_timesums.items():
                pdfs_data.append(
                    {
                        "File Name": pdf.name,  # Use pdf.name to get the file name
                        **employee_and_daterange,
                        "Community": community,
                        "Total Time": total_time,
                    }
                )
        except Exception as e:
            print(f"Error creating DataFrame row for PDF #{currPdfIndex}: {e}")
            currPdfIndex += 1
            continue

        currPdfIndex += 1
    print(f"\nFinished reading all pdfs! Returning created DataFrame")
    return pdfs_data


def pdf_to_text(pdf_file):
    text = ""
    # Read the content of the uploaded file
    pdf_bytes = pdf_file.read()
    document = fitz.open(stream=pdf_bytes, filetype="pdf")
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text += page.get_text()
    return text


def extract_employee_and_daterange(pdf_text):
    employee_info_match = re.search(
        r"([A-Za-z]+\s[A-Za-z]+)\s\(Employee Id:\s(\d+[A-Z]+\d+)\)", pdf_text
    )
    if employee_info_match:
        employee_name = employee_info_match.group(1)
        employee_id = employee_info_match.group(2)
    else:
        employee_name = None
        employee_id = None

    date_from_to_match = re.search(
        r"(\d{2}/\d{2}/\d{4})\s-\s(\d{2}/\d{2}/\d{4})", pdf_text
    )
    if date_from_to_match:
        date_from_to = f"{date_from_to_match.group(1)}-{date_from_to_match.group(2)}"
    else:
        date_from_to = None

    return {
        "employee_name": employee_name,
        "employee_id": employee_id,
        "date_from_to": date_from_to,
    }


def extract_community_timesums(pdf_text):
    # # Dummy implementation for debugging
    # return {"Community A": "10:00", "Community B": "5:00"}
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
