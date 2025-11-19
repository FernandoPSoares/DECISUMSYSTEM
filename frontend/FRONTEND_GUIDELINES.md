⚙️ Setup do Ambiente de Desenvolvimento
Pré-requisitos: Node.js (versão LTS recomendada) e npm.

Instalar as Dependências: Na primeira vez que configurar o projeto, execute:

npm install

Iniciar o Servidor de Desenvolvimento:

npm run dev

🏛️ Arquitetura do Frontend
A aplicação segue um padrão de "Feature-Sliced Design", organizando o código por funcionalidade de negócio para máxima escalabilidade e manutenibilidade.

src/api/: Contém a instância central do apiClient (Axios) para a comunicação com o backend.

src/components/ui/: A nossa biblioteca de componentes de UI de excelência. São componentes "burros" e reutilizáveis (ex: DataTable, Modal, SearchableSelect).

src/context/: Gestão de estado global. Atualmente, contém o AuthContext para a gestão da autenticação.

src/router/: O "mapa" da nossa aplicação. Contém o AppRouter, que define todas as rotas e a lógica de rotas protegidas.

src/features/: O coração da aplicação. Cada subdiretório é uma "fatia vertical" completa de uma funcionalidade, contendo as suas próprias páginas, componentes especializados, chamadas à API e hooks.

🎨 Estilização
A estilização é feita exclusivamente com Tailwind CSS. Todas as classes de utilidade são aplicadas diretamente no JSX. O ficheiro tailwind.config.js contém a configuração principal, e o src/index.css importa as diretivas base do Tailwind.

📡 Comunicação com a API
Toda a comunicação com o backend é gerida através da instância do apiClient (src/api/apiClient.js). O AuthContext é responsável por intercetar e adicionar automaticamente o token JWT a todos os pedidos, garantindo que as chamadas a endpoints protegidos são autenticadas.