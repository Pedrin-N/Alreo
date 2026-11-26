"""Teste fim a fim do Alreo via HTTP: upload do empresa.db + 4 baterias de consulta."""
import json, sys, urllib.request, http.cookiejar, uuid

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
DB = sys.argv[2] if len(sys.argv) > 2 else "/app/exemplos/empresa.db"
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

def post(path, data, ctype):
    req = urllib.request.Request(BASE + path, data=data, headers={"Content-Type": ctype})
    try:
        r = opener.open(req, timeout=30); return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

b = uuid.uuid4().hex
body = (f"--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"empresa.db\"\r\n"
        "Content-Type: application/octet-stream\r\n\r\n").encode() + open(DB, "rb").read() + f"\r\n--{b}--\r\n".encode()
st, txt = post("/loadfile", body, f"multipart/form-data; boundary={b}")
print("loadfile:", st, [r[0] for r in json.loads(txt)[1]] if st == 200 else txt)

TABLES = ["FUNCIONARIO", "DEPARTAMENTO"]
def op(o, attrs, rel, idx): return {"operator": o, "atributes_values": attrs, "relation": rel, "operatorindex": idx}
casos = {
    "sigma composta": [[op("σ", "Salario > 30000 and Dnr = 5", ["FUNCIONARIO"], 0)]],
    "pi sobre sigma": [[op("π", "Pnome, Salario", [1], 0), op("σ", "Salario > 30000", ["FUNCIONARIO"], 1)]],
    "atribuicao": [["RICOS", op("σ", "Salario > 30000", ["FUNCIONARIO"], 0)],
                   [op("π", "Pnome", ["RICOS"], 0)]],
    "juncao theta": [[op("⋈", "Dnr = Dnumero", ["FUNCIONARIO", "DEPARTAMENTO"], 0)]],
}
ok = True
for nome, linhas in casos.items():
    st, txt = post("/consult", json.dumps([linhas, TABLES]).encode(), "application/json")
    ok &= st == 200
    resumo = txt[:160].replace("\n", " ")
    if st == 200:
        res = json.loads(txt)
        resumo = "; ".join(f"{len(r[0][1]) if isinstance(r[0], list) and len(r[0]) > 1 else '?'} tuplas" for r in res)
    print(f"{nome}: HTTP {st} -> {resumo}")
print("RESULTADO:", "OK" if ok else "FALHOU")
