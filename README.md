DecisumSystem - ERP Moderno
Bem-vindo ao DecisumSystem, um sistema de gestão integrada (ERP) desenhado para ser escalável, seguro e com uma experiência de utilizador de excelência.

🚀 Visão Geral da Arquitetura
O projeto está dividido em duas aplicações principais:

Backend: Uma API RESTful robusta construída com Python e FastAPI. É responsável por toda a lógica de negócio, interação com a base de dados e segurança.

Frontend: Uma Single-Page Application (SPA) moderna e reativa, construída com React (Vite) e estilizada com Tailwind CSS.

A comunicação entre os dois é feita através de pedidos HTTP, com autenticação gerida por tokens JWT.

⚡ Guia de Início Rápido (Quick Start)
Para executar o projeto completo localmente, você precisará de ter dois terminais abertos.

1. Iniciar o Backend
Abra um terminal e navegue para a pasta backend:

cd backend

Ative o ambiente virtual:

# No Windows PowerShell
.\venv\Scripts\activate

Inicie o servidor da API com Uvicorn:

uvicorn app.main:app --reload

O backend estará a ser executado em http://localhost:8000.

2. Iniciar o Frontend
Abra um segundo terminal e navegue para a pasta frontend:

cd frontend

Instale as dependências (apenas na primeira vez):

npm install

Inicie o servidor de desenvolvimento do Vite:

npm run dev

A aplicação frontend estará acessível no endereço que o terminal indicar (geralmente http://localhost:5173).

🛠️ Stack Tecnológica
Backend: Python 3.11+, FastAPI, SQLAlchemy, Alembic, Uvicorn, Passlib, python-jose.

Frontend: Node.js, Vite, React, Tailwind CSS, Axios, React Router, Headless UI, Framer Motion, react-hot-toast.

Base de Dados: PostgreSQL (a correr num contentor Docker).

📁 Estrutura do Projeto
/DecisumSystem
├── backend/          # Código da API (Python/FastAPI)
├── frontend/         # Código da Interface (React/Vite)
└── docker-compose.yml  # Configuração do contentor da base de dados

Para mais detalhes, consulte os ficheiros README.md dentro de cada uma das pastas backend/ e frontend/.