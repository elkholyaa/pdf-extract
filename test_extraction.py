#!/usr/bin/env python3
"""
Test script to demonstrate the Bill of Lading PDF extraction
"""

import os
import json
from extract_bol import BillOfLadingExtractor
from extract_bol_with_ocr import BillOfLadingExtractorWithOCR

def print_json(data):
    """Print JSON data in a readable format"""
    print(json.dumps(data, indent=2))

def main():
    # Path to the PDF file
    pdf_path = "065-2024 MBL MEDUP1966175.pdf"
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file '{pdf_path}' not found.")
        return
    
    print("=" * 80)
    print("Testing regular extraction (without OCR):")
    print("=" * 80)
    
    # Extract data using the regular extractor
    extractor = BillOfLadingExtractor(pdf_path)
    data = extractor.extract_data()
    output_file = extractor.save_to_json("output_regular.json")
    
    # Print summary
    print(f"Extracted data saved to {output_file}")
    print("\nSummary of extracted data:")
    print(f"BOL Number: {data.get('bol_number', 'Not found')}")
    print(f"Shipper: {data.get('shipper', {}).get('company_name', 'Not found')}")
    print(f"Consignee: {data.get('consignee', {}).get('company_name', 'Not found')}")
    print(f"Vessel: {data.get('vessel', {}).get('name', 'Not found')}")
    print(f"Containers: {len(data.get('containers', []))}")
    
    # Automatically run OCR extraction without asking
    print("\n" + "=" * 80)
    print("Testing OCR extraction:")
    print("=" * 80)
    
    try:
        # Extract data using the OCR extractor
        ocr_extractor = BillOfLadingExtractorWithOCR(pdf_path, use_ocr=True)
        ocr_data = ocr_extractor.extract_data()
        ocr_output_file = ocr_extractor.save_to_json("output_ocr.json")
        
        # Print summary
        print(f"Extracted data saved to {ocr_output_file}")
        print("\nSummary of extracted data (OCR):")
        print(f"BOL Number: {ocr_data.get('bol_number', 'Not found')}")
        print(f"Shipper: {ocr_data.get('shipper', {}).get('company_name', 'Not found')}")
        print(f"Consignee: {ocr_data.get('consignee', {}).get('company_name', 'Not found')}")
        print(f"Vessel: {ocr_data.get('vessel', {}).get('name', 'Not found')}")
        print(f"Containers: {len(ocr_data.get('containers', []))}")
        
        # Compare results
        print("\nComparing results between regular and OCR extraction:")
        
        # Compare BOL numbers
        if data.get('bol_number') == ocr_data.get('bol_number'):
            print("✓ BOL numbers match")
        else:
            print(f"✗ BOL numbers differ: {data.get('bol_number')} vs {ocr_data.get('bol_number')}")
        
        # Compare shipper company names
        if data.get('shipper', {}).get('company_name') == ocr_data.get('shipper', {}).get('company_name'):
            print("✓ Shipper company names match")
        else:
            print(f"✗ Shipper company names differ: {data.get('shipper', {}).get('company_name')} vs {ocr_data.get('shipper', {}).get('company_name')}")
        
        # Compare container counts
        if len(data.get('containers', [])) == len(ocr_data.get('containers', [])):
            print(f"✓ Container counts match: {len(data.get('containers', []))}")
        else:
            print(f"✗ Container counts differ: {len(data.get('containers', []))} vs {len(ocr_data.get('containers', []))}")
        
    except Exception as e:
        print(f"Error during OCR extraction: {str(e)}")
        print("Make sure Tesseract OCR is installed and in your PATH.")

if __name__ == "__main__":
    main() 