from flask import Blueprint, Response, jsonify
from app.db import get_all
from app.controllers.estadisticas_controller import generar_csv_estadisticas

estadisticas_bp = Blueprint('estadisticas', __name__, url_prefix='/estadisticas')

@estadisticas_bp.route('/exportar', methods=['GET'])
def exportar_estadisticas():
    csv_data = generar_csv_estadisticas()

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=estadisticas.csv"}
    )

@estadisticas_bp.route('/detalle/<int:id_eleccion>', methods=['GET'])
def detalle_eleccion(id_eleccion):
    eleccion = get_all("SELECT tipo FROM Eleccion WHERE id_eleccion = %s AND status = FALSE", (id_eleccion,))
    if not eleccion:
        return jsonify({"error": "Elección no encontrada o no está cerrada"}), 404

    tipo = eleccion[0]['tipo'].lower()

    if tipo == "presidencial":
        listas = get_all("""
            SELECT l.id, lp.presidente as candidato
            FROM Lista_Presidencial lp
            JOIN Lista l ON l.id = lp.id
        """)
    elif tipo == "ballotage":
        listas = get_all("""
            SELECT l.id, lb.candidato
            FROM Lista_Ballotage lb
            JOIN Lista l ON l.id = lb.id
        """)
    elif tipo == "municipal":
        listas = get_all("""
            SELECT l.id, lm.candidato
            FROM Lista_Municipal lm
            JOIN Lista l ON l.id = lm.id
        """)
    elif tipo in ["plebiscito", "referendum"]:
        listas = get_all("""
            SELECT l.id, p.opcion as candidato
            FROM Papeleta p
            JOIN Lista l ON l.id = p.id
        """)
    else:
        return jsonify({"error": "Tipo de elección no soportado"}), 400

    lista_ids = [l['id'] for l in listas]

    if not lista_ids:
        return jsonify([])

    placeholders = ','.join(['%s'] * len(lista_ids))

    votos_por_lista = get_all(f"""
        SELECT id_lista, COUNT(*) as votos
        FROM Voto
        WHERE id_lista IN ({placeholders})
        GROUP BY id_lista
    """, lista_ids)

    candidato_map = {l['id']: l['candidato'] for l in listas}

    total_votos = sum(v['votos'] for v in votos_por_lista)

    resultados = []
    for v in votos_por_lista:
        lista_id = v['id_lista']
        votos = v['votos']
        porcentaje = round((votos / total_votos) * 100, 2) if total_votos > 0 else 0
        resultados.append({
            "id_lista": lista_id,
            "candidato": candidato_map.get(lista_id, "N/A"),
            "votos": votos,
            "porcentaje": porcentaje
        })

    return jsonify(resultados)
