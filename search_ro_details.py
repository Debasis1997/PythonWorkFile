
import re
import sys
from pathlib import Path

import pdfplumber
from rapidfuzz import fuzz, process
from tqdm import tqdm

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
)


# =========================================================
# 1. FILE PATHS
# =========================================================

DOWNLOADS = Path(r"C:\\Users\\Debasis\\Downloads")

INPUT_PDF = DOWNLOADS / "cc-iocl-fuel-station-list.pdf"
OUTPUT_PDF = DOWNLOADS / "RO_Search_Result.pdf"


# =========================================================
# 2. RO NAMES TO SEARCH (25 STATIONS)
# =========================================================

RO_NAMES = [
    "Paikaray Fuel Point",
    "Binod Bihari Kisan Seva Kendra",
    "Omm Sai Filling Station",
    "Mahapatra Service Station",
    "Meghdoot Filling Station",
    "Maa Bayani Kisan Seva Kendra",
    "Bhairavi Filling Station",
    "Bisma Filling Station",
    "Mahapatra Filling Station, Argul",
    "Mahima Kisan Seva Kendra",
    "Kumar Kisan Seva Kendra",
    "Budheswar Kisan Seva Kendra",
    "Shreekhetra Kisan Seva Kendra",
    "Balaji Fuels",
    "Baba Sai Fuel Station",
    "Prabhukrupa Fuels KSK",
    "Chariot Highway Service",
    "Shreekrishna Filling Station",
    "A.B.C. Kisan Seva Kendra",
    "Maa Sulia Devi Kisan Seva Kendra",
    "Matrukrupa Auto Fuels",
    "Maa Batamangala Filling Station",
    "Nandi Filling Station",
    "Paikaray Filling Station, Jankia",
    "Maa Santoshi Trading",
]

# Approximate matches must be reviewed against the source PDF.
FUZZY_THRESHOLD = 85


# =========================================================
# 3. NORMALIZE TEXT
# =========================================================

def normalize(value):
    if value is None:
        return ""

    value = str(value).upper().strip()
    value = re.sub(r"[^A-Z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


# =========================================================
# 4. READ TABLES FROM THE PDF
# =========================================================

def read_pdf_tables(pdf_path):
    records = []

    with pdfplumber.open(str(pdf_path)) as pdf:
        total_pages = len(pdf.pages)

        if total_pages == 0:
            raise ValueError("The PDF contains no pages.")

        for page_number, page in enumerate(
            tqdm(
                pdf.pages,
                total=total_pages,
                desc="Reading PDF",
                unit="page",
                dynamic_ncols=True,
            ),
            start=1,
        ):
            tables = page.extract_tables()

            for table in tables:
                if not table:
                    continue

                header_row = None
                indexes = {}

                # Locate the header row
                for row_number, row in enumerate(table):
                    cells = [normalize(cell) for cell in row]

                    ro_index = next(
                        (
                            i for i, cell in enumerate(cells)
                            if "RO NAME" in cell
                        ),
                        None,
                    )

                    merchant_index = next(
                        (
                            i for i, cell in enumerate(cells)
                            if "MERCHANT ID" in cell
                        ),
                        None,
                    )

                    terminal_index = next(
                        (
                            i for i, cell in enumerate(cells)
                            if "TERMINAL ID" in cell
                        ),
                        None,
                    )

                    if (
                        ro_index is not None
                        and merchant_index is not None
                        and terminal_index is not None
                    ):
                        header_row = row_number
                        indexes = {
                            "ro": ro_index,
                            "merchant": merchant_index,
                            "terminal": terminal_index,
                        }
                        break

                if header_row is None:
                    continue

                # Extract records below the header
                for row in table[header_row + 1:]:
                    if not row:
                        continue

                    if max(indexes.values()) >= len(row):
                        continue

                    ro_name = str(
                        row[indexes["ro"]] or ""
                    ).strip()

                    merchant_id = str(
                        row[indexes["merchant"]] or ""
                    ).strip()

                    terminal_id = str(
                        row[indexes["terminal"]] or ""
                    ).strip()

                    if not normalize(ro_name):
                        continue

                    if normalize(ro_name) in {
                        "RO NAME",
                        "TOTAL",
                    }:
                        continue

                    records.append({
                        "RO Name": ro_name,
                        "Merchant ID": merchant_id,
                        "Terminal ID": terminal_id,
                        "Source Page": page_number,
                    })

    return records


# =========================================================
# 5. SEARCH THE 25 RO NAMES
# =========================================================

def search_ro_names(records, search_names):
    results = []
    unmatched = []

    if not records:
        raise ValueError(
            "No table records were extracted. "
            "The PDF may be scanned or its table layout "
            "may require different extraction settings."
        )

    normalized_records = [
        (record, normalize(record["RO Name"]))
        for record in records
    ]

    available_names = list(dict.fromkeys(
        name
        for _, name in normalized_records
        if name
    ))

    for search_name in tqdm(
        search_names,
        total=len(search_names),
        desc="Searching RO names",
        unit="RO",
        dynamic_ncols=True,
    ):
        query = normalize(search_name)

        if not query:
            continue

        # First: exact match
        matched_names = [
            name for name in available_names
            if name == query
        ]

        match_type = "Exact"

        # Second: partial match
        if not matched_names:
            matched_names = [
                name for name in available_names
                if query in name or name in query
            ]
            match_type = "Partial"

        # Third: fuzzy match
        if not matched_names:
            best = process.extractOne(
                query,
                available_names,
                scorer=fuzz.ratio,
                score_cutoff=FUZZY_THRESHOLD,
            )

            if best:
                matched_names = [best[0]]
                match_type = f"Approximate ({best[1]}%)"

        if not matched_names:
            unmatched.append(search_name)
            continue

        for record, normalized_name in normalized_records:
            if normalized_name not in matched_names:
                continue

            results.append({
                "RO Name": record["RO Name"],
                "Merchant ID": record["Merchant ID"],
                "Terminal ID": record["Terminal ID"],
                "Source Page": record["Source Page"],
                "Search Name": search_name,
                "Match Type": match_type,
            })

    # Remove duplicate records
    unique_results = []
    seen = set()

    for record in results:
        key = (
            normalize(record["RO Name"]),
            record["Merchant ID"],
            record["Terminal ID"],
            record["Source Page"],
        )

        if key not in seen:
            seen.add(key)
            unique_results.append(record)

    return unique_results, unmatched


# =========================================================
# 6. GENERATE THE RESULT PDF
# =========================================================

def create_result_pdf(results, unmatched, output_path):
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        leftMargin=12 * mm,
        rightMargin=12 * mm,
        topMargin=12 * mm,
        bottomMargin=12 * mm,
    )

    story = [
        Paragraph(
            "IndianOil Retail Outlet Search Report",
            styles["Title"],
        ),
        Spacer(1, 5 * mm),
        Paragraph(
            f"Requested RO names: {len(RO_NAMES)}",
            styles["Normal"],
        ),
        Paragraph(
            f"Matching records found: {len(results)}",
            styles["Normal"],
        ),
        Paragraph(
            f"RO names not found: {len(unmatched)}",
            styles["Normal"],
        ),
        Spacer(1, 5 * mm),
    ]

    data = [[
        "RO Name",
        "Merchant ID",
        "Terminal ID",
        "PDF Page",
        "Match Type",
    ]]

    for record in results:
        data.append([
            Paragraph(
                str(record["RO Name"]),
                styles["BodyText"],
            ),
            str(record["Merchant ID"]),
            str(record["Terminal ID"]),
            str(record["Source Page"]),
            str(record["Match Type"]),
        ])

    if not results:
        data.append([
            "No matching records found",
            "",
            "",
            "",
            "",
        ])

    table = Table(
        data,
        colWidths=[
            85 * mm,
            42 * mm,
            40 * mm,
            22 * mm,
            40 * mm,
        ],
        repeatRows=1,
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#168CC4")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [
            colors.white,
            colors.HexColor("#EAF5FA"),
        ]),
    ]))

    story.append(table)

    # List names not found in the source PDF
    if unmatched:
        story.extend([
            Spacer(1, 8 * mm),
            Paragraph(
                "RO Names Not Found",
                styles["Heading2"],
            ),
        ])

        for name in unmatched:
            story.append(
                Paragraph(str(name), styles["BodyText"])
            )

    # List approximate matches that need verification
    approximate = [
        record for record in results
        if record["Match Type"].startswith("Approximate")
    ]

    if approximate:
        story.extend([
            Spacer(1, 8 * mm),
            Paragraph(
                "Approximate Matches - Please Verify",
                styles["Heading2"],
            ),
        ])

        for record in approximate:
            story.append(
                Paragraph(
                    f"Requested: {record['Search Name']} | "
                    f"PDF: {record['RO Name']} | "
                    f"Page: {record['Source Page']}",
                    styles["BodyText"],
                )
            )

    doc.build(story)


# =========================================================
# 7. MAIN PROGRAM
# =========================================================

def main():
    print("=" * 60)
    print("INDIANOIL RO SEARCH PROGRAM")
    print("=" * 60)

    if not INPUT_PDF.exists():
        print("\nERROR: Original PDF not found.")
        print(f"Expected file: {INPUT_PDF}")
        print(
            "\nCheck the exact filename and extension "
            "in your Downloads folder."
        )
        return

    if not RO_NAMES:
        print("ERROR: Add RO names to the RO_NAMES list.")
        return

    try:
        print(f"\nInput PDF: {INPUT_PDF}")
        print(f"RO names to search: {len(RO_NAMES)}\n")

        # Step 1: Read the PDF
        records = read_pdf_tables(INPUT_PDF)
        print(f"\nRecords extracted: {len(records)}")

        # Step 2: Search the names
        results, unmatched = search_ro_names(
            records,
            RO_NAMES,
        )

        # Step 3: Generate the output PDF
        print("\nGenerating result PDF...")

        with tqdm(
            total=1,
            desc="Creating report",
            unit="PDF",
            dynamic_ncols=True,
        ) as progress:
            create_result_pdf(
                results,
                unmatched,
                OUTPUT_PDF,
            )
            progress.update(1)

        # Step 4: Print summary
        print("\n" + "=" * 60)
        print("SEARCH COMPLETED")
        print("=" * 60)
        print(f"Requested RO names: {len(RO_NAMES)}")
        print(f"Matching records: {len(results)}")
        print(f"Names not found: {len(unmatched)}")
        print(f"\nOutput PDF:\n{OUTPUT_PDF}")

        if unmatched:
            print("\nRO names not found:")
            for name in unmatched:
                print(f"  - {name}")

        if results:
            print("\nMatched records:")
            for record in results:
                print(
                    f"{record['RO Name']} | "
                    f"Merchant ID: {record['Merchant ID']} | "
                    f"Terminal ID: {record['Terminal ID']} | "
                    f"Match: {record['Match Type']}"
                )

        print("\nPlease verify approximate matches before use.")

    except Exception as error:
        print(f"\nERROR: {error}")
        print(
            "\nIf the PDF is scanned or contains image-only tables, "
            "OCR may be required."
        )


if __name__ == "__main__":
    main()
