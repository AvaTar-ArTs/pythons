#!/usr/bin/env python3
"""
Job Search Web Scraper
Searches LinkedIn, company websites, and job boards for AI music/audio positions
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
from typing import List, Dict
import time

class JobSearcher:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.results = []
    
    def search_company_careers(self, company_name: str, careers_url: str) -> List[Dict]:
        """Search a company's career page"""
        print(f"\n?? Searching {company_name}...")
        
        try:
            response = requests.get(careers_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Common job posting selectors
            job_listings = soup.find_all(['div', 'li', 'article'], class_=lambda x: x and any(
                term in str(x).lower() for term in ['job', 'position', 'role', 'opening', 'career']
            ))
            
            jobs = []
            for job in job_listings[:10]:  # Limit to first 10
                title_elem = job.find(['h2', 'h3', 'h4', 'a'])
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    # Filter for relevant roles
                    if any(keyword in title.lower() for keyword in [
                        'engineer', 'ml', 'machine learning', 'data', 'growth', 'software'
                    ]):
                        link = title_elem.get('href', '') if title_elem.name == 'a' else ''
                        if link and not link.startswith('http'):
                            link = f"{careers_url.split('/careers')[0]}{link}"
                        
                        jobs.append({
                            'company': company_name,
                            'title': title,
                            'url': link or careers_url,
                            'source': 'Company Website',
                            'found_date': datetime.now().strftime('%Y-%m-%d')
                        })
            
            print(f"   ? Found {len(jobs)} relevant positions")
            return jobs
            
        except Exception as e:
            print(f"   ? Error: {e}")
            return []
    
    def search_greenhouse(self, company_name: str, greenhouse_url: str) -> List[Dict]:
        """Search Greenhouse job boards (many startups use this)"""
        print(f"\n?? Searching {company_name} on Greenhouse...")
        
        try:
            response = requests.get(greenhouse_url, headers=self.headers, timeout=10)
            data = response.json() if 'json' in response.headers.get('content-type', '') else []
            
            jobs = []
            if isinstance(data, dict) and 'jobs' in data:
                data = data['jobs']
            
            for job in data:
                if isinstance(job, dict):
                    title = job.get('title', '')
                    if any(keyword in title.lower() for keyword in [
                        'engineer', 'ml', 'machine learning', 'data', 'growth', 'software'
                    ]):
                        jobs.append({
                            'company': company_name,
                            'title': title,
                            'url': job.get('absolute_url', greenhouse_url),
                            'location': job.get('location', {}).get('name', 'N/A'),
                            'source': 'Greenhouse',
                            'found_date': datetime.now().strftime('%Y-%m-%d')
                        })
            
            print(f"   ? Found {len(jobs)} relevant positions")
            return jobs
            
        except Exception as e:
            print(f"   ? Error: {e}")
            return []
    
    def search_lever(self, company_name: str, lever_url: str) -> List[Dict]:
        """Search Lever job boards"""
        print(f"\n?? Searching {company_name} on Lever...")
        
        try:
            response = requests.get(lever_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            jobs = []
            postings = soup.find_all('div', class_='posting')
            
            for posting in postings:
                title_elem = posting.find('h5')
                if title_elem:
                    title = title_elem.get_text(strip=True)
                    if any(keyword in title.lower() for keyword in [
                        'engineer', 'ml', 'machine learning', 'data', 'growth', 'software'
                    ]):
                        link_elem = posting.find('a', class_='posting-title')
                        jobs.append({
                            'company': company_name,
                            'title': title,
                            'url': link_elem.get('href', lever_url) if link_elem else lever_url,
                            'source': 'Lever',
                            'found_date': datetime.now().strftime('%Y-%m-%d')
                        })
            
            print(f"   ? Found {len(jobs)} relevant positions")
            return jobs
            
        except Exception as e:
            print(f"   ? Error: {e}")
            return []

    def save_results(self, filename: str = None):
        """Save results to CSV"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'job_search_results_{timestamp}.csv'
        
        if not self.results:
            print("\n??  No results to save")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            if self.results:
                writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                writer.writeheader()
                writer.writerows(self.results)
        
        print(f"\n?? Saved {len(self.results)} jobs to {filename}")
        return filename

def main():
    searcher = JobSearcher()
    
    # AI Music Companies
    companies = [
        {
            'name': 'Suno',
            'url': 'https://jobs.ashbyhq.com/suno',
            'type': 'ashby'
        },
        {
            'name': 'Runway ML',
            'url': 'https://runwayml.com/careers',
            'type': 'careers'
        },
        {
            'name': 'ElevenLabs',
            'url': 'https://elevenlabs.io/careers',
            'type': 'careers'
        },
        {
            'name': 'Stability AI',
            'url': 'https://stability.ai/careers',
            'type': 'careers'
        },
        {
            'name': 'Descript',
            'url': 'https://www.descript.com/careers',
            'type': 'careers'
        },
        {
            'name': 'Splice',
            'url': 'https://splice.com/careers',
            'type': 'careers'
        },
        {
            'name': 'Leonardo.AI',
            'url': 'https://leonardo.ai/careers',
            'type': 'careers'
        },
    ]
    
    print("?? Starting Job Search...")
    print("=" * 60)
    
    for company in companies:
        jobs = searcher.search_company_careers(company['name'], company['url'])
        searcher.results.extend(jobs)
        time.sleep(2)  # Be polite, don't hammer servers
    
    # Save results
    if searcher.results:
        filename = searcher.save_results()
        
        print("\n" + "=" * 60)
        print(f"? Search Complete! Found {len(searcher.results)} total jobs")
        print("=" * 60)
        
        # Show summary
        print("\n?? Summary by Company:")
        company_counts = {}
        for job in searcher.results:
            company_counts[job['company']] = company_counts.get(job['company'], 0) + 1
        
        for company, count in sorted(company_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"   {company}: {count} jobs")
    else:
        print("\n??  No jobs found. Try adjusting search criteria or check URLs.")

if __name__ == '__main__':
    main()
