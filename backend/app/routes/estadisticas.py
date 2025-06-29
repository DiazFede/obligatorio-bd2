from flask import Blueprint, Response
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
