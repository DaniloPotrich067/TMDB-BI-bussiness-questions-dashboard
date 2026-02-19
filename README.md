# TMDB Dataset - Análise de Filmes

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Um pipeline completo e interativo para análise de dados de filmes da TMDB (The Movie Database). Extraia, transforme e visualize insights de negócio sobre qualidade, demanda, gêneros e ROI de filmes populares. Perfeito para entusiastas de cinema, analistas de dados e estudantes de BI.

## ✨ Funcionalidades
- **🔄 ETL Pipeline Robusto**: Extração inteligente via API TMDB com cache, transformação com enriquecimento de dados e carregamento em JSONL eficiente.
- **📊 Dashboards Interativos**: Interface web em Streamlit com gráficos Altair para exploração visual de dados.
- **💾 Cache Inteligente**: Evita requisições repetidas, economizando tempo e respeitando limites da API.
- **🎯 Análises Avançadas**: Curadoria (qualidade), demanda (popularidade), mix de gêneros e ROI financeiro.
- **🛡️ Seguro**: Usa variáveis de ambiente para chaves de API, sem exposição de dados sensíveis.

## 🛠️ Tecnologias
- **Python 3.8+**
- **Bibliotecas Principais**: pandas, requests, streamlit, altair, python-dotenv
- **APIs**: TMDB API (gratuita)
- **Formato de Dados**: JSONL para eficiência

## 🚀 Instalação Rápida
1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/tmdb-dataset.git
   cd tmdb-dataset
   ```

2. **Instale as dependências**:
   ```bash
   pip install pandas requests streamlit altair python-dotenv
   ```

3. **Configure a API**:
   - Crie um arquivo `.env` na raiz:
     ```
     API_KEY=sua_chave_tmdb_aqui
     ```
   - Obtenha sua chave gratuita em [TMDB API Settings](https://www.themoviedb.org/settings/api).

## 📖 Uso
### Atualizar Dados (ETL)
```bash
python refresh.py
```
Isso coleta os top filmes, enriquece com gêneros/finanças e salva em `DATA/CURATED/`.

### Executar a Aplicação
```bash
streamlit run UI/Main.py
```
Abra http://localhost:8501 no navegador. Explore as páginas:
- **🏆 Curadoria**: Rankings por qualidade e distribuições.
- **📈 Demanda**: Análise de popularidade vs. qualidade.
- **🎭 Gênero Mix**: Trade-off entre volume e qualidade por gênero.
- **💰 ROI**: Retorno financeiro e cobertura de dados.

## 📁 Estrutura do Projeto
```
TMDB - Dataset/
├── refresh.py                 # Script principal ETL
├── ETL/                       # Pipeline de dados
│   ├── extract.py            # Extração de dados TMDB
│   ├── transform.py          # Limpeza e enriquecimento
│   └── load.py               # Carregamento (futuro)
├── UI/                        # Interface Streamlit
│   ├── Main.py               # Página principal
│   ├── components/           # Componentes reutilizáveis
│   └── pages/                # Páginas específicas
├── DATA/                      # Dados
│   ├── ORIGINAL/RAW/         # Dados brutos
│   ├── CURATED/              # Dados processados
│   └── CACHE/                # Cache de requisições
├── .env                       # Chaves de API (não versionar)
├── .gitignore                # Arquivos ignorados
└── README.md                 # Este arquivo
```

## 📸 Screenshots
*(Adicione screenshots da interface aqui para visualização)*

## 🤝 Contribuição
Contribuições são bem-vindas! Siga estes passos:
1. Fork o projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`).
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`).
4. Push para a branch (`git push origin feature/nova-funcionalidade`).
5. Abra um Pull Request.

## 📝 Notas Técnicas
- **Limites da API**: TMDB permite ~40 requisições/minuto. Use `sleep_s` em `refresh.py` para pausas.
- **Dados**: Arquivos JSONL são leves e fáceis de processar com pandas.
- **Ambiente**: Recomendamos virtualenv para isolamento.
- **Cache**: Dados em `DATA/CACHE/` são temporários e ignorados pelo Git.

## 📄 Licença
Este projeto está sob a licença MIT. Dados da TMDB são distribuídos sob Creative Commons. Veja [LICENSE](LICENSE) para detalhes.

---

Feito com ❤️ para amantes de cinema e dados. Se gostou, dê uma ⭐ no repositório!

## Licença
Este projeto é para fins educacionais. Dados da TMDB sob licença Creative Commons.