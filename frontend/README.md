# Vue Python Microservices Frontend

Interface web moderna desenvolvida com Vue.js 3 e Tailwind CSS para visualização e gestão do Data Warehouse Financeiro.

## 💼 Contexto de Negócio

Esta aplicação serve como interface para o Data Warehouse Financeiro, fornecendo acesso e visualização das informações contábeis e financeiras da empresa. O sistema consolida dados cruciais para a gestão financeira, incluindo:

### Estrutura de Dados

#### Dados Principais
- **Razão (Ledger)**: Registro completo de todas as transações contábeis
  - Mantém o histórico detalhado de cada lançamento contábil
  - Permite rastreabilidade completa das movimentações financeiras

- **Saldos (Balances)**: Balancetes periódicos da empresa
  - Fotografia dos saldos das contas ao final de cada período
  - Permite análise temporal da evolução patrimonial

- **Contas (Accounts)**: Plano de contas contábil
  - Descrição e categorização das contas utilizadas
  - Hierarquia e ordenação das contas
  - Vinculação com grupos de contas

- **Grupos de Contas (Account Groups)**: Estrutura de agregação contábil
  - Agrupamentos para demonstrações financeiras
  - Classificação hierárquica das contas
  - Facilita a geração de relatórios consolidados

### Views e Funções Principais

- **VGL (View General Ledger)**
  - Visualização integrada do razão com grupos de contas
  - Permite análise detalhada das transações por grupo contábil

- **GetBal (Get Balance)**
  - Geração de balancetes com grupos de contas
  - Facilita a análise de saldos por período e grupo contábil

## 🚀 Tecnologias

- [Vue.js 3](https://vuejs.org/) - Framework JavaScript progressivo
- [Tailwind CSS](https://tailwindcss.com/) - Framework CSS utilitário
- [Pinia](https://pinia.vuejs.org/) - Gerenciamento de estado
- [Vue Router](https://router.vuejs.org/) - Roteamento oficial do Vue.js
- [Vite](https://vitejs.dev/) - Build tool e dev server
- [Heroicons](https://heroicons.com/) - Conjunto de ícones SVG
- [Axios](https://axios-http.com/) - Cliente HTTP

## 📁 Estrutura do Projeto

```
frontend/
├── src/
│   ├── assets/        # Recursos estáticos (imagens, estilos)
│   ├── components/    # Componentes reutilizáveis
│   ├── layouts/       # Layouts da aplicação
│   ├── router/        # Configuração de rotas
│   ├── stores/        # Estados globais (Pinia)
│   ├── views/         # Páginas/Views da aplicação
│   ├── App.vue        # Componente raiz
│   └── main.js        # Ponto de entrada da aplicação
├── public/            # Arquivos públicos
└── index.html         # Template HTML principal
```

## 🛠️ Instalação

```bash
# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# Construir para produção
npm run build

# Visualizar build de produção
npm run serve
```

## 🔧 Configuração

O projeto utiliza as seguintes versões principais de dependências:

- Vue.js: 3.3.4
- Vue Router: 4.2.5
- Pinia: 2.1.7
- Tailwind CSS: 3.3.5

## 🌐 Ambiente de Desenvolvimento

O projeto utiliza Vite como ferramenta de build, oferecendo:
- Hot Module Replacement (HMR)
- Otimizações de build
- Ambiente de desenvolvimento rápido

## 📝 Convenções

- Componentes Vue seguem o Style Guide oficial do Vue.js
- CSS utiliza as convenções do Tailwind CSS
- Nomenclatura de arquivos em PascalCase para componentes
- Nomenclatura de arquivos em kebab-case para views

## 🤝 Contribuição

1. Faça o fork do projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE).
