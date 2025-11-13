Módulo de Manutenção (CMMS) - Arquitetura dos Modelos de Dados (Fase 1)

Este documento descreve a arquitetura de dados (modelos SQLAlchemy) para o módulo de Gestão de Manutenção (CMMS) do DecisumSystem. A Fase 1 foca-se exclusivamente na fundação da base de dados.

1. Visão Geral e Filosofia

O objetivo deste módulo é fornecer uma capacidade de CMMS "nível-líder" (inspirado em Fiix, UpKeep, MaintainX), que seja ao mesmo tempo robusta e perfeitamente integrada com os outros módulos existentes do DecisumSystem (Inventário, Administração, Produção).

A arquitetura dos modelos é dividida em quatro domínios lógicos principais:

Domínio 1: Pessoas e Equipes (O "Quem")

Define quem pode executar o trabalho.

Liga-se ao módulo de Administration (Usuários).

Domínio 2: Ativos e Locais (O "O Quê" e "Onde")

Define o inventário de equipamentos a manter.

Liga-se hierarquicamente e ao módulo de Inventory (Locais e Peças).

Domínio 3: Ordens de Serviço (O "Trabalho")

Define o fluxo de trabalho reativo (manutenção corretiva).

Este é o "coração" operacional do CMMS, unindo os Domínios 1 e 2.

Domínio 4: Manutenção Preventiva (O "Plano")

Define o fluxo de trabalho proativo (planos de manutenção).

Este é o "cérebro" estratégico, que gera automaticamente o "Trabalho" (Domínio 3).

2. Diagrama de Relacionamento Simplificado

Este diagrama mostra as principais "entidades-chave" e como elas se conectam:

 Mód. Admin        DOMÍNIO 1 (Pessoas)
┌───────────┐      ┌───────────────────┐
│  Usuario  │──1:1─►│    Technician     │
└───────────┘      └───────────────────┘
                         │ ▲
                         │ │ 1:N
                         ▼ │
                     ┌───────────────────┐
                     │ MaintenanceTeam   │
                     └───────────────────┘
                            │
                            │ (Atribuído a)
 Mód. Inventário     DOMÍNIO 2 (Ativos)    │           DOMÍNIO 3 (O Trabalho)
┌───────────┐      ┌───────────────────┐   │         ┌───────────────────────┐
│   Local   │──1:N─►│       Asset       │◄──N:1──────┤      WorkOrder      │
└───────────┘      │ (Hierárquico)     │   │         │  (OS Corretiva)       │
                   └───────────────────┘   │         └───────────────────────┘
┌───────────┐      │ ▲     │ ▲           │                       ▲
│  Produto  │      │ │ 1:N │ │ 1:N       │                       │ (Gerada por)
│ (Peça)    │      │ │     │ │           │           DOMÍNIO 4 (O Plano)
└───────────┘      │ │     │ └───────────┼───────────►┌───────────────────────┐
                   │ │     │   (Medidor) │           │        PMPlan       │
                   │ └─────┼──►┌───────────────┐ │           │    (OS Preventiva)    │
                   │  (BOM)│   │  AssetMeter   │◄──────────┼───────────────────────┘
                   │       │   └───────────────┘           │
                   │       │                               │
                   ▼       └───────────────────────────────┘
     ┌──────────────────────┐
     │ AssetSparePart (N:N) │
     └──────────────────────┘


3. Detalhe dos Domínios e Modelos

Domínio 1: Pessoas e Equipes (O "Quem")

Este domínio responde "Quem é o técnico?" e "A que equipa ele pertence?".

MaintenanceTeam (maintenance_team_model.py)

Propósito: Define as equipas de trabalho (ex: "Mecânica", "Elétrica", "Turno A").

Funcionalidade: Agrupa técnicos e serve como um "balde" para atribuir OSs e Planos de PM.

Technician (technician_model.py)

Propósito: Este é o modelo "ponte" crucial.

Funcionalidade: Cria um perfil de "Técnico" que se liga (1:1) a um Usuario (do módulo administration). Isto permite que um utilizador que faz login no sistema seja reconhecido como um técnico, herde as permissões da sua MaintenanceTeam e possa ter OSs atribuídas a si.

Domínio 2: Ativos e Locais (O "O Quê" e "Onde")

Este domínio é o inventário de equipamentos (a "árvore de ativos").

Manufacturer (manufacturer_model.py)

Propósito: Uma tabela de lookup simples para fabricantes (ex: "WEG", "Siemens", "Parker").

Funcionalidade: Usada para catalogar e filtrar Ativos.

Asset (asset_model.py)

Propósito: O coração do CMMS. Representa qualquer item que requeira manutenção (uma máquina, um sub-componente, um edifício).

Funcionalidade:

Hierarquia: Possui um auto-relacionamento (parent_asset_id) para criar uma árvore de ativos (Pai/Filho).

Localização: Liga-se (N:1) ao modelo Local (do módulo inventory), garantindo que a localização de uma máquina é a mesma usada pelo inventário.

Catalogação: Liga-se ao Manufacturer e armazena dados críticos (nº de série, criticidade, datas de garantia).

AssetSparePart (asset_spare_parts_model.py)

Propósito: Define a Lista de Materiais (BOM - Bill of Materials) de um Asset.

Funcionalidade: É uma tabela de associação (N:N) que liga Asset a Produto (do módulo inventory). Responde à pergunta: "Quais peças sobressalentes este equipamento utiliza e em que quantidade?"

AssetMeter / AssetMeterReading (asset_meter_model.py)

Propósito: Rastreia o uso de um Ativo.

Funcionalidade: AssetMeter define o medidor (ex: "Horímetro" ou "Contador de Ciclos"). AssetMeterReading armazena o histórico de leituras (ex: 1500h em 01/11, 1600h em 08/11). É a fundação para a manutenção preditiva/baseada em uso.

AssetFailure... (Modelos) (asset_failure_mode_model.py)

Propósito: Tabelas de lookup para Análise de Causa Raiz (RCA).

Funcionalidade: MaintenanceFailureSymptom (Sintoma - "O que viu?"), MaintenanceFailureMode (Modo - "O que falhou?"), MaintenanceFailureCause (Causa - "Porquê?"). Preenchidas pelo técnico ao fechar uma OS para criar um histórico inteligente de falhas.

Domínio 3: Ordens de Serviço (O "Trabalho")

Este domínio é o fluxo de trabalho reativo e o "documento" central que une tudo.

WorkOrder (work_order_model.py)

Propósito: A Ordem de Serviço (OS) de manutenção.

Funcionalidade: O objeto central. Liga um Asset (o que falhou) a um Technician ou MaintenanceTeam (quem repara). Contém o estado (Aberta, Em Progresso, Concluída), prioridade, tipo (Corretiva) e rastreia o downtime (tempo de paragem).

WorkOrderTask (work_order_task_model.py)

Propósito: O checklist de tarefas dentro da OS.

Funcionalidade: Lista ordenada de passos que o técnico deve executar e marcar como concluídos.

WorkOrderLaborLog (work_order_labor_log_model.py)

Propósito: O "apontamento de horas" (mão de obra).

Funcionalidade: Permite a um Technician registar o tempo (ex: "3.5 horas") gasto numa WorkOrder específica, crucial para o cálculo de custos.

WorkOrderPartUsage (work_order_parts_model.py)

Propósito: O registo de consumo de peças.

Funcionalidade: Regista as peças (VarianteProduto e Lote) que foram consumidas numa OS. A lógica de negócio (na Fase 2) irá usar este modelo para dar baixa do stock no módulo de Inventory.

WorkOrderLog (work_order_log_model.py)

Propósito: O histórico/comentários da OS.

Funcionalidade: Regista automaticamente mudanças de estado (ex: "Utilizador X mudou estado para CONCLUÍDA") e permite que técnicos adicionem comentários (Tipo: COMMENT).

Domínio 4: Manutenção Preventiva (O "Plano")

Este domínio é o cérebro proativo que gera o "Trabalho" (Domínio 3) automaticamente.

PMPlan (pm_plan_model.py)

Propósito: O Plano de Manutenção Preventiva.

Funcionalidade: Um "molde" que define quando gerar uma OS.

Gatilhos (Triggers): Pode ser CALENDAR (ex: a cada 30 dias) ou METER (ex: a cada 500 horas, lendo do AssetMeter).

Template: Contém os dados (título, prioridade, equipa) para pré-preencher a WorkOrder que será gerada.

PMTask (pm_task_list_model.py)

Propósito: O checklist mestre do Plano de Preventiva.

Funcionalidade: Quando uma WorkOrder é gerada pelo PMPlan, estas tarefas são copiadas para o WorkOrderTask da nova OS.

PMRequiredPart (pm_parts_list_model.py)

Propósito: A Lista de Materiais (BOM) mestre do Plano.

Funcionalidade: Define as peças necessárias para a preventiva. Quando a OS é gerada, estas peças podem ser automaticamente reservadas no inventário ou adicionadas à OS como "planeadas".