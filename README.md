# 🔍 AI LinkedIn Post Relevance Notifier

This project is an **AI-driven LinkedIn monitoring tool** that automatically scrapes LinkedIn content based on specific search criteria, classifies each post's relevance using a **zero-shot NLP model**, and sends WhatsApp alerts (via Twilio) for high-priority leads. Relevant posts are also logged into Google Sheets and deduplicated using a persistent local store.

---

## 📌 Features

- ✅ **Daily LinkedIn post scraping** with Selenium and BeautifulSoup  
- 🧠 **AI-based relevance classification** using `facebook/bart-large-mnli`
- 📩 **Automated WhatsApp alerts** for highly relevant leads via Twilio
- 📊 **Google Sheets logging** for historical tracking
- 🔁 **Smart deduplication** using SHA256 hash storage (`seen_posts.json`)
- 🔧 **Debugging output** for scraping and AI inference steps
- ☁️ Designed to run locally or deployable via GitHub Actions / n8n

---

## 🧠 Relevance Classification Logic

Each LinkedIn post is scored based on:
- Keyword matches from L&D, graduate program, and coaching-related terms
- Semantic relevance using **zero-shot NLI** (Natural Language Inference)
- Combined into a score between `1` (irrelevant) and `5` (highly relevant)

Only posts with a score **≥ 3.0** trigger alerts and logging.

---

## 📂 Project Structure

```
AI-LinkedIn-Tool/
├── main.py                      # Entry point script
├── linkedin_scraper.py         # LinkedIn scraping logic
├── relevance_model.py          # AI relevance scoring engine
├── twilio_alert.py             # WhatsApp sending logic
├── google_sheets_logger.py     # Google Sheets integration
├── cookies.json                # Exported session cookies (from LinkedIn)
├── seen_posts.json             # SHA256 hashes of already seen posts
├── .env                        # Local environment variables
├── requirements.txt            # Python dependencies
├── debug_posts/                # (Optional) Saved HTML posts for debugging
└── README.md                   # This file
```

---

## 🚀 How It Works (Step-by-Step)

1. **Startup:**
   - Loads `seen_posts.json` to track duplicates.
   - Loads session cookies from `cookies.json`.

2. **Scraping:**
   - Opens LinkedIn search results (customizable URL).
   - Scrolls through and extracts post containers.

3. **Relevance Filtering:**
   - Each post is scored using `relevance_model.py`.
   - If relevant and not already seen:
     - Sends a WhatsApp message
     - Logs into Google Sheet
     - Saves its hash to `seen_posts.json`

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/ai-linkedin-tool.git
cd ai-linkedin-tool
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
# OR
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add `.env` Configuration

Create a `.env` file with the following:

```env
TWILIO_SID=your_twilio_account_sid
TWILIO_AUTH=your_twilio_auth_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_WHATSAPP_TO=whatsapp:+971501234567
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_CREDENTIALS_FILE=path/to/your/credentials.json
```

---

## ✅ Running the Script

```bash
python main.py
```

---

## ⚙️ Configuration Tips

- To **debug a post**, enable the `debug=True` argument in `scrape_relevant_posts()`
- To **simulate detection**, lower `RELEVANCE_THRESHOLD = 1.0` in `main.py`
- You can **clear `seen_posts.json`** to reprocess all posts during testing

---

## 🧪 Example Output

```
📝 Post 3 | Score: 4.00
Text: EY-Parthenon is hiring graduates for its Riyadh office...

🔎 Lead Profile:
John Smith
https://www.linkedin.com/in/johnsmith

📩 Action: Observe or follow up later

✅ WhatsApp message sent
✅ Logged to Google Sheet
```

---

## ☁️ Deployment Ideas

- Run daily via **GitHub Actions** or **n8n scheduled trigger**
- Integrate with Slack instead of WhatsApp for team use
- Extend to track company page posts or L&D vendors

---

## 📜 License

This project is licensed under MIT. Feel free to reuse or adapt with attribution.

---

## 🙌 Acknowledgements

Built using:
- [HuggingFace Transformers](https://huggingface.co/transformers/)
- [Selenium](https://www.selenium.dev/)
- [Twilio WhatsApp API](https://www.twilio.com/whatsapp)
- [Google Sheets API](https://developers.google.com/sheets/api)
