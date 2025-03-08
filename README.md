# Bill of Lading PDF Extractor

This Python script extracts structured data from Bill of Lading (BOL) PDF documents and converts it to JSON format.

## Features

- Extracts key information from Bill of Lading PDFs including:
  - BOL number
  - Shipper information
  - Consignee information
  - Notify party information
  - Vessel and voyage details
  - Container information
  - Dates (issue date, shipped date)
  - Port information
  - Cargo details

- Handles layout variations in PDFs
- Provides both structured data and raw text for each section
- Outputs data in JSON format
- Optional OCR support for PDFs with poor text extraction

## Requirements

- Python 3.6+
- PyMuPDF (fitz)
- For OCR support:
  - Tesseract OCR (must be installed separately)
  - pytesseract
  - Pillow

## Installation

1. Clone this repository or download the script files
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. For OCR support, install Tesseract OCR:
   - On macOS: `brew install tesseract`
   - On Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
   - On Windows: Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)

## Usage

### Basic Usage

```bash
python extract_bol.py path/to/your/bol.pdf
```

This will extract data from the PDF and save it to a JSON file with the same name as the PDF.

### With OCR Support

If the PDF has poor text extraction, you can use the OCR version:

```bash
python extract_bol_with_ocr.py path/to/your/bol.pdf --ocr
```

### Specify Output File

```bash
python extract_bol.py path/to/your/bol.pdf --output output.json
```

### Example

```bash
python extract_bol.py ./public/065-2024\ MBL\ MEDUP1966175.pdf
```

With OCR:

```bash
python extract_bol_with_ocr.py 065-2024\ MBL\ MEDUP1966175.pdf --ocr --lang eng
```

## Output Format

The script generates a JSON file with the following structure:

```json
{
  "document_type": "Bill of Lading",
  "filename": "example.pdf",
  "bol_number": "MEDUP1966175",
  "shipper": {
    "company_name": "COMPANY NAME",
    "address": "Full address",
    "raw_text": "Raw text from the shipper section"
  },
  "consignee": {
    "company_name": "CONSIGNEE COMPANY",
    "address": "Full address",
    "raw_text": "Raw text from the consignee section"
  },
  "notify_party": {
    "company_name": "NOTIFY PARTY",
    "address": "Full address",
    "raw_text": "Raw text from the notify party section"
  },
  "vessel": {
    "name": "VESSEL NAME",
    "voyage": "VOYAGE NUMBER"
  },
  "containers": [
    {
      "container_number": "ABCD1234567",
      "seal_number": "SEAL123",
      "package_count": "44",
      "weight": "25000.00",
      "context": "Surrounding text for context"
    }
  ],
  "issue_date": "28-Nov-2024",
  "shipped_date": "24-Nov-2024",
  "port_of_loading": "PARANAGUA, PR, BRAZIL",
  "port_of_discharge": "JEBEL ALI, DUBAI",
  "place_of_receipt": "Place information",
  "place_of_delivery": "Delivery information",
  "cargo": {
    "package_count": "88",
    "gross_weight_kg": "50000.00",
    "description": "Description of cargo"
  }
}
```

## Handling Different PDF Layouts

The script uses multiple strategies to extract data:
1. Regular expression pattern matching on the full text
2. Region-based extraction for specific areas of the document
3. Context-based extraction for related information

If you encounter PDFs with different layouts, you may need to adjust the extraction patterns or regions in the script.

## Choosing Between Regular and OCR Version

- Use `extract_bol.py` for PDFs with good text extraction (faster)
- Use `extract_bol_with_ocr.py` for:
  - Scanned PDFs
  - PDFs with poor text extraction
  - PDFs with unusual layouts or formatting

## Limitations

- The script is designed for a specific Bill of Lading format and may require adjustments for different formats
- OCR accuracy depends on the quality of the PDF
- Complex tables or unusual layouts may not be fully captured

## License

MIT 