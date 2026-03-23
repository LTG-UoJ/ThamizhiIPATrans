# ThamizhiIPATrans

**Dialect-aware Tamil Text-to-IPA transcription tool**

## Prerequisites

- Python  
- `pip` package manager  

---

## Installation
```bash
git clone https://github.com/LTG-UoJ/ThamizhiIPATrans.git
cd ThamizhiIPATrans
pip install streamlit
streamlit run IPATrans.py
``````

## 🌐 Running the API 

The API is located in the `API/` folder.

```bash
cd API
uvicorn app:app --reload


Example POST Request
Endpoint: /convert
Content-Type: application/json

{
  "text": "அன்பு",
  "dialect": "Jaffna Sri Lankan"
}
Response Example:
{
    "original_text": "அன்பு",
    "ipa_transcription": "ɛnbɨ",
    "dialect": "Jaffna Sri Lankan"
}
``````
## Cite:
```bash
@inproceedings{mahaganapathy-etal-2026-bridging,
    title = "Bridging Dialectal Variation: A Phonetic Transcription Tool for {T}amil",
    author = "Mahaganapathy, Ahrane  and
      Karunakaran, Sumirtha  and
      Navakulan, Kavitha  and
      Sarveswaran, Kengatharaiyer",
    booktitle = "Proceedings of the 13th Workshop on {NLP} for Similar Languages, Varieties and Dialects",
    month = mar,
    year = "2026",
    address = "Rabat, Morocco",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2026.vardial-1.19/",
    pages = "234--241",
    abstract = "Phonetic transcription is vital for speech processing and linguistic documentation, particularly in languages like Tamil with complex phonology and dialectal variation. Challenges such as consonant gemination, retroflexion, vowel length, and one-to-many grapheme-phoneme mappings are compounded by limited data on Sri Lankan Tamil dialects. We present a dialect-aware, rule-based transcription tool for Tamil that supports Indian and Jaffna Tamil, with extensions underway for other dialects. Using a two-stage pipeline: Tamil script to Latin, then to IPA with context-sensitive rules, the tool handles dialect shifts. A real-time interface enables dialect selection. Evaluated on a 7,830-word corpus, it achieves 94.54{\%} accuracy for Jaffna Tamil and is higher than other tools like eSpeak NG, advancing linguistic preservation and accessible speech technology for Tamil communities."
}
