from pydantic import BaseModel
from typing import Optional
from enum import Enum

class TipoConta(str, Enum):
    ATIVO = "ATIVO"
    PASSIVO = "PASSIVO"
    RECEITA = "RECEITA"
    DESPESA = "DESPESA"

class ContaBase(BaseModel):
    codigo: str
    descricao: str
    tipo: TipoConta

class ContaCreate(ContaBase):
    pass

class Conta(ContaBase):
    id: int

    class Config:
        orm_mode = True
