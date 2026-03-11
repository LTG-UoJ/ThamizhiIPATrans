import re
from fastapi import FastAPI
from pydantic import BaseModel
import os
import glob

app = FastAPI(title="Thamizhi IPA Transcription API")

def tam2lat(text):
	tameng = {
		'அ': '_a', 'ஆ': '_A', 'இ': '_i', 'ஈ': '_I', 'உ': '_u', 'ஊ': '_U',
		'எ': '_E', 'ஏ': '_e', 'ஐ': '_Y', 'ஒ': '_O', 'ஓ': '_o', 'ஔ': '_W',
		'க': 'k', 'ங': 'G', 'ச': 'c', 'ஜ': 'j', 'ஞ': 'J', 'ட': 'T', 'ண': 'N',
		'த': 't', 'ந': 'n', 'ன': 'V', 'ப': 'p', 'ம': 'm', 'ய': 'y', 'ர': 'r',
		'ற': 'X', 'ல': 'l', 'ள': 'L', 'ழ': 'Z', 'வ': 'v', 'ஶ': 'F', 'ஷ': 'S',
		'ஸ': 's', 'ஹ': 'h', 'ா': 'A', 'ி': 'i', 'ீ': 'I', 'ு': 'u', 'ூ': 'U',
		'ெ': 'E', 'ே': 'e', 'ை': 'Y', 'ொ': 'O', 'ோ': 'o', 'ௌ': 'W', '்': 'F',
		'ஃ': 'K'
	}
	
	for key, value in tameng.items():
		text = text.replace(key, value)
	
	text = re.sub(r'([kGcJTNtnpmyrlvZLXVjSsh])F', r'_\1', text)
	text = re.sub(r'(?<!_)([kGcJTNtnpmyrlvZLXVjSsh])(?![aAiIuUeEoOYW])', r'\1a', text)
	text = re.sub(r'(_[kGcJTNtnpmyrlvZLXVjSsh])(_[aAiIuUeEoOYW])', r'\1_\2', text)
	text = text.replace("_", "").replace("Y", "ai").replace("W", "au")
	
	return text


def ipa(text, dialect):
	text = " " + text + " "
	
	# Move Punctuations
	text = re.sub(r"([\;\,\.\!\?\"\'\"\(\)])", r" \1 ", text)
	
	# Dipthongs
	# text = text.replace("ai", "ay")
	text = text.replace("au", "av")
	
	# Grantha
	text = text.replace("j", "ʤ")
	text = text.replace("h", "ɦ")
	text = text.replace("S", "ʂ")
	text = text.replace("srI", "ʂrI")
	
	# Mey
	
	# Vallinam
	
	# pa
	text = re.sub(r"(?<=[aAiIuUeEoO])p(?=[aAiIuUeEoO])", "β", text)
	# text = re.sub(r"(?<=[yrlvZL])p", "β", text)
	text = re.sub(r"(?<=[GJnVmN])p", "b", text)
	
	# ta
	text = re.sub(r"(?<=[aAiIuUeEoO])t(?=[aAiIuUeEoO])", "ð", text)
	text = re.sub(r"(?<=[nV])t", "d̪", text)
	text = re.sub(r"t", "t̪", text)
	
	# Ra
	text = text.replace("XX", "tːr")
	text = re.sub(r"(?<=V)X", "d̺ʳ", text)
	text = text.replace("X", "R")
	
	# Ta
	text = re.sub(r"(?<=[aAiIuUeEoO])T(?=[aAiIuUeEoO])", "ɽ", text)
	text = re.sub(r"(?<=[N])T", "ɖ", text)
	text = text.replace("T", "ʈ")
	
	# ca
	if dialect == 'Jaffna Sri Lankan':
		text = re.sub(r"(?<=[aAiIuUeEoOl])c(?=[aAiIuUeEoO])", "s", text)
		text = re.sub(r"(?<=[J])c", "ɟʝ", text)
		text = re.sub(r"(\s)c", r"\1s", text)
		text = re.sub(r"(V)c", r"\1s", text)
		text = text.replace("c", "cç")
	
	
	elif dialect == 'Indian':
		text = re.sub(r"(?<=[aAiIuUeEoOl])c(?=[aAiIuUeEoO])", "s", text)
		text = re.sub(r"(\s)c", r"\1s", text)
		text = re.sub(r"(V)c", r"\1s", text)
		text = re.sub(r"(?<=[J])c", "ʤ", text)
		text = text.replace("c", "ʧ")
	
	# ka
	
	if dialect == 'Jaffna Sri Lankan':
		# Sri Lankan Tamil
		text = re.sub(r"(?<=[aAiIuUeEoO])k(?=[aAiIuUeEoO])", "x", text)  # Intervocalic /k/
		text = re.sub(r"(?<=[NVmnG])k(?=[aAuUeEoO])", "g", text)  # Intervocalic /k/ after nasal sounds
	elif dialect == 'Indian':  # Indian Tamil
		text = re.sub(r"(?<=[aAiIuUeEoO])k(?=[aAiIuUeEoO])", "ɣ", text)  # Intervocalic /k/
		text = re.sub(r"Gk(?=[iI])", "ŋʲgʲ", text)  # Before front vowels
		text = text.replace("Gk", "ŋg")  # General /k/ before a vowel
		text = re.sub(r"(?<=[aAiIuUeEoO])k(?=[iI])", "ç", text)  # Before front vowels
		text = re.sub(r"(?<=r)k(?=[aAuUeEoO])", "ɣ", text)  # After /r/
		text = re.sub(r"(?<=[aAiIuUeEoO])k(?=[aAiIuUeEoO])", "ɣ", text)  # General /k/
		text = re.sub(r"(?<=[ylvZL])k(?=[aAuUeEoO])", "x", text)  # After semi-vowels
		text = re.sub(r"ykk", "jcc", text)  # Geminate k after semi-vowel
		text = re.sub(r"jkk", "jcc", text)  # Geminate k after /j/
		text = re.sub(r"(?<=[rylvZLGVNaAiIuUeEoO])k(?=[iI])", "gʲ", text)  # Before front vowels
		text = re.sub(r"(?<=[NVmn])k(?=[aAuUeEoO])", "g", text)  # Intervocalic /k/ after nasal sounds
		text = re.sub(r"(?<=k)k(?=[iI])", "kʲ", text)  # Geminate k before front vowels
	
	# Idaiyinam
	text = text.replace("Z", "ɻ")
	text = re.sub(r"(?<=[aAiIuUeEoO])L(?=[aAiIuUeEoO])", "ɭʼ", text)
	text = text.replace("L", "ɭ")
	text = re.sub(r"(?<=[aAiIuUeEoO])[rr](?=[aAiIuUeEoO])", "ɾ", text)
	text = re.sub(r"r(?!=[aAiIuUeEoO])", "r", text)
	text = re.sub(r"(?<=[aAiIuUeEoO])v(?=[aAiIuUeEoO])", "ʋ", text)
	text = re.sub(r"(\s)v(?=[aAiIuUeEoO])", r"\1ʋ", text)
	text = text.replace("vv", "ʊ̯ʋ")
	text = text.replace("v", "ʋ")
	text = text.replace("yy", "jɪ̯")
	
	# Mellinam
	text = text.replace("n̺d̪", "n̪d̪")
	text = re.sub(r"(?<=[aAiIuUeEoO])N(?=[aAiIuUeEoO])", "ɳʼ", text)
	text = text.replace("N", "ɳ")
	text = text.replace("J", "ɲ")
	text = text.replace("n", "n̺")
	text = text.replace("V", "n")
	text = re.sub(r"GG(?=[iI])", "ŋʲŋʲ", text)
	text = text.replace("GG", "ŋŋ")
	text = text.replace("G", "ŋ")
	
	# Uyir
	
	# Separate Pure Vowel Combinations
	text = re.sub(r"([aAiIuUeEoO])([aAiIuUeEoO])", r"\1_\2", text)
	
	# # # Long O
	if dialect == 'Jaffna Sri Lankan':
		text = re.sub(r"o(\s)", r"ō", text)
		text = re.sub(r"(\s)o(?!·)", r"ō", text)
		text = re.sub(r"_o(?!·)", r"ō", text)
		text = re.sub(r"(?<![aAiIuUeEoOː·])o(?![ː·])", r"ō", text)
	# Long O
	else:
		text = re.sub(r"o(\s)", r"o·\1", text)  # 5.2.5.2 v
		
		text = re.sub(r"(\s)o(?!·)", r"\1ʷoː", text)  # 5.2.5.2 iii
		text = re.sub(r"_o(?!·)", r"ʷoː", text)  # 5.2.5.2 iii - puththi_Ottum
		
		text = re.sub(r"(?<![aAiIuUeEoOː·])o(?![ː·])", r"oː", text)  # 5.2.5.2 i
		
		# #
		# # # Short o
		if dialect == 'Jaffna Sri Lankan':
			text = re.sub(r"(\s)O(?!·)", r"o", text)
			text = re.sub(r"_O(?!·)", r"o", text)
			text = re.sub(r"(?<![aAiIuUeEoOː·̞])O(?![ː·])", r"o̞", text)
		# Short O
		else:
			text = re.sub(r"(\s)O(?!·)", r"\1ʷo̞", text)  # 5.2.5.1 iii
			text = re.sub(r"_O(?!·)", r"ʷo̞", text)  # 5.2.5.1 iii - puththi_Ottum
			
			text = re.sub(r"(?<![aAiIuUeEoOː·̞])O(?![ː·])", r"o̞", text)  # 5.2.5.1 i
	
	# Adding extra symbol for Retroflex Consonants
	retroflex = ["ɽ", "ɖ", "ʈ", "ɳ", "ɭ", "ɻ"]
	for rf in retroflex:
		text = re.sub(r"̞(?=" + re.escape(rf) + ")", r"̞˞", text)
	# Grantha
	text = re.sub(r"v(?![ː])", r"ʋ", text)
	
	text = text.replace("FF", "ʃ")
	
	# N
	text = re.sub(r"N(?![ː])", r"n", text)
	text = re.sub(r"N(?!·)", r"nː", text)
	
	# Post It
	text = re.sub(r"t̺(?!ʳ)", r"t̺ʳ", text)
	
	text = text.replace("a_i", "ai")
	
	if dialect == 'Jaffna Sri Lankan':
		text = re.sub(r"a(?=ʧ|y|l|n|r|ɾ)(?<!n̺)", "ɛ", text)
		
		text = re.sub(r'i(?=ɭʼ|ɻ|ɳ|ɾ)', 'ɨ', text)
		text = re.sub(r'I(?= R|ɭʼ|ɳ|ɾ|ɽ)', 'ɨ:', text)
		text = re.sub(r"(?<=k|p|ʋ|ɽ|b|β)u", "ɨ", text)
		text = re.sub(r'E(?=k|ɭ|ɳ|p|m|ʈ)', 'ɘ', text)
		text = re.sub(r'e(?=ɭ|ɳ|ʈ)', 'ɘ:', text)
	
	text = text.replace('A', 'ā').replace('I', 'ī').replace('U', 'ū')
	text = text.replace('e', 'ē').replace('O', 'o')
	text = text.replace('E', 'e')
	
	return text.strip()


def process_files(input_folder, output_folder, dialect='Jaffna Sri Lankan'):
	# Ensure output directory exists
	os.makedirs(output_folder, exist_ok=True)
	
	# Get all text files from the input folder
	for file_path in glob.glob(os.path.join(input_folder, '*.txt')):
		with open(file_path, 'r', encoding='utf-8') as f:
			text = f.read()
		
		# Convert Tamil to Latin
		latin_transcription = tam2lat(text)
		# Get IPA transcription
		ipa_transcription = ipa(latin_transcription, dialect)
		
		# Get the filename without extension for output
		filename = os.path.basename(file_path)
		output_file_path = os.path.join(output_folder, filename)
		
		# Save the IPA transcription to the output folder
		with open(output_file_path, 'w', encoding='utf-8') as f:
			f.write(ipa_transcription)


# ---------------------------
# Request Model
# ---------------------------
class TextRequest(BaseModel):
    text: str
    dialect: str = "Jaffna Sri Lankan"


# ---------------------------
# API Endpoints
# ---------------------------
@app.get("/")
def root():
    return {"message": "Thamizhi IPA Transcription API is running"}


@app.post("/convert")
def convert_text(request: TextRequest):
    latin = tam2lat(request.text)
    ipa_text = ipa(latin, request.dialect)

    return {
        "original_text": request.text,
        "ipa_transcription": ipa_text,
        "dialect": request.dialect
    }
