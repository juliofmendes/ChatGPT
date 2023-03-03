import requests
from requests.structures import CaseInsensitiveDict
import json
from PIL import Image
from io import BytesIO
import openai

# Configurações da API do OpenAI
openai.api_key = "your_api_key"
model_engine = "text-davinci-002"

# Configurações da API do DALL-E do OpenAI
dalle_api_key = "your_api_key"
dalle_endpoint = "https://api.openai.com/v1/images/generations"

# Obter entrada do usuário para tema ou assunto
prompt = input("Digite um tema ou assunto: ")

# Obter sugestões para comunicação, tom de escrita e público
suggestion_prompt = (
    f"{prompt}\n\nSugira três tipos de comunicação:\n- Educativa\n- Persuasiva\n- Informativa\n\n"
    "Sugira três tons de escrita:\n- Formal\n- Amigável\n- Autoritário\n\n"
    "Sugira três tipos de público:\n- Jovens adultos\n- Profissionais de negócios\n- Pais e mães com filhos pequenos\n"
)
response = openai.Completion.create(engine=model_engine, prompt=suggestion_prompt, max_tokens=256, n=1, stop=None, temperature=0.5)
suggestions = response.choices[0].text.strip().split("\n")

# Permitir que o usuário escolha uma sugestão de cada categoria
communication_suggestions = suggestions[2:5]
writing_tone_suggestions = suggestions[7:10]
audience_suggestions = suggestions[12:15]

print("Escolha uma sugestão de comunicação:")
for i, suggestion in enumerate(communication_suggestions):
    print(f"{i+1}. {suggestion}")
communication_choice = int(input())

print("Escolha uma sugestão de tom de escrita:")
for i, suggestion in enumerate(writing_tone_suggestions):
    print(f"{i+1}. {suggestion}")
writing_tone_choice = int(input())

print("Escolha uma sugestão de público:")
for i, suggestion in enumerate(audience_suggestions):
    print(f"{i+1}. {suggestion}")
audience_choice = int(input())

# Gerar possíveis imagens usando o DALL-E do OpenAI
image_generation_prompt = (
    f"Generate 5 possible images for the prompt: {prompt}\n\n"
    f"{communication_suggestions[communication_choice-1]} sobre {prompt} com um tom {writing_tone_suggestions[writing_tone_choice-1].lower()} "
    f"é perfeito para o público {audience_suggestions[audience_choice-1].lower()}."
)
headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"
headers["Authorization"] = f"Bearer {dalle_api_key}"

data = """
{
    """
data += f'"model": "{model_engine}",'
data += f'"prompt": "{image_generation_prompt}",'
data += """
    "num_images":5,
    "size":"1024x1024",
    "response_format":"url"
}
"""

resp = requests.post(dalle_endpoint, headers=headers, data=data)

# Imprimir as possíveis imagens
response_data = json.loads(resp.text)
image_urls = response_data["data"]

print("Possíveis imagens geradas:")
for i, image_url in enumerate(image_urls):
    print(f"{i+1}. {image_url}")
