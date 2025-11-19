Diretrizes de Desenvolvimento Frontend (React)

1. Componentes e UI

Bibliotecas Base: Utilize os componentes em src/components/ui/ (DataTable, Modal, SearchableSelect, Tabs) em vez de criar HTML puro. Isso garante consistência visual.

Ícones: Utilize lucide-react como padrão principal. Se necessário, @heroicons/react é o fallback.

2. Gestão de Estado e Hooks

Async/Await: Prefira async/await em useEffect para chamadas de API.

Loading States: Sempre implemente indicadores de carregamento (isLoading) enquanto aguarda dados do backend.

Debounce: Utilize o hook useDebounce para campos de pesquisa em tempo real para evitar sobrecarga na API.

3. Formulários e Inputs

Sanitização: Ao enviar formulários, converta strings vazias "" para null se o campo for opcional no backend. O Pydantic rejeitará "" para campos como datas ou números.

Selects: Utilize o componente SearchableSelect para chaves estrangeiras (FKs).

Modo Client-Side: Carregue a lista no pai e passe via prop options (melhor para listas pequenas < 500 itens).

Modo Server-Side: Configure o loadOptions para buscar paginado (melhor para listas grandes).

4. Estrutura de Pastas

Mantenha o código próximo de onde é usado.

src/features/maintenance/work_orders/
├── components/         # Componentes exclusivos desta feature (Forms, Modais)
├── tabs/              # Sub-paginas de conteúdo (ex: Logs, Peças)
├── WorkOrderListPage.jsx
├── WorkOrderDetailPage.jsx
└── workOrdersApi.js    # Definição dos endpoints desta feature


5. Navegação

Use o hook useNavigate do react-router-dom.

Defina rotas aninhadas no AppRouter.jsx respeitando a hierarquia dos módulos.