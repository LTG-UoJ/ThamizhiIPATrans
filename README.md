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
##Cite (ACL):
Ahrane Mahaganapathy, Sumirtha Karunakaran, Kavitha Navakulan, and Kengatharaiyer Sarveswaran. 2026. Bridging Dialectal Variation: A Phonetic Transcription Tool for Tamil. In Proceedings of the 13th Workshop on NLP for Similar Languages, Varieties and Dialects, pages 234–241, Rabat, Morocco. Association for Computational Linguistics.
