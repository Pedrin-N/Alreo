# Conteinerização do Alreo para desenvolvimento (TCC I)

Branch: `feat/docker-dev`. Objetivo: subir o Alreo v1.0 com um único comando, sem instalar Python nem configurar caminhos, para o desenvolvedor e para o orientador. A imagem de produção e o deploy em nuvem ficam para o TCC II.

## Como usar

Pré-requisito: Docker Desktop com WSL2 (no Windows, a "Plataforma de Máquina Virtual" habilitada e a virtualização ligada na BIOS).

```
docker compose up --build
```

Acesse http://localhost:5000. O código fica montado em `/app`, então editar no host recarrega o Flask (hot-reload).

No VS Code: extensão *Dev Containers* → "Reopen in Container" (usa `.devcontainer/devcontainer.json`).

## Arquivos criados

| Arquivo | Função |
|---|---|
| `Dockerfile` | Imagem `python:3.11-slim` (mesma versão do `venv` da v1.0, 3.11.4), instala o `requirements.txt` e roda `python app.py`. |
| `docker-compose.yml` | Porta 5000, volume `.:/app` para hot-reload, `init: true` para repassar sinais. |
| `.devcontainer/devcontainer.json` | Integração com o VS Code reaproveitando o compose. |
| `.dockerignore` / `.gitignore` | Tiram da imagem/do git: `venv`, `__pycache__`, `flask_session/` e os `.db` de sessão na raiz. |

## Ajustes mínimos no código da v1.0 (saneamento)

Nenhum altera a lógica de tradução AR → SQL.

1. **`ralib/sys.ini` — caminho absoluto → relativo.** `configfile` apontava para `C:\Users\lucas\...\radb.ini`, então todo usuário precisava editar o arquivo à mão (o próprio README instrui isso). Agora é `ralib/radb.ini`, resolvido a partir da raiz do projeto, e funciona igual no Windows, no Linux e no container.
2. **`app.py` — host/porta/debug por variável de ambiente.** `app.run(debug=True)` escutava só em `127.0.0.1`, inacessível de fora do container. Agora lê `ALREO_HOST`, `ALREO_PORT` e `ALREO_DEBUG`. Sem as variáveis, o comportamento é idêntico ao da v1.0.
3. **`requirements.txt` — de ~110 pacotes para 4.** O original estava em UTF-16 e incluía pacotes de outro ambiente (jupyter, matplotlib, contourpy, scikit-learn, pywin32...), alguns dos quais falham ao compilar (`contourpy`) ou nem existem no Linux (`pywin32`). Os pacotes que ficaram têm as versões validadas no `venv`: Flask 3.1.3, Flask-Session 0.8.0, asgiref 3.12.1, radb 3.0.5 (que traz SQLAlchemy e antlr4). O original continua no histórico do git.
4. **`empresa.db` e `gerar_banco.py` → `exemplos/`.** `clean_db_files()` apaga todo `*.db` da raiz ao encerrar o app, o que destruiria o banco de exemplo. O script agora grava o banco ao lado de si mesmo.
5. **`ralib/__pycache__/` removido do versionamento.** São artefatos de compilação e não devem ficar no git.

6. **Dependências transitivas do radb fixadas** (`SQLAlchemy==2.0.54`, `antlr4-python3-runtime==4.13.2`). Sem a fixação, o build instalou SQLAlchemy 2.1.9, diferente do ambiente validado. Fixar garante que o ambiente seja reproduzível.

## Verificação (23/11/2026 — Docker Desktop 29.9.3, imagem Python 3.11.18)

Teste fim a fim via HTTP (`tests/teste_e2e_http.py`): upload de `exemplos/empresa.db` em `/loadfile` e quatro baterias em `/consult`, comparadas com SQL direto no SQLite:

| Bateria | Alreo no container | SQLite direto |
|---|---|---|
| Seleção composta σ(Salario > 30000 ∧ Dnr = 5) | 2 tuplas | 2 |
| Projeção sobre seleção π(Pnome, Salario)(σ) | 4 tuplas | 4 |
| Atribuição RICOS ← σ(...); π(Pnome)(RICOS) | 4 tuplas | 4 |
| Junção theta ⋈(Dnr = Dnumero) | 8 tuplas | 8 |

Também verificado:
- **Hot-reload:** alterar `app.py` no host gera "Detected change ... reloading" no container, e a aplicação volta a responder HTTP 200.
- **Encerramento:** `docker compose down` termina em cerca de 1 s (com `init: true`, os sinais chegam ao Python).
- **Fora do Docker** (venv, Python 3.11.4): o app também sobe com `ALREO_HOST=0.0.0.0`.

Para repetir o teste: `docker compose up -d` e depois `docker compose exec -T alreo python tests/teste_e2e_http.py`.

Comportamento herdado da v1.0, observado no modo dev: a cada hot-reload, o `atexit` (`clean_db_files` / `limpar_arquivos_session`) apaga os bancos de sessão e `flask_session/`. Salvar um arquivo, portanto, encerra as sessões abertas, e é preciso recarregar o banco na interface.

Pré-requisito do host Windows: virtualização ligada na BIOS. Sem isso, o Docker Desktop falha com `HCS_E_HYPERV_NOT_INSTALLED`. Vale registrar no texto como atrito de ambiente que permanece mesmo com Docker.

## Observações para o TCC II

- `SECRET_KEY` continua fixa no código; precisa vir de variável de ambiente antes da produção.
- `clean_db_files()`/`limpar_arquivos_session()` operam no diretório de trabalho, que no modo dev é o volume montado. Na produção, os dados de sessão devem ir para um diretório próprio.
- A fila global (`requisition_queue`) + thread única do radb continua sendo o gargalo multiusuário.
