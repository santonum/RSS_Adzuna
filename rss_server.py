from flask import Flask, Response
import requests
from feedgen.feed import FeedGenerator

app = Flask(__name__)

@app.route("/rss")
def rss_feed():
    # Appel API Adzuna
    app_id = "TON_APP_ID"
    app_key = "TA_CLE_API"
    url = "https://api.adzuna.com/v1/api/jobs/fr/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": "bts electrotechnique",
        "where": "Charente-Maritime",
        "results_per_page": 10
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Generation du flux RSS
    fg = FeedGenerator()
    fg.title("Offres Adzuna – BTS Electrotechnique en Charente-Maritime")
    fg.link(href="https://www.adzuna.fr")
    fg.description("Flux RSS basé sur l'API Adzuna")

    for job in data["results"]:
        fe = fg.add_entry()
        fe.title(job["title"])
        fe.link(href=job["redirect_url"])
        fe.description(job.get("description", "")[:300] + "…")

    rss_xml = fg.rss_str(pretty=True)

    # Retourner la reponse HTTP avec le bon content-type
    return Response(rss_xml, mimetype='application/rss+xml')

if __name__ == "__main__":
    app.run(debug=True)
