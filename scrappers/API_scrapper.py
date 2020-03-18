from flask import Flask, request
import jsonpickle
from constants_scrappers import Constants, TimeRange
import time
from Utils import download_files, load_browser, scrap_web, quit_browser
from Utils import clean_data


app = Flask(__name__)


@app.route('/download_files', methods=['POST'])
def api_download_files():
    if request.method == 'POST':
        data = jsonpickle.decode(request.data)
        try:
            companies = data["companies"]
            download_files(companies, TimeRange.MAX)
            clean_data(companies)
            response = jsonpickle.encode(companies)
        except Exception as error:
            response = str(error)
        return response
    else:
        return 'POST method. Ex: {companies : ["aapl", "amzn", "tsla"]}'


@app.route('/launch_scrapper', methods=['GET', 'POST'])
def launch_scrapper():
    try:
        browser = load_browser()
        while True:  # Don't close the browser
            response = scrap_web(browser)
            # -----------> KAFKA connected with the json_response
            time.sleep(Constants.FREQUENCY_SCRAPPING_MS / 1000)
    except Exception as error:
        response = error
    return response


@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    quit_browser()
    func()
    return 'Server shutting down...'


if __name__ == "__main__":
    app.run(debug=True)




