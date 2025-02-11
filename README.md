# Vue.js + Python Microservices Project

Este é um projeto fullstack utilizando Vue.js com Tailwind CSS no frontend e Python (FastAPI) para microsserviços no backend.

## Estrutura do Projeto

```
vue-python-microservices/
├── frontend/           # Aplicação Vue.js + Tailwind CSS
├── backend/           # Microsserviços em Python com FastAPI
└── docker-compose.yml # Configuração dos containers Docker
```

## Requisitos

- Docker
- Docker Compose

## Como Iniciar com Docker

1. Clone o repositório
2. Na raiz do projeto, execute:
```bash
docker-compose up --build
```

Isso iniciará:
- Frontend: http://localhost:80
- Serviço de Autenticação: http://localhost:8000
- Serviço de Usuários: http://localhost:8001
- Banco de Dados PostgreSQL: localhost:5432

## Desenvolvimento Local (sem Docker)

### Frontend
- Node.js >= 16
- Vue.js 3
- Tailwind CSS
- Vite

```bash
cd frontend
npm install
npm run dev
```

### Backend
- Python >= 3.8
- FastAPI
- Uvicorn
- SQLAlchemy

```bash
cd backend
python -m venv venv
source venv/bin/activate  # No Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Arquitetura

O projeto segue uma arquitetura de microsserviços:

- **Frontend**: Vue.js + Tailwind CSS
- **Auth Service**: Gerenciamento de autenticação e autorização
- **User Service**: Gerenciamento de usuários
- **Database**: PostgreSQL

### Containers Docker

- **frontend**: Servidor Nginx servindo a aplicação Vue.js
- **auth-service**: Serviço de autenticação em FastAPI
- **user-service**: Serviço de usuários em FastAPI
- **db**: Banco de dados PostgreSQL

## Desenvolvimento

Para desenvolvimento, você pode:

1. Executar todos os serviços:
```bash
docker-compose up
```

2. Reconstruir um serviço específico:
```bash
docker-compose up --build <service-name>
```

3. Visualizar logs:
```bash
docker-compose logs -f <service-name>
