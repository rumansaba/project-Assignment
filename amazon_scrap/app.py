# Import necessary libraries
from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import time
app = Flask(__name__)
def scrape_phones():
    url = "https://www.amazon.in/s?k=iphone+15+pro+max&crid=35E4QWPJ8ZLQ7&sprefix=i%2Caps%2C662&ref=nb_sb_ss_ts-doa-p_2_1"
    try:

        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        #print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')

        phones_data = []
        phone_elements = soup.find_all("div", class_="puisg-col-inner")  # Update class based on the structure of the website

        for phone in phone_elements:
            title_element = phone.find("span",class_="a-size-medium a-color-base a-text-normal")
            price_element = phone.find("span", class_="a-price-whole")
            review_element = phone.find("span", class_="a-icon-alt")


            # Check if elements exist before accessing their text attributes
            title = title_element.text.strip() if title_element else "N/A"
            price = price_element.text.strip() if price_element else "N/A"
            review = review_element.text.strip() if review_element else "N/A"

            phone_info = {
                'title': title,
                'price': price,
                'review': review
            }
            phones_data.append(phone_info)

        return phones_data
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
        if response.status_code == 503:
            print("Service Unavailable. Retrying after 5 seconds.")
            time.sleep(5)
            return scrape_phones()
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)

    return []


@app.route('/')
def index():
    phones = scrape_phones()
    return render_template('index.html', phones=phones)

if __name__ == '__main__':
    app.run(host="0.0.0.0" ,port=5002)
