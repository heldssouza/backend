# Sistema Financeiro Multitenant

Sistema financeiro empresarial com suporte a múltiplos tenants, implementando os mais altos padrões de segurança e desempenho.

## Arquitetura e Tecnologias

### Backend (Python/FastAPI)
- **FastAPI**: Framework web assíncrono de alta performance
- **SQLAlchemy**: ORM para acesso ao banco de dados
- **Pydantic**: Validação de dados e configurações
- **Redis**: Cache distribuído e gerenciamento de sessão
- **PyJWT**: Autenticação baseada em tokens JWT
- **TOTP**: Autenticação de dois fatores (2FA)

## Componentes Principais

### 1. Sistema Multitenant
- **Isolamento de Dados**: Cada tenant possui seu próprio contexto de dados
- **Middleware de Tenant**: Identificação automática do tenant via header HTTP
- **Validação de Subdomínio**: Cada tenant possui um subdomínio único
- **Banco Master**: Gerencia informações globais e autenticação

#### Importância para Segurança
- Isolamento completo entre tenants
- Prevenção de vazamento de dados entre organizações
- Auditoria independente por tenant

### 2. Autenticação e Autorização

#### Autenticação
- **JWT (JSON Web Tokens)**
  - Tokens de acesso com expiração curta (30 minutos)
  - Tokens de refresh para renovação automática
  - Assinatura criptográfica para prevenir adulteração

- **2FA (Two-Factor Authentication)**
  - Implementação TOTP (Time-based One-Time Password)
  - QR Code para configuração fácil
  - Backup codes para recuperação

#### Autorização
- **RBAC (Role-Based Access Control)**
  - Papéis predefinidos (admin, user, etc.)
  - Permissões granulares por funcionalidade
  - Herança de permissões

#### Importância para Segurança
- Proteção contra acesso não autorizado
- Rastreabilidade de ações por usuário
- Conformidade com normas de segurança (LGPD, SOX)

### 3. Banco de Dados e Migrações

#### Estrutura
- **Tabelas Principais**:
  - `tenants`: Configuração de inquilinos
  - `users`: Usuários do sistema
  - `roles`: Papéis e permissões
  - `user_roles`: Associação usuário-papel
  - `refresh_tokens`: Tokens de renovação
  - `two_factor_auth`: Configuração 2FA
  - `audit_logs`: Registro de auditoria

#### Migrações
- Sistema de migrações separado em:
  - `001_schema.sql`: Estrutura do banco (DDL)
  - `002_seed_data.sql`: Dados iniciais (DML)

#### Importância para Segurança
- Versionamento de schema
- Rastreabilidade de mudanças
- Backup e recuperação facilitados

### 4. Cache e Performance

#### Redis
- Cache distribuído para:
  - Sessões de usuário
  - Dados frequentemente acessados
  - Rate limiting

#### Health Checks
- Monitoramento de:
  - Conexão com banco de dados
  - Serviço de cache
  - Métricas do sistema

#### Importância para Performance
- Redução de carga no banco
- Melhor tempo de resposta
- Alta disponibilidade

## Configuração do Ambiente

### Requisitos
- Python 3.11+
- SQL Server 2019+
- Redis 7.0+

### Variáveis de Ambiente (.env)
```bash
# Banco de Dados Master
MASTER_DB_HOST=localhost
MASTER_DB_PORT=1433
MASTER_DB_NAME=fdw00
MASTER_DB_USER=sa
MASTER_DB_PASS=YourStrong!Passw0rd

# Redis
REDIS_URL=redis://localhost:6379/0

# Segurança
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# API
PROJECT_NAME="Financial System"
VERSION="1.0.0"
API_V1_STR="/api/v1"
```

## Instalação e Execução

1. Clone o repositório
```bash
git clone [repository_url]
cd backend
```

2. Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure o arquivo .env

5. Execute as migrações
```bash
python -m app.core.db.migrations.migrate
```

6. Inicie o servidor
```bash
uvicorn app.main:app --reload
```

## Segurança e Boas Práticas

### Práticas de Código
- Tipagem estática com Python type hints
- Validação de dados com Pydantic
- Documentação detalhada com docstrings
- Logs estruturados

### Segurança
- Senhas hasheadas com bcrypt
- Headers de segurança HTTP
- Rate limiting por IP/usuário
- Proteção contra ataques comuns (XSS, CSRF, SQL Injection)

### Auditoria
- Log de todas as ações críticas
- Rastreamento de alterações
- Histórico de acessos
- Alertas de segurança

## Próximos Passos
- [ ] Implementação de logs estruturados
- [ ] Configuração de backups automáticos
- [ ] Implementação de métricas detalhadas
- [ ] Documentação da API com Swagger
- [ ] Testes automatizados
- [ ] CI/CD com GitHub Actions
