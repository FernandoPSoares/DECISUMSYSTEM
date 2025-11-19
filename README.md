DecisumSystem

O DecisumSystem é um ERP modular de nova geração focado na gestão industrial, com ênfase em Manutenção (CMMS), Inventário e Produção. O sistema utiliza uma arquitetura moderna baseada em "Fatias Verticais" (Vertical Slices) para garantir escalabilidade e desacoplamento entre módulos.

🛠 Stack Tecnológico

Backend

Linguagem: Python 3.13+

Framework: FastAPI

ORM: SQLAlchemy 2.0+ (Sintaxe Moderna)

Validação: Pydantic V2

Banco de Dados: PostgreSQL

Migrações: Alembic

Frontend

Framework: React 18+

Build Tool: Vite

Estilização: Tailwind CSS

Ícones: Lucide React / Heroicons

HTTP Client: Axios

Infraestrutura

Containerização: Docker & Docker Compose

🚀 Como Iniciar (Quick Start)

Pré-requisitos

Docker Desktop instalado e a correr.

Node.js v18+ (para desenvolvimento local do frontend).

1. Configuração do Ambiente

Clone o repositório e inicie os serviços de infraestrutura (BD e Backend).

git clone [URL_DO_REPO]
cd DecisumSystem

# Iniciar Backend e Banco de Dados
docker compose up --build -d


2. Configuração do Banco de Dados

Na primeira execução, é necessário criar as tabelas e popular os dados iniciais.

# Aguarde uns segundos para o Postgres iniciar, depois execute:
docker compose exec backend alembic upgrade head
docker compose exec backend python seeder.py


3. Iniciar o Frontend

cd frontend
npm install
npm run dev


4. Acessar a Aplicação

Frontend: http://localhost:5173

API Docs (Swagger): http://localhost:8000/docs

API ReDoc: http://localhost:8000/redoc

📂 Estrutura de Módulos

O sistema está dividido em grandes domínios de negócio:

administration: Gestão de Utilizadores, Papéis e Permissões.

inventory: Gestão de Produtos, Stocks, Locais e Movimentações.

maintenance: CMMS completo (Ativos, Ordens de Serviço, Técnicos, Planos Preventivos).

production: Ordens de Produção, Centros de Trabalho e BOMs.

purchasing: Compras e Fornecedores.

🤝 Contribuição

Consulte o ARCHITECTURE.md para entender o padrão de design antes de criar novas funcionalidades.