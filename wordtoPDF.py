import os
import sys
import subprocess

# ----------- WORD → PDF FUNCTION -----------
def word_to_pdf(input_file, output_file=None):
    try:
        from docx2pdf import convert

        if output_file:
            convert(input_file, output_file)
        else:
            convert(input_file)

        print(f"✅ Word → PDF done: {input_file}")

    except Exception:
        print("⚠️ docx2pdf failed, trying LibreOffice...")

        try:
            subprocess.run([
                "libreoffice",
                "--headless",
                "--convert-to", "pdf",
                input_file
            ], check=True)

            print(f"✅ Converted using LibreOffice: {input_file}")

        except Exception as e:
            print("❌ Conversion failed:", e)


# ----------- PDF → WORD FUNCTION -----------
def pdf_to_word(input_file, output_file=None):
    try:
        from pdf2docx import Converter

        if not output_file:
            output_file = input_file.replace(".pdf", ".docx")

        cv = Converter(input_file)
        cv.convert(output_file)
        cv.close()

        print(f"✅ PDF → Word done: {output_file}")

    except Exception as e:
        print("❌ Conversion failed:", e)


# ----------- SWITCH CASE USING MATCH -----------
def handle_conversion(mode, input_file, output_file):
    match mode:
        case "word2pdf":
            word_to_pdf(input_file, output_file)

        case "pdf2word":
            pdf_to_word(input_file, output_file)

        case _:
            print("❌ Invalid option!")
            print("Use: word2pdf or pdf2word")


# ----------- MAIN FUNCTION -----------
def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python converter.py word2pdf input.docx [output.pdf]")
        print("  python converter.py pdf2word input.pdf [output.docx]")
        return

    mode = sys.argv[1]
    input_file = sys.argv[2]
    output_file = sys.argv[3] if len(sys.argv) > 3 else None

    if not os.path.exists(input_file):
        print("❌ File not found:", input_file)
        return

    handle_conversion(mode, input_file, output_file)


# ----------- RUN -----------
if __name__ == "__main__":
    main()