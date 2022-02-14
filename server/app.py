from flask import Flask, render_template
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
import time, os

origin_url = 'https://realtimelab.com/local-testing/travel-testing/'
url = Request(origin_url,
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36'})

app = Flask(__name__) 
counter = 0
time_started = time.asctime()

@app.route("/") 
def hello_world():
    return render_template('check.html', started=time_started)


@app.route("/test_available")
def test_avail():
    global counter 
    counter += 1
    if (available()):
        response = {"html": f"""<p class="alert"><a href="{origin_url}" target="_blank">Test avaliable</a> at {time.asctime()}.</p>"""
                , "available": True}
    else:
        response = {"html": f"""<p>Checked {str(counter)} times, no available test at {time.asctime()}.</p>"""
                , "available": False}
    return response




def available():
    try:
        response = urlopen(url).read()
        soup = BeautifulSoup(response, 'html.parser')
        cal_cell = soup.find(attrs={'data-day': 19})
        return cal_cell.has_attr('aria-label')
    except HTTPError as e:
        print('Error code: ', e.code)
    except URLError as e:
        print('Reason: ', e.reason)
        return 

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=True, port=server_port, host='0.0.0.0')