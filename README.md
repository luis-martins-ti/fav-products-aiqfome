# API GESTÃO DE PRODUTOS FAVORITOS

API REST para gerenciar produtos favoritos de clientes.

Validação de E-mail
Autenticação JWT
Controle de Permissões
Banco de dados PostgreSQL
Docker para orquestração
Testes unitários e integrados
---

## 🚀 Como iniciar o projeto

### ✅ Pré-requisitos
- Docker + Docker Compose

---

### 🧱 STEP 1 - Build e start com Docker

**Renomeie o arquivo .env.example para .env e execute:**

```bash
docker compose build --no-cache
docker compose up -d
```

### 📦 STEP 2 - Criar banco e aplicar migrações SqlAlchemy + 

As migrações rodam automaticamente ao inicializar a aplicação com Docker. Aguarde alguns segundos.


### 🖥️ STEP 3 - Iniciar a aplicação
A aplicação se inicia automaticamente com o Docker após alguns segundos. Para acessar a API use: http://localhost:8000/

### 📚 DOCUMENTAÇÃO:
Acesse a documentação interativa no navegador:
```bash
 http://localhost:8000/docs
```
Se preferir, existe o arquivo **AiQFome API.postman_collection** já configurado para usar o token do login de forma automática nas rotas.
Com essa collection é possível testar todas as rotas, inclusive criar um usuário **ADMIN** para verificar a detalhes de clientes por ID, lista de clientes e favoritos de clientes por ID. Usuários **NÃO ADMIN** somente podem visualizar seus dados de cliente e favoritos.
Todos clientes cadastrados são automáticamente vinculados ao usuário logado. Todos favoritos cadastrados são vinculado ao cliente logado.

**Como importar AiQFome API.postman_collection no Postman**
Postman:

Vá em Import > File > Upload Files > AiQFome API.postman_collection
Os endpoints serão importados automaticamente.


### 🧪 TESTES:
Rodar fora do container:

```bash
docker-compose exec web pytest app/tests
```
**Estrutura usada para testes:**
Testes estão localizados na pasta tests
Usa Pytest para simular requisições HTTP reais
Logs e observações via terminal:
```bash
docker-compose logs -f web
```

### 🛠️ TROBLESHOOTING:
| Erro                                         | Causa provável                   | Solução                                                        |
|----------------------------------------------|----------------------------------|----------------------------------------------------------------|
| Container aiqfome encerra sozinho            | Erro de construção do app        | Rode `docker compose down -v --remove-orphans` e depois build  |




### 📘 Tecnologias Utilizadas
- Python 3.10+
- FastAPI
- SQLAlchemy + Alembic
- PostgreSQL
- Docker & Docker Compose
- Pytest para testes

### Arquitetura:
rural_api/
├── app/
│   ├── api/                  # Rotas
│   ├── auth/                 # Autenticação JWT
│   ├── core/             	  # Configurações    
│   ├── db/              	    # Models e database
│   ├── schemas/              # Pydantic Validations
│   ├── services/         	  # Lógica de negócio	
│   └── tests/                # Testes
├── Dockerfile
├── docker-compose.yml
├── .env
├── requirements.txt
└── README.md

**Para encerrar a aplicação basta executar:**
```bash
docker compose down -v --remove-orphans
```