# 🎣 Phishing URL Detection

A Flask-based phishing URL detector that extracts **30 URL, HTML and domain features** from a link and classifies it with a **Keras deep learning model** (`model.h5`). URLs are received live over a TCP socket from a second machine, so the system can monitor links from a remote client.

## How It Works

```
Client machine ──(URL over TCP :8080)──► Flask server ──► Feature extraction (30 features) ──► Keras model ──► Phishing probability
```

1. `app.py` opens a TCP socket and waits for a client to send a URL.
2. `feature.py` (`FeatureExtraction`) fetches the page and builds a 30-feature vector.
3. `model/model.h5` predicts the probability that the URL is phishing.
4. The URL and score are printed on the server console.

## Features Extracted

| Category | Examples |
|---|---|
| **URL-based** | IP address in URL, URL length, shortening services, `@` symbol, `//` redirect, `-` in domain, subdomain count, HTTPS, non-standard port |
| **HTML / JavaScript** | Favicon, request URLs, anchor URLs, links in script tags, server form handler, mailto links, right-click disabled, pop-ups, iframes, status-bar tampering |
| **Domain / external** | WHOIS registration length, domain age, DNS record, website traffic, PageRank, Google index, links pointing to page, blacklisted IPs and domains |

## Tech Stack

Python · Flask · TensorFlow/Keras · scikit-learn · NumPy · Pandas · BeautifulSoup · python-whois · SQLite · Bootstrap

## Project Structure

```
├── app.py            # Flask app + TCP socket server + model prediction
├── feature.py        # 30-feature URL extraction
├── model/model.h5    # Trained Keras model
├── templates/        # index.html (sign in / sign up), userlog.html
└── static/           # CSS, JS, images
```

## Getting Started

**1. Clone and install**
```bash
git clone https://github.com/Muskanpandey0304/Main_phishing_url_detection.git
cd Main_phishing_url_detection
pip install flask tensorflow numpy pandas scikit-learn beautifulsoup4 requests python-whois googlesearch-python python-dateutil lxml
```

**2. Set the server IP**

In `app.py`, change `server_address = ('192.168.0.104', 8080)` to your machine's local IP.

**3. Run the server**
```bash
python app.py
```
The server waits for a client connection on port `8080`, then serves the Flask app on `http://127.0.0.1:5000`.

**4. Send a URL from the client machine**
```python
import socket
s = socket.socket()
s.connect(("192.168.0.104", 8080))   # server IP
s.send(b"http://example.com")
```
The URL and its phishing score appear in the server console.

## Notes

- Feature extraction makes live network calls (page fetch, WHOIS, DNS), so it needs internet access and results may vary by site.
- Some external services used for traffic and PageRank features may no longer be available. Those features fall back to default values.
- The 30 features follow the widely used phishing-website feature set (`1` = legitimate, `0` = suspicious, `-1` = phishing).

## Author

**Muskan Pandey** · [@Muskanpandey0304](https://github.com/Muskanpandey0304)
