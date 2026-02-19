# TMDB Dataset - Análise de Filmes

Este projeto é um pipeline completo para extração, transformação e visualização de dados de filmes da TMDB (The Movie Database). Ele coleta informações de filmes populares, enriquece com dados financeiros e de gêneros, e oferece uma interface interativa em Streamlit para análises de negócio, como curadoria (qualidade), demanda (popularidade), mix de gêneros e ROI (retorno sobre investimento).

## Funcionalidades
- **ETL Pipeline**: Extração de dados via API TMDB, transformação com limpeza e enriquecimento, e carregamento em arquivos JSONL.
- **Interface Web**: Aplicação Streamlit com dashboards interativos usando Altair para gráficos.
- **Cache**: Sistema de cache para evitar requisições repetidas à API.
- **Análises**: Insights sobre qualidade de dados, popularidade, gêneros e finanças.

## Tecnologias
- Python 3.8+
- Bibliotecas: pandas, requests, streamlit, altair, python-dotenv

## Instalação
1. Clone ou baixe o repositório.
2. Instale as dependências:
   ```
   pip install pandas requests streamlit altair python-dotenv
   ```
3. Crie um arquivo `.env` na raiz com sua chave da API TMDB:
   ```
   API_KEY=sua_chave_aqui
   ```
   Obtenha a chave gratuita em [TMDB API](https://www.themoviedb.org/settings/api).

## Uso
1. **Executar ETL**: Para atualizar os dados, rode:
   ```
   python refresh.py
   ```
   Isso extrairá, transformará e salvará os dados em `DATA/CURATED/`.

2. **Executar Interface**: Para abrir a aplicação web:
   ```
   streamlit run UI/Main.py
   ```
   Acesse no navegador (geralmente http://localhost:8501). Navegue pelas páginas: Curadoria, Demanda, Gênero Mix e ROI.

## Estrutura de Arquivos
- `refresh.py`: Script principal para ETL.
- `ETL/`: Módulos para extração (`extract.py`), transformação (`transform.py`) e carregamento (`load.py`).
- `UI/`: Interface Streamlit, com `Main.py` e componentes em `components/`, páginas em `pages/`.
- `DATA/`: Dados brutos (`ORIGINAL/RAW/`), cache (`CACHE/`), e curados (`CURATED/`).
- `.env`: Chaves de API (não versionar).

## Notas
- A API TMDB tem limites de requisições; use pausas (`sleep_s`) para evitar bloqueios.
- Dados são salvos em JSONL para eficiência.
- Para desenvolvimento, use um ambiente virtual Python.

## Licença
Este projeto é para fins educacionais. Dados da TMDB sob licença Creative Commons.