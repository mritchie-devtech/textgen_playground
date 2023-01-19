import requests
import os
#import PyPDF2
import PyPDF2

HF_API_KEY = os.environ.get('HF_API_KEY')


API_URL = "https://api-inference.huggingface.co/models/bigscience/bloom"
headers = {"Authorization": f"Bearer {HF_API_KEY}"}

daide_syntax_obj = open('daide_syntax.pdf', 'rb')

daide_reader = PyPDF2.PdfReader(daide_syntax_obj)

daide_syntax = ""

for page_num in range(len(daide_reader.pages)):
	page = daide_reader.pages[page_num]
	daide_syntax += str(page.extract_text())

daide_syntax_obj.close()

#print(daide_syntax)


one_prompt = """'XDO((AUS AMY LON) SUP (ENG AMY VIE) MTO PAR)': I propose that the Austrian army in London supports the English army in Vienna's move to Paris.

This is a list of 10 different ways that you could communicate this proposal to your opponent in the board game Diplomacy.  They vary in terms of their attitude, emotional content, and friendliness:

1. Listen to me, you idiot, I implore the Austrian army in London to join forces with the English army in Vienna's move to Paris. [Aggressive]"""


prompt = """'XDO((AUS AMY LON) SUP (ENG AMY VIE) MTO PAR)': I propose that the Austrian army in London supports the English army in Vienna's move to Paris.

If we translated the DAIDE message above to an angry, WW1-era tone, reminiscent of Winston Churchill, it might look like: 
"""

prompt = daide_syntax + " " + prompt

print(prompt)
print(type(prompt))

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	response.raise_for_status()
	return response.json()
	

query_dict = {"inputs": prompt }

print(query_dict.keys())
output = query( query_dict
	#"inputs": prompt, #"Generate a conversation between Germany and Italy in the board game Diplomacy:  ",
)

print(output)


'''import openai

content_to_classify = "I am a fuzzy little duck going to the "

response = openai.Completion.create(
      model="content-filter-alpha",
      prompt = "<|endoftext|>"+content_to_classify+"\n--\nLabel:",
      temperature=0,
      max_tokens=1,
      top_p=0,
      logprobs=10
    )

print(response)'''
