import requests
from bs4 import BeautifulSoup
import pandas as pd

# Definir a URL e os cabeçalhos para a requisição HTTP
url = 'https://www.worldometers.info/world-population/population-by-country/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Fazer a requisição HTTP
response = requests.get(url, headers=headers)
response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

# Parsear o conteúdo HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Encontrar a tabela pelo ID
table = soup.find('table', id='example2')

# Listas para armazenar os dados
paises = []
populacoes = []
variacoes = []

# Iterar pelas linhas da tabela (excluindo o cabeçalho)
for row in table.find('tbody').find_all('tr'):
    cols = row.find_all('td')
    
    # Extrair o nome do país (segunda coluna, dentro da tag <a>)
    pais = cols[1].find('a').text.strip()
    
    # Extrair a população 2024 (terceira coluna)
    populacao = cols[2].text.strip().replace(',', '')
    
    # Extrair a variação percentual (quarta coluna, removendo o '%')
    variacao = cols[3].text.strip().replace('%', '')
    
    # Adicionar aos dados
    paises.append(pais)
    populacoes.append(int(populacao))
    variacoes.append(float(variacao))

# Criar o DataFrame
df = pd.DataFrame({
    'País': paises,
    'População 2024': populacoes,
    'Variação Populacional (%)': variacoes
})

# Salvar em CSV
df.to_csv('populacao_paises.csv', index=False, encoding='utf-8-sig')

print("Dados salvos com sucesso em 'populacao_paises.csv'!")