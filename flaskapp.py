from flask import Flask, render_template, request, redirect, url_for
from scraper import scrape_content, write_to_excel_file, searching

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        urls = request.form['urls'].split(',')
        data = scrape_content(urls)

        if not isinstance(data, list):
            data = [data]

        if data:
            write_to_excel_file("scraped_data.xlsx", data)
            return redirect(url_for('success'))
        else:
            return 'No data to write to Excel file!'
    return render_template('index.html')

@app.route('/success')
def success():
    return 'Scraping and writing to Excel file successful!'

@app.route('/searching', methods=['GET', 'POST'])
def by_searching():
    if request.method == 'POST':
        search_string = request.form['search_string']
        print(search_string)
        search_data = searching(search_string)
        return render_template('search_result.html', dict_search=search_data)
    return render_template('search_input.html')

@app.route('/scrape_and_save', methods=['POST'])
def scrape_and_save():
    if request.method == 'POST':
        selected_item_urls = request.form.getlist('selected_item') 
        all_scraped_data = []  
        for url in selected_item_urls:
            scraped_data = scrape_content([url])  
            all_scraped_data.extend(scraped_data)  
        if all_scraped_data:
            write_to_excel_file("scraped_data.xlsx", all_scraped_data)  
            return redirect(url_for('success'))
        else:
            return 'No data to write to Excel file!'


if __name__ == '__main__':
    app.run(debug=True)

