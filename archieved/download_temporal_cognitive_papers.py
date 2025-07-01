#!/usr/bin/env python3
import csv
import os
import requests
import time
import re
from pathlib import Path

def get_pdf_url(url, domain_category):
    """Convert various URL formats to direct PDF URLs"""
    if not url:
        return None
        
    # arXiv URLs
    if 'arxiv.org' in url:
        if '/pdf/' in url:
            return url
        elif '/abs/' in url:
            return url.replace('/abs/', '/pdf/') + '.pdf'
        elif '/html/' in url:
            paper_id = re.search(r'(\d+\.\d+)', url)
            if paper_id:
                return f"https://arxiv.org/pdf/{paper_id.group(1)}.pdf"
    
    # PMC URLs
    elif 'pmc.ncbi.nlm.nih.gov' in url:
        if '/pdf/' in url:
            return url
        else:
            # Try to construct PDF URL
            pmc_match = re.search(r'PMC(\d+)', url)
            if pmc_match:
                return f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc_match.group(1)}/pdf/"
    
    # MDPI URLs
    elif 'mdpi.com' in url and '/pdf' not in url:
        if url.endswith('/'):
            return url + 'pdf'
        else:
            return url + '/pdf'
    
    # Frontiers URLs
    elif 'frontiersin.org' in url and '/pdf' not in url:
        return url + '/pdf'
    
    # For other open access, try the URL as-is first
    return url

def sanitize_filename(title, url):
    """Create a safe filename from paper title and URL"""
    # Clean the title
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = re.sub(r'\s+', '_', title.strip())
    
    # Limit length
    if len(title) > 80:
        title = title[:80]
    
    # Try to get a good identifier from URL
    if 'arxiv.org' in url:
        # Extract arXiv ID
        match = re.search(r'(\d+\.\d+)', url)
        if match:
            return f"temporal_cognitive_arxiv_{match.group(1)}_{title}.pdf"
    elif 'pmc.ncbi.nlm.nih.gov' in url:
        # Extract PMC ID
        match = re.search(r'PMC(\d+)', url)
        if match:
            return f"temporal_cognitive_pmc_{match.group(1)}_{title}.pdf"
    elif 'mdpi.com' in url:
        return f"temporal_cognitive_mdpi_{title}.pdf"
    elif 'frontiersin.org' in url:
        return f"temporal_cognitive_frontiers_{title}.pdf"
    
    # Fallback
    return f"temporal_cognitive_{title}.pdf"

def download_pdf(url, filename, papers_dir, max_retries=3):
    """Download PDF with retries and error handling"""
    filepath = papers_dir / filename
    
    # Skip if file already exists
    if filepath.exists():
        print(f"  ✓ Already exists: {filename}")
        return True, "already_exists"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"  → Downloading: {filename}")
            response = requests.get(url, headers=headers, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                # Check if it's actually a PDF
                content_type = response.headers.get('content-type', '').lower()
                if 'pdf' in content_type or response.content.startswith(b'%PDF'):
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    print(f"  ✓ Downloaded: {filename} ({len(response.content)} bytes)")
                    return True, "success"
                else:
                    print(f"  ⚠ Not a PDF: {content_type}")
                    return False, f"not_pdf_{content_type}"
            else:
                print(f"  ⚠ HTTP {response.status_code}: {url}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                
        except requests.exceptions.RequestException as e:
            print(f"  ⚠ Error (attempt {attempt + 1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
    
    return False, "failed_after_retries"

def download_temporal_cognitive_papers():
    """Download temporal cognitive modeling papers"""
    
    # Setup
    base_dir = Path('/Users/invoture/dev.local/hdm')
    papers_dir = base_dir / 'papers'
    csv_file = base_dir / 'temporal_cognitive_automatic_papers.csv'
    
    # Create papers directory if it doesn't exist
    papers_dir.mkdir(exist_ok=True)
    
    # Statistics
    stats = {
        'total': 0,
        'already_exists': 0,
        'success': 0,
        'failed': 0,
        'skipped': 0
    }
    
    failed_downloads = []
    
    print("=== Temporal-Cognitive Modeling Papers - Automatic Download ===")
    print(f"Target directory: {papers_dir}")
    print(f"Source file: {csv_file}")
    print()
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, 1):
                title = row.get('Title', '').strip()
                url = row.get('URL', '').strip()
                domain = row.get('Domain_Category', '').strip()
                authors = row.get('Authors', '').strip()
                
                stats['total'] += 1
                
                print(f"[{i:2d}/{stats['total']}] {title[:60]}...")
                print(f"  Authors: {authors[:50]}...")
                print(f"  Domain: {domain}")
                print(f"  URL: {url}")
                
                if not url or url == "Not available":
                    print(f"  ⚠ No URL available")
                    stats['skipped'] += 1
                    continue
                
                # Get PDF URL
                pdf_url = get_pdf_url(url, domain)
                if not pdf_url:
                    print(f"  ⚠ Could not determine PDF URL")
                    stats['skipped'] += 1
                    continue
                
                # Generate filename
                filename = sanitize_filename(title, url)
                
                # Download
                success, reason = download_pdf(pdf_url, filename, papers_dir)
                
                if success:
                    if reason == "already_exists":
                        stats['already_exists'] += 1
                    else:
                        stats['success'] += 1
                else:
                    stats['failed'] += 1
                    failed_downloads.append({
                        'title': title,
                        'url': url,
                        'pdf_url': pdf_url,
                        'reason': reason,
                        'domain': domain
                    })
                
                # Be respectful with requests
                time.sleep(1)
                
                print()
    
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Print summary
    print("=== TEMPORAL-COGNITIVE DOWNLOAD SUMMARY ===")
    print(f"Total papers processed: {stats['total']}")
    print(f"Already existed: {stats['already_exists']}")
    print(f"Successfully downloaded: {stats['success']}")
    print(f"Failed downloads: {stats['failed']}")
    print(f"Skipped (no URL): {stats['skipped']}")
    print()
    
    # Save failed downloads for review
    if failed_downloads:
        failed_file = base_dir / 'failed_temporal_cognitive_downloads.csv'
        with open(failed_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'url', 'pdf_url', 'reason', 'domain']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(failed_downloads)
        
        print(f"Failed downloads saved to: {failed_file}")
    
    # Count temporal cognitive papers
    temporal_files = list(papers_dir.glob('temporal_cognitive_*.pdf'))
    print(f"Total temporal-cognitive papers in directory: {len(temporal_files)}")

if __name__ == "__main__":
    download_temporal_cognitive_papers()