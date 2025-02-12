from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Conta, ContaCreate, TipoConta

app = FastAPI(title="Vue-Python Microservices API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:80", "http://localhost:3000", "http://127.0.0.1"],  # Adapte conforme necessário
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)

# Simulação de banco de dados em memória
contas_db = []
conta_id_counter = 1

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Endpoints da API de Contas
@app.get("/api/contas", response_model=List[Conta])
async def list_contas():
    return contas_db

@app.post("/api/contas", response_model=Conta)
async def create_conta(conta: ContaCreate):
    global conta_id_counter
    new_conta = Conta(
        id=conta_id_counter,
        codigo=conta.codigo,
        descricao=conta.descricao,
        tipo=conta.tipo
    )
    contas_db.append(new_conta)
    conta_id_counter += 1
    return new_conta

@app.get("/api/contas/{conta_id}", response_model=Conta)
async def get_conta(conta_id: int):
    conta = next((c for c in contas_db if c.id == conta_id), None)
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    return conta

@app.put("/api/contas/{conta_id}", response_model=Conta)
async def update_conta(conta_id: int, conta_update: ContaCreate):
    conta_idx = next((i for i, c in enumerate(contas_db) if c.id == conta_id), None)
    if conta_idx is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    updated_conta = Conta(
        id=conta_id,
        codigo=conta_update.codigo,
        descricao=conta_update.descricao,
        tipo=conta_update.tipo
    )
    contas_db[conta_idx] = updated_conta
    return updated_conta

@app.delete("/api/contas/{conta_id}")
async def delete_conta(conta_id: int):
    conta_idx = next((i for i, c in enumerate(contas_db) if c.id == conta_id), None)
    if conta_idx is None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    contas_db.pop(conta_idx)
    return {"message": "Conta excluída com sucesso"}
