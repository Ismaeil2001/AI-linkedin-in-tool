from transformers import pipeline
import torch

# ✅ Define full keyword list for strong signal detection
KEYWORDS = set([
    # 🎓 Graduate Programs / Nationalization / Early Careers
    "graduate development program", "graduate intake", "early careers onboarding", "nationalization initiative",
    "emirati talent development", "fresh graduate training", "young talent program", "new joiner program",
    "graduate analyst program", "entry-level upskilling",

    # 📚 L&D Strategy, Upskilling & Organizational Learning
    "learning and development strategy", "L&D initiative", "employee learning journey", "corporate training rollout",
    "reskilling programs", "training provider needed", "external training partner", "L&D vendor",
    "launching leadership training", "professional development program",

    # 🧠 Leadership Development & Coaching
    "executive coaching", "first-time manager program", "leadership capability building", "HiPo program",
    "managerial development", "succession planning", "emotional intelligence training",
    "coaching for senior leaders", "personal branding workshop", "impact and influence",

    # 💻 Assessments, Digital Training, and eLearning
    "psychometric assessment", "digital assessment platform", "Gallup strengths", "role play assessments",
    "digital learning strategy", "eLearning provider", "learning experience platform", "online training modules",
    "trackable training outcomes", "training needs assessment"
])

# ✅ Load the HuggingFace NLI model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=0 if torch.cuda.is_available() else -1)
print("Device set to use", "cuda" if torch.cuda.is_available() else "cpu")

def score_post_relevance(post_text):
    matches = [kw for kw in KEYWORDS if kw.lower() in post_text.lower()]
    keyword_match_count = len(matches)

    # 🔎 Use NLI to check intent
    hypotheses = [
        "This post is about launching a new training or development program.",
        "This post is about hiring or internal promotions.",
        "This post is about a request for vendors or external partners."
    ]

    result = classifier(post_text, hypotheses)
    top_score = max(result['scores'])

    # 🎯 AI Relevance Scoring System
    if keyword_match_count >= 3 and top_score >= 0.85:
        relevance_score = 5  # 🔥 Hot Lead
    elif keyword_match_count >= 2 and top_score >= 0.70:
        relevance_score = 4  # ✅ Warm Lead
    elif keyword_match_count >= 1 and top_score >= 0.50:
        relevance_score = 3  # ⚠️ Potential Lead
    elif keyword_match_count >= 1:
        relevance_score = 2  # ❄️ Low Signal
    else:
        relevance_score = 1  # 🚫 Not Relevant

    # ✅ Always return 3 values
    return relevance_score, top_score, matches
