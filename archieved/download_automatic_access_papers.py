#!/usr/bin/env python3
import csv
import os
import requests
import time
import re
from pathlib import Path
from urllib.parse import urlparse, urljoin
import hashlib

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
        # Handle export.arxiv.org URLs
        elif 'export.arxiv.org' in url and '/pdf/' in url:
            return url
        # Handle ar5iv.labs.arxiv.org URLs
        elif 'ar5iv.labs.arxiv.org' in url:
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
    
    # PubMed URLs
    elif 'pubmed.ncbi.nlm.nih.gov' in url:
        # PubMed typically doesn't have direct PDF access
        return None
    
    # MDPI URLs
    elif 'mdpi.com' in url:
        if '/pdf' in url:
            return url
        elif url.endswith('/'):
            return url + 'pdf'
        else:
            return url + '/pdf'
    
    # Frontiers URLs
    elif 'frontiersin.org' in url:
        if '/pdf' in url:
            return url
        else:
            return url + '/pdf'
    
    # Springer Open URLs
    elif 'springeropen.com' in url or 'journalofcloudcomputing.springeropen.com' in url:
        if '/pdf' in url:
            return url
        # Try adding .pdf extension
        if url.endswith('/'):
            return url[:-1] + '.pdf'
        else:
            return url + '.pdf'
    
    # OpenReview URLs
    elif 'openreview.net' in url:
        if '/pdf' in url:
            return url
        # OpenReview PDFs are typically at /pdf?id=PAPER_ID
        if '?id=' in url:
            paper_id = url.split('?id=')[1]
            return f"https://openreview.net/pdf?id={paper_id}"
    
    # ACL Anthology URLs
    elif 'aclanthology.org' in url:
        if url.endswith('.pdf'):
            return url
        else:
            return url + '.pdf'
    
    # CVF Open Access URLs
    elif 'openaccess.thecvf.com' in url:
        return url  # Already direct PDF links
    
    # ResearchGate URLs (often don't have direct PDF access)
    elif 'researchgate.net' in url:
        return url  # Try as-is, may fail
    
    # Semantic Scholar URLs (metadata only, no direct PDF)
    elif 'semanticscholar.org' in url:
        return None
    
    # HAL Archives URLs
    elif 'hal.science' in url or 'inria.hal.science' in url:
        if '/document' in url:
            return url
        else:
            return url + '/document'
    
    # Zenodo URLs
    elif 'zenodo.org' in url:
        if '/files/' in url:
            return url
        # Try to find PDF in Zenodo record
        return url  # May need special handling
    
    # For other URLs, try as-is
    return url

def sanitize_filename(title, url, domain_category):
    """Create a safe filename from paper title and URL"""
    # Clean the title
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = re.sub(r'\s+', '_', title.strip())
    
    # Limit length
    if len(title) > 100:
        title = title[:100]
    
    # Add domain prefix for organization
    domain_prefix = domain_category.lower().replace(' ', '_').replace('/', '_')
    
    # Try to get a good identifier from URL
    if 'arxiv.org' in url:
        # Extract arXiv ID
        match = re.search(r'(\d+\.\d+)', url)
        if match:
            return f"{domain_prefix}_arxiv_{match.group(1)}_{title}.pdf"
    elif 'pmc.ncbi.nlm.nih.gov' in url:
        # Extract PMC ID
        match = re.search(r'PMC(\d+)', url)
        if match:
            return f"{domain_prefix}_pmc_{match.group(1)}_{title}.pdf"
    elif 'mdpi.com' in url:
        return f"{domain_prefix}_mdpi_{title}.pdf"
    elif 'frontiersin.org' in url:
        return f"{domain_prefix}_frontiers_{title}.pdf"
    
    # Generate a hash for very long or problematic titles
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"{domain_prefix}_{url_hash}_{title}.pdf"

def download_pdf(url, filename, papers_dir, max_retries=3):
    """Download PDF with retries and error handling"""
    filepath = papers_dir / filename
    
    # Skip if file already exists
    if filepath.exists():
        print(f"  ✓ Already exists: {filename}")
        return True, "already_exists"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/pdf,*/*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    for attempt in range(max_retries):
        try:
            print(f"  → Downloading: {filename}")
            response = requests.get(url, headers=headers, timeout=60, allow_redirects=True, stream=True)
            
            if response.status_code == 200:
                # Check if it's actually a PDF
                content_type = response.headers.get('content-type', '').lower()
                
                # Read first chunk to check PDF magic number
                content_start = b''
                for chunk in response.iter_content(chunk_size=1024):
                    content_start = chunk
                    break
                
                if 'pdf' in content_type or content_start.startswith(b'%PDF'):
                    # Download the full content
                    with open(filepath, 'wb') as f:
                        f.write(content_start)  # Write the first chunk
                        for chunk in response.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                    
                    file_size = filepath.stat().st_size
                    print(f"  ✓ Downloaded: {filename} ({file_size} bytes)")
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

def download_automatic_access_papers():
    """Download all papers from automatic_access_papers.csv"""
    
    # Setup
    base_dir = Path('/Users/invoture/dev.local/hdm')
    papers_dir = base_dir / 'papers'
    csv_file = base_dir / 'automatic_access_papers.csv'
    
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
    
    print("=== Automatic Access Papers - Mass Download ===")
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
                source_file = row.get('Source_File', '').strip()
                
                stats['total'] += 1
                
                print(f"[{i:3d}/{stats['total']}] {title[:80]}...")
                print(f"  Authors: {authors[:60]}...")
                print(f"  Domain: {domain}")
                print(f"  Source: {source_file}")
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
                filename = sanitize_filename(title, url, domain)
                
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
                        'authors': authors,
                        'url': url,
                        'pdf_url': pdf_url,
                        'reason': reason,
                        'domain': domain,
                        'source_file': source_file
                    })
                
                # Be respectful with requests
                time.sleep(1.5)
                
                print()
    
    except FileNotFoundError:
        print(f"Error: Could not find {csv_file}")
        return
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Print summary
    print("=== AUTOMATIC ACCESS DOWNLOAD SUMMARY ===")
    print(f"Total papers processed: {stats['total']}")
    print(f"Already existed: {stats['already_exists']}")
    print(f"Successfully downloaded: {stats['success']}")
    print(f"Failed downloads: {stats['failed']}")
    print(f"Skipped (no URL): {stats['skipped']}")
    print()
    
    # Save failed downloads for review
    if failed_downloads:
        failed_file = base_dir / 'failed_automatic_access_downloads.csv'
        with open(failed_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'authors', 'url', 'pdf_url', 'reason', 'domain', 'source_file']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(failed_downloads)
        
        print(f"Failed downloads saved to: {failed_file}")
    
    # Count total papers in directory
    total_files = list(papers_dir.glob('*.pdf'))
    print(f"Total papers in directory: {len(total_files)}")
    
    # Count by source type
    arxiv_files = list(papers_dir.glob('*arxiv*.pdf'))
    pmc_files = list(papers_dir.glob('*pmc*.pdf'))
    mdpi_files = list(papers_dir.glob('*mdpi*.pdf'))
    frontiers_files = list(papers_dir.glob('*frontiers*.pdf'))
    
    print(f"arXiv papers: {len(arxiv_files)}")
    print(f"PMC papers: {len(pmc_files)}")
    print(f"MDPI papers: {len(mdpi_files)}")
    print(f"Frontiers papers: {len(frontiers_files)}")

if __name__ == "__main__":
    download_automatic_access_papers()