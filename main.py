from fastapi import FastAPI

app = FastAPI(
    title="API AST12",
    description="API desenvolvida para a atividade AST12 — Implementando Integração Contínua (CI) com GitHub Actions",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {"mensagem": "API AST12 funcionando!"}


@app.get("/somar/{a}/{b}")
def somar(a: int, b: int):
    # Retorna a soma de dois números inteiros
    return {"resultado": a + b}


@app.get("/multiplicar/{a}/{b}")
def multiplicar(a: int, b: int):
    # Retorna a multiplicação de dois números inteiros
    return {"resultado": a * b}
