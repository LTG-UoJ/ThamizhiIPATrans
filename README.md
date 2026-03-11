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
