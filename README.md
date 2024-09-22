## Colegios Colombia Scraper

This Python script uses Selenium and Scrapy to scrape data from the website colegioscolombia.com and store it in a MongoDB database and a CSV file.

### Inputs

- **None**: The script takes no explicit input parameters, but relies on hardcoded website URLs and MongoDB connection details within the code.

### Outputs

- **MongoDB database:** The script inserts scraped data into a MongoDB database called `colegios-colombia`.

  - **Collection:** `colegios`

  - **Fields:** 
    - `colegio_id` (hash of the colegio name and city): Unique identifier for each colegio.
    - `nombre`: Name of the colegio.
    - `telefono`: Phone number of the colegio.
    - `departamento`: Department where the colegio is located.
    - `ciudad`: City where the colegio is located.
    - `source`: URL of the page where the data was scraped.

- **CSV file:** The script creates a CSV file called `colegios.csv` containing the following fields: `nombre` and `telefono`.

### Usage

1. **Install Requirements:**
   - Install the required Python libraries listed in the `requirements.txt` file using `pip install -r requirements.txt`.
2. **Set up MongoDB:**
   - Create a MongoDB database named `colegios-colombia` and a collection named `colegios`.
3. **Configure MongoDB Connection:**
   - Replace the placeholder connection string `mongodb+srv://user:password@cluster0.mamup.mongodb.net` with your actual MongoDB connection details.
4. **Run the script:**
   - Execute the `main_colegioscolombia_scraper.py` script to start scraping data.

### Notes

- The script uses headless Chrome for scraping, meaning it runs without a visible browser window.
- You may need to adjust the `scroll_pause_time` variable in the `sel.py` script depending on your internet speed and computer performance.
- The script handles duplicate records by updating existing entries in the MongoDB database.
- The script can be customized to scrape data from different sections of the website or to include more fields from the scraped pages.