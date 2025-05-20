# IBGE Web Scraper

Este projeto realiza o web scraping de dados de todos os estados brasileiros a partir do site oficial do IBGE: [https://cidades.ibge.gov.br/](https://cidades.ibge.gov.br/), utilizando a biblioteca Playwright com Python.

## Descrição

O script coleta informações das seguintes seções:

- População
- Educação
- Trabalho e Rendimento
- Economia
- Território

Os dados são salvos em arquivos `.csv`, organizados por categoria e salvos no diretório `extracted_data`.

OBS.: As seções "Saúde" e "Meio Ambiente" não foram encontradas no site.

## Estrutura

```
/
├── main.py
├── xpaths.py
├── requirements.txt
├── extracted_data/
│ ├── population.csv
│ ├── education.csv
│ ├── work_and_income.csv
│ ├── economy.csv
│ └── territory.csv
```

## Execução

1. Clone este repositório:

```bash
git clone
cd
```

2. Instale as dependências do Python:

```
pip install -r requirements.txt
```

3. Instale os navegadores necessários para o Playwright:

```
playwright install
```

4. Execute o script:

```
python main.py
```
