
import os
import json
from datetime import datetime
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
import pytesseract

P = "\033[95m"
C = "\033[96m"
G = "\033[92m"
R = "\033[91m"
Y = "\033[93m"
W = "\033[97m"
B = "\033[1m"
RESET = "\033[0m"

metadata = None
ocr_text = None

def banner():
    os.system("clear")
    print(C + "╔" + "═"*42 + "╗")
    print("║" + P + B + "       RISHIKESH JS       " + C + "║")
    print("║" + W + "       PREMIUM EDITION    " + C + "║")
    print("╚" + "═"*42 + "╝" + RESET)

def menu():
    options = [
        "Extract Image Metadata",
        "Document Text Scan (OCR)",
        "Export Metadata to TXT",
        "Export Metadata to JSON",
        "Exit Tool"
    ]
    print(P + "\n       MAIN CONTROL PANEL" + RESET)
    for i, option in enumerate(options, 1):
        print(C + f"       [{i}] " + W + option + RESET)
    print(P + "\n       DEVELOPED BY RISHIKESH JS" + RESET)

def get_path():
    path = input(C + "\nEnter Image Full Path: " + W)
    path = os.path.expanduser(path.strip().strip('"').strip("'"))
    if not os.path.isfile(path):
        print(R + "[ERROR] File not found!" + RESET)
        return None
    return path

def extract_metadata(path):
    try:
        with Image.open(path) as img:
            data = {
                "Developer": "RISHIKESH JS",
                "File Name": os.path.basename(path),
                "Format": img.format,
                "Width": img.width,
                "Height": img.height,
                "Dimensions": str(img.size),
                "Mode": img.mode,
                "File Size": str(round(os.path.getsize(path)/1024, 2)) + " KB",
                "Extracted At": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                "EXIF Metadata": {}
            }
            for tag_id, value in img.getexif().items():
                data["EXIF Metadata"][TAGS.get(tag_id, str(tag_id))] = str(value)
            return data
    except Exception as e:
        print(R + "[ERROR] " + str(e) + RESET)
        return None

def show_metadata():
    if metadata is None:
        print(Y + "Extract metadata first!" + RESET)
        return
    print(G + "\n[✓] METADATA RESULTS" + RESET)
    print(json.dumps(metadata, indent=4, ensure_ascii=False))

def document_scan(path):
    global ocr_text
    try:
        with Image.open(path) as img:
            img = ImageOps.grayscale(img)
            img = ImageOps.autocontrast(img)
            text = pytesseract.image_to_string(img, lang="eng")

        ocr_text = text
        print(G + "\n[✓] OCR SCAN COMPLETED!" + RESET)
        print(C + "\nEXTRACTED DOCUMENT TEXT:" + RESET)
        print(text if text.strip() else "No readable text found.")

        if text.strip():
            choice = input("\nSave OCR text? (y/n): ").lower()
            if choice == "y":
                with open("Rishikesh_OCR.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                print(G + "OCR text saved!" + RESET)

    except Exception as e:
        print(R + "[OCR ERROR] " + str(e) + RESET)

def save_txt():
    if metadata is None:
        print(Y + "No metadata available!" + RESET)
        return
    with open("Rishikesh_Metadata.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(metadata, indent=4, ensure_ascii=False))
    print(G + "TXT Saved Successfully!" + RESET)

def save_json():
    if metadata is None:
        print(Y + "No metadata available!" + RESET)
        return
    with open("Rishikesh_Metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)
    print(G + "JSON Saved Successfully!" + RESET)

def main():
    global metadata

    while True:
        banner()
        menu()
        choice = input(C + "\nRISHIKESH JS >> " + W).strip()

        if choice == "1":
            path = get_path()
            if path:
                result = extract_metadata(path)
                if result:
                    metadata = result
                    print(G + "\nExtraction Successful!" + RESET)
                    show_metadata()

        elif choice == "2":
            path = get_path()
            if path:
                document_scan(path)

        elif choice == "3":
            save_txt()

        elif choice == "4":
            save_json()

        elif choice == "5":
            print(P + "\nTHANK YOU FOR USING RISHIKESH JS!" + RESET)
            break

        else:
            print(R + "Invalid Option!" + RESET)

        input(W + "\nPress ENTER to continue..." + RESET)

if __name__ == "__main__":
    main()
