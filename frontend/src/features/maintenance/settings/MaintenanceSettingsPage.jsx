// File: frontend/src/features/maintenance/settings/MaintenanceSettingsPage.jsx

import React, { useMemo } from 'react'; // Importar useMemo
import { Settings, Users, Factory, AlertTriangle, Activity, FileWarning, HelpCircle } from 'lucide-react';

// Componentes UI
import Tabs from '../../../components/ui/Tabs';
import SimpleSettingsTable from './components/SimpleSettingsTable';

// API Centralizada
import * as settingsApi from './settingsApi';

const MaintenanceSettingsPage = () => {

  // --- 1. Sub-Abas de RCA (Análise de Falhas) ---
  const rcaTabContent = useMemo(() => {
    const rcaSubTabs = [
      {
        id: 'symptoms',
        label: <div className="flex items-center gap-2"><Activity className="w-4 h-4" /> Sintomas</div>,
        content: (
          <SimpleSettingsTable
            title="Sintomas de Falha"
            api={{
              list: settingsApi.getFailureSymptoms,
              create: settingsApi.createFailureSymptom,
              update: settingsApi.updateFailureSymptom,
              remove: settingsApi.deleteFailureSymptom
            }}
            columns={[
              { header: 'Código', accessor: 'code', sortable: true },
              { header: 'Descrição', accessor: 'description', sortable: true }
            ]}
            formFields={[
              { name: 'code', label: 'Código (Ex: S01)', required: true },
              { name: 'description', label: 'Descrição', required: true }
            ]}
          />
        )
      },
      {
        id: 'modes',
        label: <div className="flex items-center gap-2"><FileWarning className="w-4 h-4" /> Modos de Falha</div>,
        content: (
          <SimpleSettingsTable
            title="Modos de Falha"
            api={{
              list: settingsApi.getFailureModes,
              create: settingsApi.createFailureMode,
              update: settingsApi.updateFailureMode,
              remove: settingsApi.deleteFailureMode
            }}
            columns={[
              { header: 'Código', accessor: 'code', sortable: true },
              { header: 'Descrição', accessor: 'description', sortable: true }
            ]}
            formFields={[
              { name: 'code', label: 'Código (Ex: M01)', required: true },
              { name: 'description', label: 'Descrição', required: true }
            ]}
          />
        )
      },
      {
        id: 'causes',
        label: <div className="flex items-center gap-2"><HelpCircle className="w-4 h-4" /> Causas Raiz</div>,
        content: (
          <SimpleSettingsTable
            title="Causas de Falha"
            api={{
              list: settingsApi.getFailureCauses,
              create: settingsApi.createFailureCause,
              update: settingsApi.updateFailureCause,
              remove: settingsApi.deleteFailureCause
            }}
            columns={[
              { header: 'Código', accessor: 'code', sortable: true },
              { header: 'Descrição', accessor: 'description', sortable: true }
            ]}
            formFields={[
              { name: 'code', label: 'Código (Ex: C01)', required: true },
              { name: 'description', label: 'Descrição', required: true }
            ]}
          />
        )
      }
    ];

    return (
      <div className="mt-2">
        <div className="mb-4 p-4 bg-blue-50 border border-blue-100 rounded-lg text-sm text-blue-800">
          <p className="font-bold flex items-center gap-2">
            <AlertTriangle className="w-4 h-4" /> Configuração de RCA
          </p>
          <p className="mt-1">Defina aqui os códigos padronizados para relatórios de falhas.</p>
        </div>
        <Tabs tabs={rcaSubTabs} variant="underline" />
      </div>
    );
  }, []); // Array vazio = cria apenas uma vez

  // --- 2. Abas Principais ---
  const mainTabs = useMemo(() => [
    {
      id: 'teams',
      label: <div className="flex items-center gap-2"><Users className="w-4 h-4" /> Equipes</div>,
      content: (
        <SimpleSettingsTable
          title="Equipes de Manutenção"
          api={{
            list: settingsApi.getMaintenanceTeams,
            create: settingsApi.createMaintenanceTeam,
            update: settingsApi.updateMaintenanceTeam,
            remove: settingsApi.deleteMaintenanceTeam
          }}
          columns={[{ header: 'Nome da Equipe', accessor: 'name', sortable: true }]}
          formFields={[{ name: 'name', label: 'Nome da Equipe', required: true }]}
        />
      )
    },
    {
      id: 'manufacturers',
      label: <div className="flex items-center gap-2"><Factory className="w-4 h-4" /> Fabricantes</div>,
      content: (
        <SimpleSettingsTable
          title="Fabricantes de Ativos"
          api={{
            list: settingsApi.getManufacturers,
            create: settingsApi.createManufacturer,
            update: settingsApi.updateManufacturer,
            remove: settingsApi.deleteManufacturer
          }}
          columns={[
            { header: 'Nome', accessor: 'name', sortable: true },
            { header: 'Telefone', accessor: 'contact_phone' }
          ]}
          formFields={[
            { name: 'name', label: 'Nome da Empresa', required: true },
            { name: 'contact_person', label: 'Pessoa de Contato' },
            { name: 'contact_email', label: 'Email', type: 'email' },
            { name: 'contact_phone', label: 'Telefone / Celular', type: 'tel', hint: 'Ex: (11) 98888-7777' } 
          ]}
        />
      )
    },
    {
      id: 'rca',
      label: <div className="flex items-center gap-2"><AlertTriangle className="w-4 h-4" /> Análise de Falhas</div>,
      content: rcaTabContent
    }
  ], [rcaTabContent]);

  return (
    <div className="container mx-auto pb-10">
      <div className="flex items-center gap-3 mb-8">
        <div className="p-3 bg-gray-100 rounded-lg">
          <Settings className="w-6 h-6 text-gray-600" />
        </div>
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Configurações de Manutenção</h1>
          <p className="text-sm text-gray-500">Gerir tabelas auxiliares e preferências.</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden min-h-[500px]">
        <Tabs tabs={mainTabs} />
      </div>
    </div>
  );
};

export default MaintenanceSettingsPage;