from bardapi import Bard
import os
import pandas as pd
import requests
import json
import re

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

# aqui vamos abrir o arquivo csv
df = pd.read_csv('SDW2023.csv')
user_ids = df['UserID'].tolist()
print(user_ids)





# Função para consultar o banco de dados
def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2, ensure_ascii=False))
                                          #|
                                          #|-> (ensure_ascii=False) estou indicando para a biblioteca json não escapar caracteres não-ASCII



"""
Nessa etapa eu vou utilizar o Google bard por fins didáticos...
A maioria das API's precisam cadastrar o cartão de crédito ou pagar para ter acesso as mesmas..
vou utilizar um jeito gratuito de acessar o google bard, para mais explicações de como fazer essa autenticação vou estar 
deixando o link aqui: https://github.com/dsdanielpark/Bard-API

Esse token de segurança estará inválido na hora da publicação por questão de segurança mas só seguir os passos do 
repositório que dará tudo certo...

unico problema é que esse token tem um tempo limitado
"""
# Area de acesso ao bard para

os.environ['_BARD_API_KEY'] = 'aAjtX1oz0Z3g6mW_2orgDW90V9GMjciSzU5zpHKom8D6xPqvNcpbxm6oKpYgP2yxHbLUlw.'

def gen_ia_news(user):
  input_text = f"Você é um especialista em marketing Bancário. Gere para {user['name']} um email sobre a importancia dos investimentos com no max(100 caracteres)"

  return Bard().get_answer(input_text)['content']

for user in users:
  news = gen_ia_news(user)
  news_format = re.sub(f'{news[0:2]}.*?:', "", news, flags=re.DOTALL)
  news_format = re.sub(r'\n', "", news_format, flags=re.DOTALL)
  print(news)
  print(news_format)
  user['news'].append({
    "description":news_format
  })

print(json.dumps(users, indent=2, ensure_ascii=False))

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")










