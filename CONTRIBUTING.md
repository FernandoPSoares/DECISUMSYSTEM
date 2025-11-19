Guia de Contribuição

Obrigado pelo interesse em contribuir para o DecisumSystem! Segue estas diretrizes para garantir um processo de desenvolvimento fluido.

Fluxo de Trabalho (Git Flow Simplificado)

Escolha uma Tarefa: Atribua a si mesmo uma Issue ou crie uma nova descrevendo o bug/feature.

Crie uma Branch:

Formato: feature/nome-da-feature ou fix/nome-do-bug.

Exemplo: feature/adicionar-analise-falhas.

Commit Semântico:

Tente seguir o padrão Conventional Commits.

Ex: feat(maintenance): adicionar endpoint de failure modes ou fix(frontend): corrigir z-index do modal.

Pull Request (PR):

Abra o PR para a branch main (ou develop).

Descreva claramente o que foi feito.

Verifique se não introduziu erros de linting.

Padrões de Qualidade

Backend:

Não deixe print() no código; use logging se necessário.

Remova imports não utilizados.

Se alterou modelos, gere a migração do Alembic e inclua-a no commit.

Frontend:

Remova console.log() antes do commit.

Verifique a responsividade em mobile para novas telas.

Reportar Bugs

Abra uma Issue com:

Passos para reproduzir.

Comportamento esperado vs Comportamento real.

Screenshots ou logs de erro.