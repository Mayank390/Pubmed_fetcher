# PubMed Research Paper Fetcher
#Overview

This project is a Python-based command-line tool that fetches research papers from PubMed based on a user-specified query. It identifies papers with at least one author affiliated with a pharmaceutical or biotech company and saves the results as a CSV file.

#Features

Fetches research papers from PubMed API using eutils

Identifies non-academic authors based on affiliation heuristics

Saves results in a CSV file with key details

Provides a command-line interface (CLI) for flexibility

Implements error handling and logging for robustness

#Installation

This project uses Poetry for dependency management. To install dependencies, run:

poetry install

#Usage

To execute the program, use the following command:

poetry run get-papers-list "your query here" -f output.csv

#Command-line Options

query (required) - Search query for PubMed

-f, --file (optional) - Specify filename to save results (default: prints to console)

-d, --debug (optional) - Enables debug mode for verbose output

#Example

Fetching papers related to "COVID-19 vaccine" and saving the results:

poetry run get-papers-list "COVID-19 vaccine" -f results.csv

#Output Format

The generated CSV file includes the following columns:

PubmedID: Unique identifier for the paper

Title: Title of the paper

Publication Date: Date of publication

Non-academic Author(s): Authors affiliated with companies

Company Affiliation(s): Names of pharmaceutical/biotech companies

Corresponding Author Email: Not available from PubMed API

#API Details

esearch.fcgi - Retrieves paper IDs based on a search query

esummary.fcgi - Fetches paper metadata

efetch.fcgi - Extracts author details and affiliations

#Known Limitations

Corresponding author emails are not directly available from the API.

Some company affiliations might be misclassified due to heuristic filtering.

#License

This project is licensed under the MIT License.
