# Dashboard e Previsão de Churn

## Análise de Churn 📊🚀

Este projeto foi desenvolvido como uma **pipeline completa de dados**, integrando etapas de **ETL (Extração, Transformação e Carga)** para garantir a qualidade e consistência das informações utilizadas. A análise exploratória e as visualizações interativas foram implementadas utilizando **Dash** e **Plotly**, ferramentas modernas que permitem criar dashboards dinâmicos e intuitivos, facilitando a interpretação dos dados em tempo real. O deploy do dashboard foi realizado utilizando **Heroku**, garantindo acessibilidade e escalabilidade da solução.

Para a modelagem preditiva, foi empregado o algoritmo **Random Forest**, uma técnica robusta de machine learning capaz de identificar padrões complexos nos dados e prever com alta precisão quais clientes têm maior probabilidade de churn. Essa abordagem faz parte de uma pipeline automatizada, onde os dados passam por um fluxo estruturado: desde a coleta e limpeza até a transformação e treinamento do modelo.

O uso dessas tecnologias garante não apenas **insights acionáveis**, mas também **escalabilidade** e **eficiência** no processamento de grandes volumes de dados, tornando o projeto uma solução completa para entender e combater o churn.

---

## 📋 Visão Geral

Você já se perguntou:
- Quais são os principais indicadores que levam os clientes a deixarem um serviço?
- Como os perfis dos clientes se relacionam com as taxas de churn?
- Quais estratégias podem ser implementadas para reduzir a evasão?

Neste projeto, buscamos responder essas perguntas através de:
- **Coleta e tratamento de dados:** Extração e limpeza de dados relevantes para a análise de churn.
- **Análise Exploratória:** Identificação de padrões e correlações que ajudam a entender os motivos da saída de clientes.
- **Modelagem Preditiva:** Desenvolvimento de modelos que auxiliam na previsão do churn, permitindo intervenções estratégicas.

---

## 🚀 Funcionalidades

- **Coleta de Dados:** Integração de diversas fontes para consolidar informações dos clientes.
- **Pré-processamento:** Limpeza e transformação dos dados para garantir a qualidade da análise.
- **Análise Estatística:** Uso de técnicas de visualização e estatísticas descritivas para explorar tendências.
- **Modelagem de Churn:** Implementação de modelos preditivos utilizando técnicas de machine learning.
- **Relatórios e Visualizações:** Criação de gráficos e dashboards que facilitam a compreensão dos insights obtidos.
- **Deploy no Heroku:** Disponibilização do dashboard na nuvem para acesso rápido e eficiente.

---

## 🔧 Tecnologias Utilizadas

- **Python**
- **pandas**
- **NumPy**
- **scikit-learn**
- **matplotlib**
- **seaborn**
- **Jupyter Notebook**
- **Dash**
- **Plotly**
- **SQL Server**
- **PyODBC**
- **Heroku**

---

## 📂 Estrutura do Projeto

```plaintext
├── DADOS/                   # Conjunto de dados e arquivos brutos
├── DOCS E RESULTADOS/       # Notebooks de análise e experimentos, relatórios finais e visualizações
├── MODELO/                  # Scripts de coleta, pré-processamento e modelagem
├── README.md
├── app.py                   # App responsável pelo deploy do dashboard no Heroku
├── requirements.txt         # Lista de requisitos para o Heroku fazer o deploy
