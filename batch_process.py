#!/usr/bin/env python3
"""
Batch process multiple Bill of Lading PDFs
"""

import os
import sys
import json
import argparse
import glob
from extract_bol import BillOfLadingExtractor
from extract_bol_with_ocr import BillOfLadingExtractorWithOCR

def process_pdf(pdf_path, use_ocr=False, ocr_lang="eng", output_dir=None):
    """Process a single PDF file and return the extracted data"""
    print(f"Processing {pdf_path}...")
    
    try:
        if use_ocr:
            extractor = BillOfLadingExtractorWithOCR(pdf_path, use_ocr=True, ocr_lang=ocr_lang)
        else:
            extractor = BillOfLadingExtractor(pdf_path)
        
        data = extractor.extract_data()
        
        # Determine output path
        if output_dir:
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.json")
        else:
            output_path = None
        
        # Save to JSON
        output_file = extractor.save_to_json(output_path)
        
        print(f"  ✓ Extracted data saved to {output_file}")
        print(f"  ✓ BOL Number: {data.get('bol_number', 'Not found')}")
        print(f"  ✓ Shipper: {data.get('shipper', {}).get('company_name', 'Not found')}")
        print(f"  ✓ Consignee: {data.get('consignee', {}).get('company_name', 'Not found')}")
        print(f"  ✓ Vessel: {data.get('vessel', {}).get('name', 'Not found')}")
        print(f"  ✓ Containers: {len(data.get('containers', []))}")
        
        return True, data
    
    except Exception as e:
        print(f"  ✗ Error processing {pdf_path}: {str(e)}")
        return False, None

def main():
    parser = argparse.ArgumentParser(description='Batch process Bill of Lading PDFs')
    parser.add_argument('pdf_paths', nargs='+', help='Path(s) to PDF files or glob patterns')
    parser.add_argument('--output-dir', '-o', help='Output directory for JSON files')
    parser.add_argument('--ocr', action='store_true', help='Use OCR for text extraction')
    parser.add_argument('--lang', default='eng', help='OCR language (default: eng)')
    parser.add_argument('--summary', '-s', action='store_true', help='Generate a summary JSON file')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    if args.output_dir and not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    
    # Expand glob patterns and collect all PDF paths
    all_pdf_paths = []
    for path_pattern in args.pdf_paths:
        if '*' in path_pattern or '?' in path_pattern:
            matched_paths = glob.glob(path_pattern)
            if not matched_paths:
                print(f"Warning: No files match pattern '{path_pattern}'")
            all_pdf_paths.extend(matched_paths)
        else:
            all_pdf_paths.append(path_pattern)
    
    # Filter for PDF files
    pdf_paths = [p for p in all_pdf_paths if p.lower().endswith('.pdf') and os.path.isfile(p)]
    
    if not pdf_paths:
        print("Error: No PDF files found.")
        return 1
    
    print(f"Found {len(pdf_paths)} PDF file(s) to process.")
    
    # Process each PDF
    results = []
    success_count = 0
    
    for pdf_path in pdf_paths:
        success, data = process_pdf(
            pdf_path, 
            use_ocr=args.ocr, 
            ocr_lang=args.lang, 
            output_dir=args.output_dir
        )
        
        if success:
            success_count += 1
            if args.summary and data:
                # Add minimal info to summary
                results.append({
                    "filename": os.path.basename(pdf_path),
                    "bol_number": data.get("bol_number"),
                    "shipper": data.get("shipper", {}).get("company_name"),
                    "consignee": data.get("consignee", {}).get("company_name"),
                    "vessel": data.get("vessel", {}).get("name"),
                    "container_count": len(data.get("containers", [])),
                    "issue_date": data.get("issue_date"),
                    "port_of_loading": data.get("port_of_loading"),
                    "port_of_discharge": data.get("port_of_discharge")
                })
    
    # Print summary
    print("\nSummary:")
    print(f"Successfully processed {success_count} of {len(pdf_paths)} files.")
    
    # Save summary if requested
    if args.summary and results:
        summary_path = os.path.join(args.output_dir if args.output_dir else ".", "summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Summary saved to {summary_path}")
    
    return 0 if success_count == len(pdf_paths) else 1

if __name__ == "__main__":
    sys.exit(main()) 