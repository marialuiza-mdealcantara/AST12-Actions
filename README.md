# AST12 — Implementando Integração Contínua (CI) com GitHub Actions

[![CI - Testes da API](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/workflows/ci.yml/badge.svg)](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/workflows/ci.yml)

Repositório referente à atividade prática **AST12 — Implementando Integração Contínua (CI) com GitHub Actions** da disciplina de **Automação de Testes de Software (ATS)** — Faculdade Impacta.

- **Repositório GitHub:** https://github.com/marialuiza-mdealcantara/AST12-Actions
- **Material de Referência:** https://giovbon.github.io/impacta/AST/12ATS-PG-github-actions/

---

## 1. Nome da Atividade

**AST12 — Implementando Integração Contínua (CI) com GitHub Actions**

---

## 2. Objetivo do Projeto

Construir uma API RESTful em Python utilizando **FastAPI** e configurar um pipeline completo de **Integração Contínua (CI)** com **GitHub Actions** que:

1. Execute testes automatizados com `pytest` a cada `push` e `Pull Request`.
2. Identifique erros de implementação automaticamente na nuvem (Runner Linux Ubuntu).
3. Impeça a integração (*merge*) de código com testes falhando na branch `main` usando regras de proteção de branch (*Branch Protection Rules*).
4. Utilize **Strategy Matrix** para testar simultaneamente diferentes versões do Python (`3.10`, `3.11` e `3.12`).
5. Execute um teste de integração real (caixa-preta) subindo o servidor da API em background e realizando requisições HTTP reais com `curl` dentro do Runner do GitHub.

---

## 3. Descrição da API

A API está implementada no arquivo `main.py` e disponibiliza três rotas HTTP `GET`:

| Método | Rota | Parâmetros | Descrição | Exemplo de Retorno (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Nenhum | Rota principal de verificação de status da API | `{"mensagem": "API AST12 funcionando!"}` |
| `GET` | `/somar/{a}/{b}` | `a: int`, `b: int` | Retorna a soma de dois números inteiros (`a + b`) | `{"resultado": 8}` (para `/somar/5/3`) |
| `GET` | `/multiplicar/{a}/{b}` | `a: int`, `b: int` | Retorna a multiplicação de dois números inteiros (`a * b`) | `{"resultado": 4}` (para `/multiplicar/2/2`) |

---

## 4. Tecnologias Utilizadas

- **Python** (`3.10`, `3.11`, `3.12+`) — Linguagem de programação principal.
- **FastAPI** (`fastapi[standard]`) — Framework web de alta performance para construção de APIs e CLI (`fastapi-cli` / `uvicorn`).
- **Pytest** (`pytest`) — Framework de testes automatizados em Python.
- **HTTPX** (`httpx`) — Cliente HTTP utilizado pelo `TestClient` do FastAPI.
- **Git & GitHub** — Controle de versão distribuído, gerenciamento de branches e Pull Requests.
- **GitHub Actions** — Plataforma de Integração Contínua (CI) para execução automatizada de workflows em Runners `ubuntu-latest`.
- **cURL** — Ferramenta de linha de comando para testes de integração via requisições HTTP no Runner.

---

## 5. Estrutura de Diretórios

```text
AST12-Actions/
├── .github/
│   └── workflows/
│       └── ci.yml          # Pipeline de Integração Contínua do GitHub Actions
├── .gitignore              # Regras de arquivos ignorados pelo Git (.venv, cache, etc.)
├── main.py                 # Implementação da API FastAPI
├── test_main.py            # Testes automatizados com Pytest e TestClient
├── requirements.txt        # Dependências do projeto (fastapi[standard], pytest, httpx)
└── README.md               # Documentação completa da atividade AST12
```

---

## 6. Pré-requisitos

- **Python 3.10 ou superior** instalado (com opção `Add Python to PATH` marcada).
- **Git** instalado e configurado.
- Terminal **Windows PowerShell**.

---

## 7. Instruções para Criar e Ativar o Ambiente Virtual no Windows PowerShell

Abra o terminal **PowerShell** na pasta raiz do projeto e execute:

```powershell
# 1. Criar o ambiente virtual na pasta .venv
python -m venv .venv

# 2. Ativar o ambiente virtual no PowerShell
.\.venv\Scripts\Activate.ps1
```

> **Observação:** Caso o PowerShell exiba erro de política de execução de scripts (`ExecutionPolicy`), execute o comando abaixo para permitir na sessão atual e tente ativar novamente:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
> ```

---

## 8. Instalação das Dependências

Com o ambiente virtual `.venv` ativado, atualize o `pip` e instale os pacotes do arquivo `requirements.txt`:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

As dependências instaladas a partir do `requirements.txt` são:
- `fastapi[standard]` (inclui `uvicorn` e o comando CLI `fastapi`)
- `pytest`
- `httpx`

---

## 9. Como Executar a API Localmente

Para iniciar a API localmente em modo de desenvolvimento (com *auto-reload*):

```powershell
fastapi dev main.py
```

Ou para iniciar o servidor em modo de execução na porta `8000` (mesmo comando usado no Runner):

```powershell
fastapi run main.py --port 8000
```

Após iniciar o servidor, você pode acessar no navegador ou via terminal:
- **Rota principal:** `http://localhost:8000/`
- **Exemplo de soma:** `http://localhost:8000/somar/10/20`
- **Exemplo de multiplicação:** `http://localhost:8000/multiplicar/2/2`
- **Documentação Swagger UI:** `http://localhost:8000/docs`

---

## 10. Como Executar os Testes

Para executar todos os testes automatizados definidos em `test_main.py`:

```powershell
pytest test_main.py -v
```

### Casos de Teste Implementados (`test_main.py`):
1. `test_read_root_status_code`: Verifica se `GET /` responde com status HTTP `200`.
2. `test_read_root_content`: Verifica se `GET /` retorna `{"mensagem": "API AST12 funcionando!"}`.
3. `test_somar_positivos`: Verifica a soma de números positivos (`GET /somar/5/3` -> `{"resultado": 8}`).
4. `test_somar_negativos`: Verifica a soma com números negativos (`GET /somar/-5/-3` -> `{"resultado": -8}`).
5. `test_multiplicar`: Verifica a multiplicação (`GET /multiplicar/2/2` -> `{"resultado": 4}`).
6. `test_multiplicar_por_zero`: Verifica a multiplicação por zero (`GET /multiplicar/10/0` -> `{"resultado": 0}`).

---

## 11. Explicação do Workflow do GitHub Actions (`.github/workflows/ci.yml`)

O pipeline de Integração Contínua está definido em `.github/workflows/ci.yml` sob o nome **`CI - Testes da API`**.

- **Gatilhos (`on: [push, pull_request]`):** O workflow é disparado automaticamente sempre que um novo código é enviado (`git push`) ou quando um Pull Request é aberto ou atualizado no repositório.
- **Runner (`runs-on: ubuntu-latest`):** Cada execução acontece em uma máquina virtual Linux Ubuntu limpa fornecida pelo GitHub.

---

## 12. Explicação do Job `verificar-api`

O Job principal do pipeline possui o identificador exato **`verificar-api`**. Esse nome é utilizado nas regras de proteção da branch `main` (*Required status checks*) para garantir que nenhum código seja integrado sem antes passar por todas as etapas deste Job:

1. **Checkout do repositório (`actions/checkout@v4`):** Clona o código do repositório para dentro do Runner.
2. **Setup Python (`actions/setup-python@v5`):** Instala a versão do Python definida pela matriz e habilita o cache do `pip` (`cache: 'pip'`) para acelerar execuções futuras.
3. **Instalar dependências:** Atualiza o `pip` e instala os pacotes do `requirements.txt`.
4. **Rodar Testes:** Executa `pytest test_main.py`. Se qualquer asserção falhar, o Pytest retorna código de saída `1`, interrompendo o Job e marcando o workflow como falho (`❌`).
5. **Subir a API e testar requisição (Integração):** Inicia o servidor real da API em segundo plano e testa os endpoints via `curl`.

---

## 13. Explicação da Strategy Matrix

Para garantir compatibilidade em diferentes ambientes de produção sem duplicar o código YAML, o Job `verificar-api` utiliza o recurso **`strategy.matrix`**:

```yaml
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']
```

E referencia a variável dinamicamente no passo de configuração do Python:

```yaml
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
```

Com isso, o GitHub Actions clona o Job automaticamente em **3 Runners paralelos e independentes**:
- `verificar-api (3.10)`
- `verificar-api (3.11)`
- `verificar-api (3.12)`

---

## 14. Explicação do Teste de Integração com `curl`

Enquanto os testes com `TestClient` do FastAPI simulam requisições em memória, o último passo do pipeline executa um **teste de integração real (caixa-preta)** dentro do Runner:

```yaml
      - name: Subir a API e testar requisição (Integração)
        run: |
          # O '&' no final roda a API em background para não travar o Runner
          fastapi run main.py --port 8000 &
          
          # Dá 3 segundos para o servidor ligar completamente
          sleep 3
          
          # O '-f' faz o CI falhar se a API retornar erro (ex: 404 ou 500)
          curl -f http://localhost:8000/
          curl -f http://localhost:8000/somar/10/20
```

- `fastapi run main.py --port 8000 &`: Sobe o servidor Uvicorn/FastAPI em segundo plano (`&`) na porta `8000` sem bloquear o terminal do Runner.
- `sleep 3`: Aguarda 3 segundos para garantir que o servidor concluiu a inicialização.
- `curl -f ...`: Faz requisições HTTP reais às rotas `/` e `/somar/10/20`. A flag `-f` (`--fail`) instrui o `curl` a retornar um código de erro ao shell caso a resposta HTTP seja de erro (`4xx` ou `5xx`), fazendo o pipeline falhar imediatamente caso a API não responda como esperado.

---

## 15. Explicação do Fluxo de Pull Requests e Simulações Pedagógicas

Durante a atividade, foram realizadas duas simulações práticas de falha para comprovar o papel do CI como "Guarda-Costas" do repositório:

### 15.1. Simulação 1 — Erro direto na `main` (Parte 2 do PDF)
- **Ação realizada:** A função `somar` em `main.py` foi alterada propositalmente para subtrair (`return {"resultado": a - b}`) no commit `38c8f57`.
- **Propósito pedagógico:** Observar o GitHub Actions detectar a regressão imediatamente (`Run #2`) e diagnosticar o erro real pelos logs do passo `Rodar Testes`.
- **Diagnóstico obtido nos logs do Runner:**
  - **Qual foi a mensagem exata de erro que o Pytest imprimiu?**
    `AssertionError: assert {'resultado': 2} == {'resultado': 8}` (em `test_somar_positivos`) e `AssertionError: assert {'resultado': -2} == {'resultado': -8}` (em `test_somar_negativos`).
  - **O que ele esperava receber e o que ele recebeu de fato?**
    Para `/somar/5/3`, o teste esperava receber `{'resultado': 8}` (`5 + 3`), mas recebeu de fato `{'resultado': 2}` (`5 - 3`).
- **Resolução:** A função foi restaurada para `a + b` no commit `2298ed7` e o pipeline voltou ao estado verde (`Run #3`).

### 15.2. Simulação 2 — Proteção de Branch e Pull Request Bloqueado (Parte 3 do PDF)
- **Ação realizada:** A branch `main` foi protegida em *Settings > Branches* exigindo Pull Request (`Require a pull request before merging`) e aprovação obrigatória do status check `verificar-api` (`Require status checks to pass before merging`). Na branch `feature-multiplicacao`, o teste `test_multiplicar` foi configurado para esperar um valor incorreto (`2 * 2 == 5`) no commit `153be56` e o [Pull Request #1](https://github.com/marialuiza-mdealcantara/AST12-Actions/pull/1) foi aberto.
- **Propósito pedagógico:** Comprovar que o GitHub bloqueia o botão de **Merge pull request** (`All checks have failed`) quando o check `verificar-api` falha, impedindo que código quebrado chegue à branch principal.
- **Resolução:** O teste foi corrigido para esperar `4` na mesma branch (`feature-multiplicacao`, commit `e058258`), o Pull Request #1 atualizou automaticamente, os checks ficaram verdes (`All checks have passed`) e o merge para a `main` foi liberado e concluído (`commit 69c0892`).

---

## 16. Histórico das Etapas da Atividade

| Etapa | Descrição | Commit / Referência | Status no CI |
| :--- | :--- | :--- | :--- |
| **Parte 1** | Criação da API FastAPI, testes iniciais e pipeline inicial do GitHub Actions | `3a079c8` / `8b037ad` ([Run #1](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42410142429)) | ✅ Verde (`success`) |
| **Parte 2 (Erro)** | Simulação de erro intencional na rota de soma (`a - b`) na branch `main` | `38c8f57` ([Run #2](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42410512828)) | ❌ Falha esperada (`failure`) |
| **Parte 3 (Fix main)** | Restauração da operação correta de soma (`a + b`) na branch `main` | `2298ed7` ([Run #3](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42410840076)) | ✅ Verde (`success`) |
| **Parte 3 (PR Erro)** | Branch `feature-multiplicacao` com teste falhando (`2 * 2 == 5`) e bloqueio no PR #1 | `153be56` ([PR #1](https://github.com/marialuiza-mdealcantara/AST12-Actions/pull/1) / [Run #5](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42417531358)) | ❌ Merge bloqueado (`failure`) |
| **Parte 3 (PR Fix)** | Correção do teste (`2 * 2 == 4`) na branch `feature-multiplicacao` e Merge do PR #1 | `e058258` / `69c0892` ([Run #7](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42417760748)) | ✅ Verde e Merged (`success`) |
| **Parte 4** | Evolução do pipeline com `strategy.matrix` para Python `3.10`, `3.11` e `3.12` | `b929b92` ([Run #9](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42418058351)) | ✅ Verde nos 3 ambientes |
| **Parte 5** | Adição do teste de integração (caixa-preta) subindo a API no Runner com `curl -f` | `270c417` ([Run #10](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42418220937)) | ✅ Verde nos 3 ambientes |
| **Documentação** | Documentação final detalhada da atividade AST12 no `README.md` | `01606b7` ([Run #11](https://github.com/marialuiza-mdealcantara/AST12-Actions/actions/runs/42418312485)) | ✅ Verde nos 3 ambientes |
