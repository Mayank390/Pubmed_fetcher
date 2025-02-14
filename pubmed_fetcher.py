import requests
import csv
import re
from typing import List, Dict
import xml.etree.ElementTree as ET


BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"


def fetch_papers(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    search_url = f"{BASE_URL}esearch.fcgi?db=pubmed&term={query}&retmode=json&retmax={max_results}"
    response = requests.get(search_url)
    if response.status_code != 200:
        raise Exception("Error fetching data from PubMed API")
    
    paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
    return get_paper_details(paper_ids)


def get_paper_details(paper_ids: List[str]) -> List[Dict[str, str]]:
    if not paper_ids:
        return []
    
    details_url = f"{BASE_URL}esummary.fcgi?db=pubmed&id={','.join(paper_ids)}&retmode=json"
    response = requests.get(details_url)
    if response.status_code != 200:
        raise Exception("Error fetching paper details")
    
    papers = []
    summary_data = response.json().get("result", {})
    for paper_id in paper_ids:
        paper_info = summary_data.get(paper_id, {})
        papers.append({
            "PubmedID": paper_id,
            "Title": paper_info.get("title", "N/A"),
            "Publication Date": paper_info.get("pubdate", "N/A"),
            "Non-academic Author(s)": "", 
            "Company Affiliation(s)": "",  
            "Corresponding Author Email": "N/A"
        })
    return papers


def filter_non_academic_authors(papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    filtered_papers = []
    for paper in papers:
        authors = extract_authors_with_affiliations(paper["PubmedID"])
        non_academic_authors = [(name, aff) for name, aff in authors if is_non_academic(aff)]
        if non_academic_authors:
            paper["Non-academic Author(s)"], paper["Company Affiliation(s)"] = zip(*non_academic_authors)
            filtered_papers.append(paper)
    return filtered_papers


def extract_authors_with_affiliations(pubmed_id: str) -> List[tuple]:
    details_url = f"{BASE_URL}efetch.fcgi?db=pubmed&id={pubmed_id}&retmode=xml"
    response = requests.get(details_url)
    
    if response.status_code != 200:
        return []
    
    root = ET.fromstring(response.text)
    authors = []
    
    for author in root.findall(".//Author"):
        name = author.find("LastName")
        affiliation = author.find(".//Affiliation")
        if name is not None and affiliation is not None:
            authors.append((name.text, affiliation.text))
    
    print(f"PubMed ID: {pubmed_id} - Authors Extracted: {authors}")
    
    return authors

def is_non_academic(affiliation: str) -> bool:
    academic_pattern = re.compile(r"\b(university|college|institute|academy|polytechnic|research\s?lab)\b", re.IGNORECASE)
    return not bool(academic_pattern.search(affiliation))



def save_to_csv(papers: List[Dict[str, str]], filename: str):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)
