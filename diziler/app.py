import requests
from bs4 import BeautifulSoup
import json
from flask import Flask, request,send_file, jsonify

app = Flask(__name__)


@app.route('/seriees_day',methods=['GET'])
def series_day():
    days = ["pazartesi", "sali", "carsamba", "persembe", "cuma", "cumartesi", "pazar"]
    all_shows = []
    try:
        for day in days:
            url = f"https://1001dizi.net/{day}-gunu-dizileri"
            response = requests.get(url)

            if response.status_code != 200:
                return jsonify({"error": f"Veriler alınamadı {day}. Status code: {response.status_code}"}), 500


            soup = BeautifulSoup(response.content, "html.parser")
            titles = soup.find_all("ul", class_="featured_nav")
            
            for ul in titles:
                for li in ul.find_all("li"):
                    show_title = li.get_text(separator=" ").strip()
                    show_data = {
                        "title": show_title,
                        "day": day.capitalize()
                    }
                    all_shows.append(show_data)  
        return jsonify(all_shows)
    except Exception as e:
        return jsonify({"error": f"Bir Hata oluştu: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)