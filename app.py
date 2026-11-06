import json
import os
 
from flask import Flask, jsonify, request, Response, render_template
from jinja2 import ChoiceLoader, FileSystemLoader
 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
 
app = Flask(__name__)
app.json.ensure_ascii = False       
app.json.sort_keys = False
 
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    FileSystemLoader(BASE_DIR),
])
 
municipios_nordeste_dataset = {
    "metadados": {
        "regiao": "Nordeste",
        "pais": "Brasil",
        "total_municipios": 30,
        "fonte_dados_populacao": "IBGE",
    },
    "municipios": {
        "Fortaleza": {"id_ibge": 2304400, "estado": "Ceará", "sigla_uf": "CE", "capital": True, "populacao_estimada": 2582360},
        "Salvador": {"id_ibge": 2927408, "estado": "Bahia", "sigla_uf": "BA", "capital": True, "populacao_estimada": 2559945},
        "São Luís": {"id_ibge": 2111300, "estado": "Maranhão", "sigla_uf": "MA", "capital": True, "populacao_estimada": 1037775},
        "Teresina": {"id_ibge": 2211001, "estado": "Piauí", "sigla_uf": "PI", "capital": True, "populacao_estimada": 866300},
        "Natal": {"id_ibge": 2408102, "estado": "Rio Grande do Norte", "sigla_uf": "RN", "capital": True, "populacao_estimada": 751300},
        "João Pessoa": {"id_ibge": 2507507, "estado": "Paraíba", "sigla_uf": "PB", "capital": True, "populacao_estimada": 833932},
        "Recife": {"id_ibge": 2611606, "estado": "Pernambuco", "sigla_uf": "PE", "capital": True, "populacao_estimada": 1488920},
        "Maceió": {"id_ibge": 2704302, "estado": "Alagoas", "sigla_uf": "AL", "capital": True, "populacao_estimada": 957916},
        "Aracaju": {"id_ibge": 2800308, "estado": "Sergipe", "sigla_uf": "SE", "capital": True, "populacao_estimada": 602757},
        "Feira de Santana": {"id_ibge": 2910800, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 616272},
        "Vitória da Conquista": {"id_ibge": 2933307, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 370879},
        "Camaçari": {"id_ibge": 2905701, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 300372},
        "Juazeiro": {"id_ibge": 2918407, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 237821},
        "Lauro de Freitas": {"id_ibge": 2919207, "estado": "Bahia", "sigla_uf": "BA", "capital": False, "populacao_estimada": 203334},
        "Caucaia": {"id_ibge": 2303709, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 355679},
        "Juazeiro do Norte": {"id_ibge": 2307304, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 286120},
        "Maracanaú": {"id_ibge": 2307650, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 234392},
        "Sobral": {"id_ibge": 2312908, "estado": "Ceará", "sigla_uf": "CE", "capital": False, "populacao_estimada": 203023},
        "Olinda": {"id_ibge": 2609600, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 349976},
        "Jaboatão dos Guararapes": {"id_ibge": 2607901, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 643148},
        "Caruaru": {"id_ibge": 2604106, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 378052},
        "Petrolina": {"id_ibge": 2611101, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 386786},
        "Paulista": {"id_ibge": 2607208, "estado": "Pernambuco", "sigla_uf": "PE", "capital": False, "populacao_estimada": 342167},
        "Campina Grande": {"id_ibge": 2504009, "estado": "Paraíba", "sigla_uf": "PB", "capital": False, "populacao_estimada": 419379},
        "Mossoró": {"id_ibge": 2408003, "estado": "Rio Grande do Norte", "sigla_uf": "RN", "capital": False, "populacao_estimada": 264577},
        "Parnamirim": {"id_ibge": 2403251, "estado": "Rio Grande do Norte", "sigla_uf": "RN", "capital": False, "populacao_estimada": 252716},
        "Imperatriz": {"id_ibge": 2105302, "estado": "Maranhão", "sigla_uf": "MA", "capital": False, "populacao_estimada": 273110},
        "Timon": {"id_ibge": 2112209, "estado": "Maranhão", "sigla_uf": "MA", "capital": False, "populacao_estimada": 174465},
        "Parnaíba": {"id_ibge": 2207702, "estado": "Piauí", "sigla_uf": "PI", "capital": False, "populacao_estimada": 162159},
        "Arapiraca": {"id_ibge": 2700300, "estado": "Alagoas", "sigla_uf": "AL", "capital": False, "populacao_estimada": 234696},
    },
}
 
CAMPOS_OBRIGATORIOS = ["id_ibge", "estado", "sigla_uf", "capital", "populacao_estimada"]
TIPOS = {
    "id_ibge": int,
    "estado": str,
    "sigla_uf": str,
    "capital": bool,
    "populacao_estimada": int,
}
 
 
def _atualizar_total():
    municipios_nordeste_dataset["metadados"]["total_municipios"] = len(
        municipios_nordeste_dataset["municipios"]
    )
 
 
def _validar_tipos(dados):
    """Retorna mensagem de erro se algum campo tiver tipo inválido."""
    for campo, valor in dados.items():
 
        if campo not in TIPOS:
            return f"O campo '{campo}' não é permitido."
 
        esperado = TIPOS[campo]
 
        if esperado is int and isinstance(valor, bool):
            return f"O campo '{campo}' deve ser {esperado.__name__}."
 
        if not isinstance(valor, esperado):
            return f"O campo '{campo}' deve ser {esperado.__name__}."
 
    return None
 
 
def _erro(mensagem, status):
    return jsonify({"erro": mensagem}), status
 
@app.get("/")
def home():
    return render_template("index.html")
 
 
@app.get("/metadados")
def metadados():
    return jsonify(municipios_nordeste_dataset["metadados"]), 200
 
@app.get("/download/municipios.json")
def download_json():
    conteudo = json.dumps(
        municipios_nordeste_dataset["municipios"], ensure_ascii=False, indent=2
    )
    return Response(
        conteudo,
        mimetype="application/json",
        headers={"Content-Disposition": "attachment; filename=municipios.json"},
    )
 
@app.get("/municipios")
def listar_municipios():
    uf = request.args.get("uf")
    municipios = municipios_nordeste_dataset["municipios"]
 
    if uf:
        uf = uf.strip().upper()
        filtrados = {}
        for nome, dados in municipios.items():
            if dados["sigla_uf"] == uf:
                filtrados[nome] = dados
        return jsonify(filtrados), 200
 
    return jsonify(municipios), 200
 
 
@app.get("/municipios/<nome>")
def consultar_municipio(nome):
    municipio = municipios_nordeste_dataset["municipios"].get(nome)
    if municipio is None:
        return _erro(f"Município '{nome}' não encontrado.", 404)
    return jsonify({nome: municipio}), 200
 
 
@app.post("/municipios")
def cadastrar_municipio():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return _erro("Envie um corpo JSON válido.", 400)
 
    nome = dados.pop("nome", None)
    if not isinstance(nome, str) or not nome.strip():
        return _erro("O campo 'nome' é obrigatório.", 400)
    nome = nome.strip()
 
    faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in dados]
    if faltando:
        return _erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}.", 400)
 
    desconhecidos = [c for c in dados if c not in TIPOS]
    if desconhecidos:
        return _erro(f"Campos não permitidos: {', '.join(desconhecidos)}.", 400)
 
    erro_tipo = _validar_tipos(dados)
    if erro_tipo:
        return _erro(erro_tipo, 400)
 
    if nome in municipios_nordeste_dataset["municipios"]:
        return _erro(f"Município '{nome}' já cadastrado.", 409)
 
    dados["sigla_uf"] = dados["sigla_uf"].upper()
    municipios_nordeste_dataset["municipios"][nome] = dados
    _atualizar_total()
    return jsonify({nome: dados}), 201
 
 
@app.put("/municipios/<nome>")
def substituir_municipio(nome):
    """PUT: substitui o registro INTEIRO (todos os campos são obrigatórios)."""
    municipios = municipios_nordeste_dataset["municipios"]
    if nome not in municipios:
        return _erro(f"Município '{nome}' não encontrado.", 404)
 
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return _erro("Envie um corpo JSON válido.", 400)
 
    faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in dados]
    if faltando:
        return _erro(f"Campos obrigatórios ausentes: {', '.join(faltando)}.", 400)
 
    desconhecidos = [c for c in dados if c not in TIPOS]
    if desconhecidos:
        return _erro(f"Campos não permitidos: {', '.join(desconhecidos)}.", 400)
 
    erro_tipo = _validar_tipos(dados)
    if erro_tipo:
        return _erro(erro_tipo, 400)
 
    novo = {campo: dados[campo] for campo in CAMPOS_OBRIGATORIOS}
    novo["sigla_uf"] = novo["sigla_uf"].upper()
    municipios[nome] = novo
    return jsonify({nome: novo}), 200
 
 
@app.patch("/municipios/<nome>")
def atualizar_municipio(nome):
    municipios = municipios_nordeste_dataset["municipios"]
    if nome not in municipios:
        return _erro(f"Município '{nome}' não encontrado.", 404)
 
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict) or not dados:
        return _erro("Envie um corpo JSON com os campos a atualizar.", 400)
 
    desconhecidos = [c for c in dados if c not in TIPOS]
    if desconhecidos:
        return _erro(f"Campos não permitidos: {', '.join(desconhecidos)}.", 400)
 
    erro_tipo = _validar_tipos(dados)
    if erro_tipo:
        return _erro(erro_tipo, 400)
 
    if "sigla_uf" in dados:
        dados["sigla_uf"] = dados["sigla_uf"].upper()
 
    municipios[nome].update(dados)
    return jsonify({nome: municipios[nome]}), 200
 
 
@app.delete("/municipios/<nome>")
def excluir_municipio(nome):
    removido = municipios_nordeste_dataset["municipios"].pop(nome, None)
    if removido is None:
        return _erro(f"Município '{nome}' não encontrado.", 404)
    _atualizar_total()
    return jsonify({"mensagem": f"Município '{nome}' removido com sucesso."}), 200
 
 
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
 
