# Colombia Schools Scraper

This project is a Python web scraper that collects information about schools in Colombia from the website colegioscolombia.com. The scraper uses Selenium and BeautifulSoup to extract data such as school names, phone numbers, departments, and cities.

## Features

- School data extraction by department and city
- MongoDB storage
- Duplicate prevention through hashing
- Headless mode for execution without GUI
- Automatic pagination handling

## Requirements

- Python 3.x
- MongoDB (local or Atlas)
- Chrome WebDriver

## Installation

1. Clone the repository:
```bash
git clone https://github.com/cprieto64/colegioscolombia-selenium.git
cd colegioscolombia-selenium
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure MongoDB connection:
   - Edit the `main_colegioscolombia_scraper.py` file
   - Update the MongoDB connection string with your credentials:
   ```python
   client = MongoClient('mongodb+srv://user:password@cluster0.mamup.mongodb.net')
   ```

## Usage

Run the main script:
```bash
python main_colegioscolombia_scraper.py
```

The script:
1. Navigates through Colombian departments
2. Extracts school information by city
3. Stores data in MongoDB
4. Prevents duplicates through ID hashing
5. Includes delays between requests to avoid server overload

## Project Structure

- `main_colegioscolombia_scraper.py`: Main scraping script
- `scrapy_onlyfirstpage.py`: Alternative version using Scrapy
- `requirements.txt`: Project dependencies
- `colegios.csv`: Output file (optional)
- `ubuntu_version/`: Ubuntu-specific version

## Notes

- The scraper includes delays between requests to be respectful to the server
- Data is stored in MongoDB with the following structure:
  - school_id (hash)
  - name
  - phone
  - department
  - city
  - source (origin URL)

## Contributing

Contributions are welcome. Please open an issue or pull request to propose changes.

## License

This project is licensed under the MIT License. 