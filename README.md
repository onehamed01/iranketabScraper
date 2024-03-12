# iranketab scraper

## Introduction
This scraper project utilizes BeautifulSoup (bs4), requests, and Flask to scrape book information from [iranketab.ir](https://iranketab.ir/). The primary purpose is to enable users to extract book details and download associated images. One notable feature is the user-friendly web interface provided by Flask, allowing users to input links or perform searches easily.

## Features
1. Web-based Interaction:
   - Users can add links through the initial web page or after running flaskapp.py.
   - Links can be entered in a textarea, separated by commas.

2. Search Functionality:
   - Users can search for books by entering the book name.
   - The Flask app responds with relevant book suggestions in a dropdown HTML element.

3. Bootstrap Front-end:
   - The project's front-end is designed using Bootstrap, ensuring a responsive and visually appealing user interface.

## Getting Started
1. Clone the repository:
  
   ```git clone https://github.com/onehamed01/iranketabScraper.git```
   
2. Install dependencies:
  
   ```pip install -r requirements.txt```
   
3. Run the Flask app:
  
   ```python flaskapp.py```
   
4. Access the web interface in your browser:
  
   ```http://localhost:5000```
   
## Future Development
This project is version 1.0, and the developer intends to continue its evolution. To keep track of updates and new versions, refer to the [Version History](#version-history) section below.

## Version History
- [Version 1.0](https://github.com/your_username/your_repository/releases/tag/v1.0): Initial release (current version).

Feel free to contribute, report issues, or suggest improvements. Happy scraping!
