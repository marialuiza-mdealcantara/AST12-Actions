# AST12 — Implementando Integração Contínua (CI) com GitHub Actions

Repositório referente à atividade prática **AST12 — Implementando Integração Contínua (CI) com GitHub Actions** da disciplina de **Automação de Testes de Software (ATS)** — Faculdade Impacta.

- **Repositório GitHub:** https://github.com/marialuiza-mdealcantara/AST12-Actions
- **Material de Referência:** https://giovbon.github.io/impacta/AST/12ATS-PG-github-actions/

---

## 1. Objetivo do Projeto

Construir uma API RESTful em Python utilizando **FastAPI** e configurar um pipeline completo de **Integração Contínua (CI)** com **GitHub Actions** que:

1. Execute testes automatizados com `pytest` a cada `push` e `Pull Request`.
2. Identifique erros de implementação automaticamente na nuvem (Runner Linux Ubuntu).
3. Impeça a integração (*merge*) de código com testes falhando na branch `main` usando regras de proteção de branch (*Branch Protection Rules*).
4. Utilize **Strategy Matrix** para testar simultaneamente diferentes versões do Python (`3.10`, `3.11` e `3.12`).
5. Execute um teste de integração real (caixa-preta) subindo o servidor da API em background e realizando requisições HTTP reais com `curl` dentro do Runner do GitHub.

---

## 2. Descrição da API

A API está implementada no arquivo `main.py` e disponibiliza três rotas HTTP `GET`:

| Método | Rota | Parâmetros | Descrição | Exemplo de Retorno (JSON) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | Nenhum | Rota principal de verificação de status da API | `{"mensagem": "API AST12 funcionando!"}` |
| `GET` | `/somar/{a}/{b}` | `a: int`, `b: int` | Retorna a soma de dois números inteiros (`a + b`) | `{"resultado": 8}` (para `/somar/5/3`) |
| `GET` | `/multiplicar/{a}/{b}` | `a: int`, `b: int` | Retorna a multiplicação de dois números inteiros (`a * b`) | `{"resultado": 4}` (para `/multiplicar/2/2`) |

---

## 3. Tecnologias Utilizadas

- **Python** (`3.10`, `3.11`, `3.12+`) — Linguagem de programação principal.
- **FastAPI** (`fastapi[standard]`) — Framework web de alta performance para construção de APIs e CLI (`fastapi-cli` / `uvicorn`).
- **Pytest** (`pytest`) — Framework de testes automatizados em Python.
- **HTTPX** (`httpx`) — Cliente HTTP utilizado pelo `TestClient` do FastAPI.
- **Git & GitHub** — Controle de versão distribuído, gerenciamento de branches e Pull Requests.
- **GitHub Actions** — Plataforma de Integração Contínua (CI) para execução automatizada de workflows em Runners `ubuntu-latest`.
- **cURL** — Ferramenta de linha de comando para testes de integração via requisições HTTP no Runner.

---

## 4. Estrutura de Diretórios

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

## 5. Pré-requisitos

- **Python 3.10 ou superior** instalado (com opção `Add Python to PATH` marcada).
- **Git** instalado e configurado.
- Terminal **Windows PowerShell**.

---

## 6. Criando e Ativando o Ambiente Virtual no Windows PowerShell

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

## 7. Instalação das Dependências

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

## 8. Como Executar a API Localmente

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

## 9. Como Executar os Testes Automatizados

Para executar todos os testes definidos em `test_main.py`:

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

## 10. Explicação do Workflow do GitHub Actions (`.github/workflows/ci.yml`)

O pipeline de Integração Contínua está definido em `.github/workflows/ci.yml` sob o nome **`CI - Testes da API`**.

- **Gatilhos (`on: [push, pull_request]`):** O workflow é disparado automaticamente sempre que um novo código é enviado (`git push`) ou quando um Pull Request é aberto ou atualizado no repositório.
- **Runner (`runs-on: ubuntu-latest`):** Cada execução acontece em uma máquina virtual Linux Ubuntu limpa fornecida pelo GitHub.

### 10.1. O Job `verificar-api`
O Job principal do pipeline possui o identificador exato **`verificar-api`**. Esse nome é utilizado nas regras de proteção da branch `main` (*Required status checks*) para garantir que nenhum código seja integrado sem antes passar por todas as etapas deste Job:

1. **Checkout do repositório (`actions/checkout@v4`):** Clona o código do repositório para dentro do Runner.
2. **Setup Python (`actions/setup-python@v5`):** Instala a versão do Python definida pela matriz e habilita o cache do `pip` (`cache: 'pip'`) para acelerar execuções futuras.
3. **Instalar dependências:** Atualiza o `pip` e instala os pacotes do `requirements.txt`.
4. **Rodar Testes:** Executa `pytest test_main.py`. Se qualquer asserção falhar, o Pytest retorna código de saída `1`, interrompendo o Job e marcando o workflow como falho (`❌`).
5. **Subir a API e testar requisição (Integração):** Inicia o servidor real da API em segundo plano e testa os endpoints via `curl`.

---

## 11. Explicação da Strategy Matrix

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

## 12. Explicação do Teste de Integração com `curl`

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

## 13. Explicação do Fluxo de Pull Requests e Simulações Pedagógicas

Durante a atividade, foram realizadas duas simulações práticas de falha para comprovar o papel do CI como "Guarda-Costas" do repositório:

1. **Simulação 1 — Erro direto na `main` (Parte 2):**
   - **Ação:** A função `somar` em `main.py` foi alterada propositalmente para subtrair (`return {"resultado": a - b}`).
   - **Propósito pedagógico:** Observar o GitHub Actions detectar a regressão imediatamente e diagnosticar o erro pelos logs do passo `Rodar Testes` (`AssertionError: assert {'resultado': 2} == {'resultado': 8}`).
   - **Resolução:** A função foi restaurada para `a + b` e o pipeline voltou ao estado verde (`✅`).

2. **Simulação 2 — Proteção de Branch e Pull Request Bloqueado (Parte 3):**
   - **Ação:** A branch `main` foi protegida exigindo Pull Request e aprovação do status check `verificar-api`. Na branch `feature-multiplicacao`, o teste `test_multiplicar` foi configurado para esperar um valor incorreto (`2 * 2 == 5`) e o Pull Request #1 foi aberto.
   - **Propósito pedagógico:** Comprovar que o GitHub bloqueia o botão de **Merge pull request** quando o check `verificar-api` falha, impedindo que código quebrado chegue à branch principal.
   - **Resolução:** O teste foi corrigido para esperar `4` na mesma branch (`feature-multiplicacao`), o PR atualizou automaticamente, os checks ficaram verdes e o merge para a `main` foi liberado e concluído.

---

## 14. Histórico das Etapas da Atividade

- [x] **Parte 1 — Preparação:** Criação do repositório, ambiente virtual `.venv`, API FastAPI (`main.py`), testes com Pytest (`test_main.py`), workflow inicial (`.github/workflows/ci.yml`) e primeira execução verde no GitHub Actions (`Run #1`).
- [x] **Parte 2 — O Dia em que a Produção Quase Caiu (Simulando um Erro):** Introdução de erro intencional na rota de soma (`a - b`), execução vermelha no GitHub Actions (`Run #2`), diagnóstico nos logs do Pytest e restauração da soma (`Run #3`).
- [x] **Parte 3 — Trabalhando como Profissional (Pull Requests):** Configuração de *Branch Protection Rule* na `main` exigindo o status check `verificar-api`, criação da branch `feature-multiplicacao` com teste falhando, verificação do bloqueio de merge no **Pull Request #1**, correção do teste e merge após CI verde.
- [x] **Parte 4 — Evoluindo o Pipeline (Strategy Matrix):** Configuração de `strategy.matrix` para testar simultaneamente nas versões Python `3.10`, `3.11` e `3.12`.
- [x] **Parte 5 — O Teste de Integração (Rodando a API no Runner):** Adição do passo de inicialização da API em background (`fastapi run main.py --port 8000 &`) e validação de caixa-preta com `curl -f` nas 3 versões do Python.
