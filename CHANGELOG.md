Changelog

Todas as alterações notáveis neste projeto serão documentadas neste ficheiro.

O formato baseia-se em Keep a Changelog,
e este projeto adere ao Semantic Versioning.

[Unreleased] - Trabalho Recente

🚀 Novas Funcionalidades (Features)

Maintenance Settings:

Adicionada página centralizada de configurações (MaintenanceSettingsPage) com gestão por abas.

Implementado componente genérico SimpleSettingsTable para CRUDs rápidos de tabelas auxiliares.

Criada gestão completa de Análise de Falhas (RCA): Sintomas, Modos de Falha e Causas Raiz.

Criada gestão de Equipas de Manutenção e Fabricantes.

Asset Hub (Detalhes do Ativo):

Nova página de "Visão 360º" do Ativo (AssetDetailPage).

Aba de Estrutura/Hierarquia: Visualização em árvore de Ativos Pai e Componentes Filhos.

Aba de Histórico: Listagem de todas as Ordens de Serviço associadas ao ativo.

Aba de Visão Geral: KPIs rápidos, dados de garantia e localização.

UI/UX:

Implementação do SearchableSelect avançado usando react-select.

Suporte a Portais no Select para corrigir problemas de Z-Index em Modais.

Máscara automática de telefone (Fixo/Celular) nos formulários de configuração.

🐛 Correções de Bugs (Fixes)

API Routing:

Corrigida a duplicação de prefixos nas rotas de manutenção (ex: /maintenance/maintenance/teams -> /maintenance/teams).

Normalização de URLs no frontend para incluir a barra final (/) e evitar redirecionamentos 307.

Schemas:

Removido campo inexistente website do schema de criação de Fabricantes.

Sanitização de inputs no frontend: Strings vazias ("") agora são enviadas como null para passar na validação Pydantic.

Frontend Logic:

Corrigido o conflito entre o modo "Client-Side" do AssetForm e o modo "Server-Side" do SearchModal.

🏗 Refatoração (Refactor)

Backend Structure:

Criação da fatia failure_analysis no backend para agrupar a lógica de RCA.

Centralização das rotas no maintenance/router.py.

Frontend Components:

Atualização do componente Tabs.jsx para suportar conteúdo dinâmico via prop content.

Refatoração do AssetForm.jsx para usar adaptadores de dados compatíveis com react-select.

[0.2.0] - Módulo de Manutenção (Base)

Adicionado

Entidades Core:

Modelagem completa de banco de dados para Asset, WorkOrder, Technician.

Relacionamentos complexos (Many-to-Many) para falhas e peças.

Gestão de Ativos:

CRUD básico de ativos.

Upload de imagem (placeholder).

Associação com Localização (Módulo de Inventário).

Ordens de Serviço:

Fluxo básico de criação de OS.

Numeração sequencial automática (OS-2025-XXXX).

Estados da OS (Rascunho, Aberta, Em Andamento, Concluída).

[0.1.0] - Fundação do Sistema (Legacy)

Adicionado

Core:

Configuração do FastAPI e SQLAlchemy 2.0.

Sistema de Autenticação (OAuth2 com JWT).

Gestão de Utilizadores e Permissões (RBAC).

Infraestrutura:

Docker e Docker Compose para ambiente de desenvolvimento.

Alembic para migrações de banco de dados.

Frontend Base:

Configuração do Vite + React.

Layouts de Administração e Dashboard.

Configuração do Axios (apiClient.js) com intercetores de token.

Módulo de Inventário:

Gestão de Produtos e Categorias.

Gestão de Locais e Armazéns.