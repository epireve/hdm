#!/usr/bin/env python3
import csv
import os
import requests
import time
import re
from pathlib import Path
from urllib.parse import urlparse
import hashlib

def get_pdf_url(url, domain_category):
    """Convert various URL formats to direct PDF URLs"""
    if not url:
        return None
        
    # arXiv URLs (highest success rate)
    if 'arxiv.org' in url:
        if '/pdf/' in url:
            return url
        elif '/abs/' in url:
            return url.replace('/abs/', '/pdf/') + '.pdf'
        elif '/html/' in url:
            paper_id = re.search(r'(\d+\.\d+)', url)
            if paper_id:
                return f"https://arxiv.org/pdf/{paper_id.group(1)}.pdf"
        elif 'export.arxiv.org' in url and '/pdf/' in url:
            return url
        elif 'ar5iv.labs.arxiv.org' in url:
            paper_id = re.search(r'(\d+\.\d+)', url)
            if paper_id:
                return f"https://arxiv.org/pdf/{paper_id.group(1)}.pdf"
    
    # PMC URLs (good success rate)
    elif 'pmc.ncbi.nlm.nih.gov' in url:
        if '/pdf/' in url:
            return url
        else:
            pmc_match = re.search(r'PMC(\d+)', url)
            if pmc_match:
                return f"https://pmc.ncbi.nlm.nih.gov/articles/PMC{pmc_match.group(1)}/pdf/"
    
    # MDPI URLs (good success rate)
    elif 'mdpi.com' in url and 'mdpi-res.com' not in url:
        if '/pdf' in url:
            return url
        elif url.endswith('/'):
            return url + 'pdf'
        else:
            return url + '/pdf'
    
    # ACL Anthology URLs (good success rate)
    elif 'aclanthology.org' in url:
        if url.endswith('.pdf'):
            return url
        else:
            return url + '.pdf'
    
    # CVF Open Access URLs (good success rate)
    elif 'openaccess.thecvf.com' in url:
        return url
    
    # OpenReview URLs (good success rate)
    elif 'openreview.net' in url:
        if '/pdf' in url:
            return url
        if '?id=' in url:
            paper_id = url.split('?id=')[1]
            return f"https://openreview.net/pdf?id={paper_id}"
    
    # Skip problematic sources for now
    elif any(domain in url for domain in ['researchgate.net', 'semanticscholar.org', 'pubmed.ncbi.nlm.nih.gov']):
        return None
    
    # Try other URLs as-is
    return url

def sanitize_filename(title, url, domain_category):
    """Create a safe filename from paper title and URL"""
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    title = re.sub(r'\s+', '_', title.strip())
    
    if len(title) > 80:
        title = title[:80]
    
    domain_prefix = domain_category.lower().replace(' ', '_').replace('/', '_')
    
    if 'arxiv.org' in url:
        match = re.search(r'(\d+\.\d+)', url)
        if match:
            return f"{domain_prefix}_arxiv_{match.group(1)}_{title}.pdf"
    elif 'pmc.ncbi.nlm.nih.gov' in url:
        match = re.search(r'PMC(\d+)', url)
        if match:
            return f"{domain_prefix}_pmc_{match.group(1)}_{title}.pdf"
    elif 'mdpi.com' in url:
        return f"{domain_prefix}_mdpi_{title}.pdf"
    elif 'aclanthology.org' in url:
        return f"{domain_prefix}_acl_{title}.pdf"
    
    url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
    return f"{domain_prefix}_{url_hash}_{title}.pdf"

def file_already_exists(filename, papers_dir):
    """Check if file already exists with exact or similar name"""
    filepath = papers_dir / filename
    if filepath.exists():
        return True
    
    # Check for similar files (same arXiv ID, PMC ID, etc.)
    if '_arxiv_' in filename:
        arxiv_id = re.search(r'arxiv_(\d+\.\d+)', filename)
        if arxiv_id:
            existing_files = list(papers_dir.glob(f"*arxiv_{arxiv_id.group(1)}*.pdf"))
            if existing_files:
                return True
    
    if '_pmc_' in filename:
        pmc_id = re.search(r'pmc_(\d+)', filename)
        if pmc_id:
            existing_files = list(papers_dir.glob(f"*pmc_{pmc_id.group(1)}*.pdf"))
            if existing_files:
                return True
    
    return False

def download_pdf(url, filename, papers_dir):
    """Download PDF with single attempt"""
    filepath = papers_dir / filename
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/pdf,*/*'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30, allow_redirects=True, stream=True)
        
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            
            # Read first chunk to check PDF magic number
            content_start = b''
            for chunk in response.iter_content(chunk_size=1024):
                content_start = chunk
                break
            
            if 'pdf' in content_type or content_start.startswith(b'%PDF'):
                with open(filepath, 'wb') as f:
                    f.write(content_start)
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                
                file_size = filepath.stat().st_size
                print(f"  ✓ {file_size} bytes")
                return True, "success"
            else:
                return False, f"not_pdf_{content_type}"
        else:
            return False, f"http_{response.status_code}"
            
    except requests.exceptions.RequestException as e:
        return False, f"error_{str(e)[:50]}"

def download_remaining_papers():
    """Download remaining papers from automatic_access_papers.csv efficiently"""
    
    base_dir = Path('/Users/invoture/dev.local/hdm')
    papers_dir = base_dir / 'papers'
    csv_file = base_dir / 'automatic_access_papers.csv'
    
    papers_dir.mkdir(exist_ok=True)
    
    stats = {'processed': 0, 'skipped_exists': 0, 'skipped_no_url': 0, 'success': 0, 'failed': 0}
    failed_downloads = []
    
    print("=== Download Remaining Papers (Efficient Mode) ===")
    print(f"Target: {papers_dir}")
    print(f"Source: {csv_file}")
    print()
    
    # Priority order: arXiv > PMC > MDPI > ACL > OpenReview > Others
    priority_domains = ['arXiv', 'PubMed/PMC', 'MDPI', 'ACL Anthology', 'OpenReview']
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Sort by priority
        def get_priority(row):
            domain = row.get('Domain_Category', '')
            for i, priority_domain in enumerate(priority_domains):
                if priority_domain.lower() in domain.lower():
                    return i
            return len(priority_domains)
        
        rows.sort(key=get_priority)
        
        for i, row in enumerate(rows, 1):
            title = row.get('Title', '').strip()
            url = row.get('URL', '').strip()
            domain = row.get('Domain_Category', '').strip()
            
            stats['processed'] += 1
            
            if not url or url == "Not available":
                stats['skipped_no_url'] += 1
                continue
            
            filename = sanitize_filename(title, url, domain)
            
            if file_already_exists(filename, papers_dir):
                stats['skipped_exists'] += 1
                continue
            
            pdf_url = get_pdf_url(url, domain)
            if not pdf_url:
                stats['skipped_no_url'] += 1
                continue
            
            print(f"[{i:3d}] {domain}: {title[:60]}...")
            success, reason = download_pdf(pdf_url, filename, papers_dir)
            
            if success:
                stats['success'] += 1
            else:
                stats['failed'] += 1
                failed_downloads.append({
                    'title': title[:100],
                    'url': url,
                    'pdf_url': pdf_url,
                    'reason': reason,
                    'domain': domain
                })
            
            time.sleep(0.5)  # Faster processing
            
            # Print progress every 50 papers
            if i % 50 == 0:
                print(f"\n--- Progress: {i}/{len(rows)} papers processed ---")
                print(f"Success: {stats['success']}, Failed: {stats['failed']}, Exists: {stats['skipped_exists']}")
                print()
    
    except Exception as e:
        print(f"Error: {e}")
        return
    
    print("\n=== FINAL SUMMARY ===")
    print(f"Total processed: {stats['processed']}")
    print(f"Already existed: {stats['skipped_exists']}")
    print(f"No URL available: {stats['skipped_no_url']}")
    print(f"Successfully downloaded: {stats['success']}")
    print(f"Failed downloads: {stats['failed']}")
    
    if failed_downloads:
        failed_file = base_dir / 'failed_remaining_downloads.csv'
        with open(failed_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['title', 'url', 'pdf_url', 'reason', 'domain']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(failed_downloads)
        print(f"Failed downloads saved to: {failed_file}")
    
    total_files = list(papers_dir.glob('*.pdf'))
    print(f"Total papers in directory: {len(total_files)}")

if __name__ == "__main__":
    download_remaining_papers()