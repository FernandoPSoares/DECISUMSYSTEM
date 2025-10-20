Backend - DecisumSystem API
Este diretório contém todo o código da API do DecisumSystem.

⚙️ Setup do Ambiente de Desenvolvimento
Pré-requisitos: Python 3.11+ e pip.

Criar o Ambiente Virtual (venv): Se for a primeira vez, execute:

python -m venv venv

Ativar o Ambiente Virtual:

# No Windows PowerShell
.\venv\Scripts\activate

Instalar as Dependências:

pip install -r requirements.txt 

(Nota: Iremos criar um ficheiro requirements.txt para facilitar este passo).

🏛️ Arquitetura do Backend
A API segue um padrão de Arquitetura por Módulos para garantir a escalabilidade e a separação de responsabilidades.

app/core/: Contém a fundação técnica partilhada (ligação à BD, segurança, dependências, CRUDBase).

app/models/: Um pacote Python que serve como o ponto de encontro central para todas as definições de tabelas (modelos SQLAlchemy), organizadas por domínio de negócio.

app/modules/: Onde a lógica de negócio vive. Cada subdiretório é uma "fatia vertical" de uma funcionalidade, contendo:

_router.py (Camada de Apresentação): Expõe os endpoints HTTP, aplica a segurança e chama a camada de serviço.

_service.py (Camada de Lógica de Negócio): Orquestra as operações, aplica as regras de negócio e as validações.

_crud.py (Camada de Acesso a Dados): Interage diretamente com a base de dados, herdando a lógica genérica da CRUDBase.

_schemas.py (Camada de Contrato): Define os "contratos" de dados da API com Pydantic.

🗄️ Gestão da Base de Dados (Alembic)
Usamos o Alembic para gerir as versões do schema da nossa base de dados.

Para gerar uma nova migração (depois de alterar um ficheiro em app/models/):

alembic revision --autogenerate -m "Descrição da alteração"

Para aplicar as migrações e atualizar a base de dados:

alembic upgrade head

API Documentation
A documentação completa da API é gerada automaticamente pelo FastAPI. Com o servidor a correr, aceda a:

http://localhost:8000/docs

Para testar os endpoints protegidos, use o endpoint POST /login/token para obter um token e depois clique no botão "Authorize" para o usar.