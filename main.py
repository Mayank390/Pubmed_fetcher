import argparse
import logging
from pubmed_fetcher import fetch_papers, filter_non_academic_authors, save_to_csv

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Filename to save results as CSV.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logging.info("Fetching papers...")
    papers = fetch_papers(args.query)
    
    logging.info("Filtering non-academic authors...")
    filtered_papers = filter_non_academic_authors(papers)
    
    if args.file:
        logging.info(f"Saving results to {args.file}")
        save_to_csv(filtered_papers, args.file)
    else:
        for paper in filtered_papers:
            print(paper)

if __name__ == "__main__":
    main()
