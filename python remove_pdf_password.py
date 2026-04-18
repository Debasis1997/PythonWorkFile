from pypdf import PdfReader, PdfWriter
import getpass
import os

folder    = input("Enter folder path : ").strip().strip('"').strip("'")
file_name = input("Enter file name   : ").strip().strip('"').strip("'")

# Add .pdf extension if not provided
if not file_name.lower().endswith(".pdf"):
    file_name += ".pdf"

INPUT_FILE  = os.path.join(folder, file_name)
OUTPUT_FILE = os.path.join(folder, file_name.replace(".pdf", "_unlocked.pdf"))

password = getpass.getpass("Enter PDF password: ")

reader = PdfReader(INPUT_FILE)

if not reader.is_encrypted:
    print("This PDF is not password protected.")
else:
    result = reader.decrypt(password)

    if result == 0:
        print("Wrong password. Please try again.")
    else:
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(OUTPUT_FILE, "wb") as f:
            writer.write(f)

        print(f"Done! Unlocked file saved to: {OUTPUT_FILE}")