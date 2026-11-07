# AST12 — Implementando Integração Contínua (CI) com GitHub Actions

Repositório referente à atividade prática **AST12** da disciplina de **Automação de Testes de Software (ATS)** — Faculdade Impacta.

## 1. Objetivo do Projeto

Construir uma API RESTful em Python utilizando **FastAPI** e configurar um pipeline completo de **Integração Contínua (CI)** com **GitHub Actions** capaz de:

1. Executar testes automatizados com `pytest` a cada `push` e `Pull Request`.
2. Identificar regressões e erros de implementação automaticamente na nuvem (Runner Ubuntu).
3. Bloquear a integração (merge) de código defeituoso na branch principal (`main`) por meio de regras de proteção de branch (*Branch Protection Rules* / *Rulesets*).
4. Utilizar **Strategy Matrix** para validar a aplicação simultaneamente nas versões **Python 3.10, 3.11 e 3.12**.
5. Executar testes de integração (caixa-preta) subindo o servidor real no Runner do GitHub e realizando requisições HTTP com `curl`.

---

## 2. Descrição da API

A API está implementada em `main.py` e disponibiliza os seguintes endpoints:

| Método | Rota | Descrição | Exemplo de Resposta (JSON) |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Rota principal (Healthcheck) | `{"mensagem": "API AST12 funcionando!"}` |
| `GET` | `/somar/{a}/{b}` | Soma dois números inteiros `a` e `b` | `{"resultado": 8}` (para `/somar/5/3`) |
| `GET` | `/multiplicar/{a}/{b}` | Multiplica dois números inteiros `a` e `b` | `{"resultado": 12}` (para `/multiplicar/4/3`) |

---

## 3. Tecnologias Utilizadas

- **Python** (compatível com 3.10, 3.11, 3.12+)
- **FastAPI** (`fastapi[standard]`) — Framework web para construção da API e servidor CLI.
- **Pytest** (`pytest`) — Framework de execução de testes automatizados.
- **HTTPX** (`httpx`) — Cliente HTTP necessário para o `TestClient` do FastAPI.
- **Git & GitHub** — Controle de versão e hospedagem do repositório.
- **GitHub Actions** — Plataforma de CI/CD para automação do pipeline de testes.

---

## 4. Estrutura de Diretórios

```text
AST12-Actions/
├── .github/
│   └── workflows/
│       └── ci.yml          # Definição do pipeline de CI no GitHub Actions
├── .gitignore              # Arquivos e diretórios ignorados pelo Git (.venv, cache, etc.)
├── main.py                 # Implementação da API FastAPI
├── test_main.py            # Suite de testes automatizados com Pytest e TestClient
├── requirements.txt        # Lista de dependências do projeto
└── README.md               # Documentação completa do projeto
```

---

## 5. Pré-requisitos

- **Python 3.10+** instalado e adicionado ao `PATH`.
- **Git** instalado.

---

## 6. Configuração do Ambiente no Windows PowerShell

Execute os comandos abaixo na raiz do projeto no **Windows PowerShell**:

### 6.1. Criar e ativar o ambiente virtual (`.venv`)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

> **Dica:** Caso o PowerShell bloqueie a execução do script de ativação, libere temporariamente na sessão atual com:
> `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process`

### 6.2. Instalar as dependências

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

## 7. Como Executar a API Localmente

Com o ambiente virtual ativo, inicie o servidor de desenvolvimento do FastAPI:

```powershell
fastapi dev main.py
```

Ou em modo de produção na porta `8000`:

```powershell
fastapi run main.py --port 8000
```

- Acesse a API em: `http://localhost:8000/`
- Documentação interativa (Swagger UI): `http://localhost:8000/docs`

---

## 8. Como Executar os Testes Localmente

Para rodar a bateria completa de testes automatizados com `pytest`:

```powershell
pytest test_main.py -v
```

Testes implementados em `test_main.py`:
- `test_read_root_status_code`: Valida status HTTP 200 na rota `/`.
- `test_read_root_content`: Valida o JSON `{"mensagem": "API AST12 funcionando!"}` na rota `/`.
- `test_somar_positivos`: Valida a soma de inteiros positivos (`/somar/5/3` -> `8`).
- `test_somar_negativos`: Valida a soma com inteiros negativos (`/somar/-5/-3` -> `-8`).
- `test_multiplicar`: Valida a multiplicação de inteiros (`/multiplicar/4/3` -> `12`).
- `test_multiplicar_por_zero`: Valida a multiplicação por zero (`/multiplicar/10/0` -> `0`).

---

## 9. Pipeline de CI no GitHub Actions (`.github/workflows/ci.yml`)

O workflow **CI - Testes da API** é acionado automaticamente nos eventos `push` e `pull_request`.

### 9.1. O Job `verificar-api`
O Job principal chama-se exatamente `verificar-api`. Ele é executado em uma máquina virtual limpa (`ubuntu-latest`) fornecida pelo GitHub Actions e realiza:
1. **Checkout do repositório** (`actions/checkout@v4`): Baixa o código-fonte para o Runner.
2. **Setup Python** (`actions/setup-python@v5`): Instala a versão especificada do Python com cache de pacotes `pip`.
3. **Instalação de dependências**: Atualiza o `pip` e instala os pacotes listados em `requirements.txt`.
4. **Execução dos testes (`Rodar Testes`)**: Executa `pytest test_main.py`. Qualquer falha interrompe o pipeline com código de saída diferente de zero.

> As etapas de **Strategy Matrix**, **Teste de Integração com `curl`** e **Fluxo de Pull Requests** serão detalhadas e atualizadas conforme o progresso das etapas práticas da atividade.

---

## 10. Histórico de Etapas da Atividade

- [x] **Parte 1 — Preparação e Configuração Inicial**: Criação da API FastAPI (`main.py`), testes unitários (`test_main.py`) e workflow inicial (`.github/workflows/ci.yml`).
- [ ] **Parte 2 — Simulação de Erro no CI (Na branch `main`)**: Introdução proposital de bug na rota `/somar/{a}/{b}` para diagnóstico de falha no GitHub Actions e posterior restauração.
- [ ] **Parte 3 — Proteção da Branch `main` e Fluxo de Pull Request**: Configuração de proteção exigindo o status check `verificar-api`, criação da branch `feature-multiplicacao`, simulação de teste falhando no PR e correção.
- [ ] **Parte 4 — Evolução do Pipeline com Strategy Matrix**: Execução paralela em Python `3.10`, `3.11` e `3.12`.
- [ ] **Parte 5 — Teste de Integração no Runner com `curl`**: Inicialização da API em background no Runner e requisições HTTP reais.
