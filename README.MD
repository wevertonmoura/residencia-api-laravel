# 🤖 AlphaNews AI | Parceria Jornal do Commercio (JC)
### Sistema de Redação Financeira Autônoma com Multi-Agentes

Este projeto foi desenvolvido como parte de uma iniciativa de inovação tecnológica aplicada ao jornalismo financeiro para o **Jornal do Commercio**. O objetivo é automatizar a análise de dados do mercado de capitais e a redação de artigos especializados, unindo a precisão dos dados à agilidade editorial.

## 🚀 Contexto do Projeto
O sistema simula uma redação digital onde três agentes de Inteligência Artificial colaboram para gerar conteúdos prontos para publicação no portal do JC, mantendo o tom de voz analítico e a credibilidade exigida pelo veículo.

### 🧠 A Equipe Digital
1. **Agente Júlia (Quantitativa):** Coleta dados em tempo real (Yahoo Finance) e calcula indicadores técnicos como o $SMA_{200}$ (Média Móvel de 200 dias).
2. **Agente Pedro (Fundamentalista):** Analisa o sentimento do mercado e o contexto econômico via **Gemini 2.5 Flash**.
3. **Agente Key (Editora-Chefe):** Consolida as informações e redige o artigo final no padrão Bloomberg/Valor Econômico, realizando o deploy automático via API Laravel.

## 🛠️ Stack Tecnológica
- **Backend:** Python (Flask) para a orquestração dos agentes.
- **IA Generativa:** Google Gemini 2.5 Flash API.
- **Painel Administrativo:** HTML5, Tailwind CSS e JavaScript (Dashboard de monitoramento JC).
- **Infraestrutura:** Docker e Docker-Compose para ambiente produtivo.
- **Integração de Dados:** API RESTful conectada ao sistema Laravel.