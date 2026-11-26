# Alreo Web 2.0 — TCC (UFOP/ICEA, Sistemas de Informação)

Evolução do Alreo v1.0 (OLIVEIRA, 2024): tradutor web de Álgebra Relacional → SQL (Flask + `radb` + SQLite).
Contexto acadêmico completo, escopo, diagnóstico e cronograma: @docs/tcc/CONTEXTO.md

## Regras de trabalho

- Responder e documentar em português. Texto acadêmico segue ABNT.
- Mudanças em código da v1.0 devem ser mínimas e justificadas; registre cada uma (motivo + efeito) porque vão para o texto do TCC.
- Fora do escopo: autocomplete/sugestão de predicados.
- Ao concluir uma etapa, atualize a seção "Status e pendências" de `docs/tcc/CONTEXTO.md`.

## Armadilhas do código

- `clean_db_files()` em `app.py` apaga todo `*.db` do diretório de trabalho; não deixe bancos de exemplo (ex.: `empresa.db`) na raiz.
- `ralib/sys.ini` usa `configfile = ralib/radb.ini` (relativo ao cwd), então rode o app sempre a partir da raiz.
- `requirements.txt` é enxuto (Flask, Flask-Session, asgiref, radb); `ralib` é importado direto da pasta.
- Banco de exemplo fica em `exemplos/` (fora do alcance de `clean_db_files()`).
- Estado concorrente: fila global `requisition_queue` + thread única do radb; um `.db` por sessão (`{session_init}.db`).

## Rodar

- Docker (dev): `docker compose up --build` → http://localhost:5000 (hot-reload via volume). Detalhes: `docs/tcc/conteinerizacao.md`.
- Teste fim a fim (4 baterias sobre `empresa.db`): `docker compose exec -T alreo python tests/teste_e2e_http.py`. Todo hot-reload apaga as sessões (atexit da v1.0).
- Local: `venv\Scripts\python.exe -m pip install -r requirements.txt` e depois `venv\Scripts\python.exe app.py` (variáveis opcionais `ALREO_HOST`, `ALREO_PORT`, `ALREO_DEBUG`).
