# Business News Headlines Web Scraper

A robust web scraping solution that extracts business news headlines from multiple sources and consolidates them into a single file.

## Features

- **Multi-source scraping**: Collects headlines from 4 major business news websites
- **Intelligent fallback system**: Automatically switches between requests and Selenium when needed
- **Anti-blocking measures**: 
  - Random user agent rotation
  - Request throttling
  - Realistic browser headers
- **Data cleaning**: 
  - Whitespace normalization 
  - Duplicate removal
  - Special character stripping
- **Easy integration**: Simple text file input/output system

## Requirements

- Python 3.9
- Conda package manager
- Chrome browser (for Selenium)
- 2GB RAM minimum
- 500MB disk space

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/business-news-scraper.git
   cd business-news-scraper

2. **Set up the Conda environment**:

   Create environment from YAML file:
   conda env create -f requirements.yml

   Activate the environment
   conda activate webscraping  

   Run the python script
   python scraper.py
   