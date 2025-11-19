Arquitetura do DecisumSystem

Este projeto segue estritamente o padrão de Arquitetura em Fatias Verticais (Vertical Slice Architecture).

Ao contrário da arquitetura em camadas tradicional (onde temos pastas gigantes de Controllers, Services e Models separadas), aqui organizamos o código por Funcionalidade/Entidade.

1. Estrutura do Backend (backend/app/modules/)

Cada entidade do sistema tem a sua própria pasta ("Fatia") contendo tudo o que necessita para funcionar.

Exemplo: Módulo de Manutenção -> Fatia "Assets"
Caminho: backend/app/modules/maintenance/assets/

Ficheiro

Responsabilidade

Padrão

assets_model.py

Definição da Tabela (SQLAlchemy).

Usa Mapped e mapped_column (SQLAlchemy 2.0).

assets_schemas.py

Contratos de Dados (Pydantic).

Define Base, Create, Update e Read.

assets_crud.py

Acesso ao Banco de Dados.

Herda de CRUDBase. Implementa Eager Loading.

assets_service.py

Regras de Negócio.

Validações, orquestração e tratamento de erros HTTP.

assets_router.py

Endpoints da API.

Define as rotas e injeta dependências (db, user).

Regras de Comunicação Inter-Modular

Isolamento: Uma fatia deve ser o mais independente possível.

Dependências: Um Service de uma fatia pode importar o CRUD de outra fatia para validações de leitura (ex: validar se um ID existe).

Exemplo: WorkOrderService importa AssetCRUD para validar asset_id.

Sem Ciclos: Evite importar Service dentro de Service de forma cruzada.

2. Estrutura do Frontend (frontend/src/features/)

O Frontend espelha a estrutura do Backend.

Exemplo: Feature "Maintenance" -> "Assets"
Caminho: frontend/src/features/maintenance/assets/

assetsApi.js: Centraliza todas as chamadas axios para a fatia correspondente no backend.

AssetManagementPage.jsx: Página principal (Listagem). Gere o estado da tabela e modais.

AssetDetailPage.jsx: Página de detalhes ("Hub"). Gere as abas de informação.

components/AssetForm.jsx: Formulário de Criação/Edição.

tabs/*.jsx: Sub-componentes para visualização detalhada.

3. Padrões de Dados

3.1 Soft Delete

A exclusão física de dados (DELETE SQL) é proibida para entidades principais.

Padrão: O campo is_active (bool) é definido como False.

Implementação: O CRUDBase lida com isso no método .remove().

3.2 UUIDs

Todos os IDs primários são UUIDv4 para garantir unicidade global e segurança na enumeração de recursos.