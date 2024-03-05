#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from flask_restful import Resource, reqparse
from aplicacion.modelos.curso import CursoModel
from aplicacion.modelos.profesor import ProfesorModel

class Curso(Resource):

    # Acá nos funciona porque en BD tiene un default NOW() pero si usamos el filtro debemos añadir todos los parámetros necesarios.
    parser = reqparse.RequestParser()
    parser.add_argument('nombre',
        type=str,
        required=True,
        help="Debe ingresar un nombre para el curso"
    )
    parser.add_argument('id_profesor',
        type=int,
        required=True,
        help="Debe ingresar el identificador del profesor que dictará el curso."
    )
    parser.add_argument('nivel',
        type=int,
        required=True,
        choices=(1, 2, 3, 4),
        help="Debe ingresar el nivel (entero del 1 al 4)."
    )
    parser.add_argument('activo',
        type=int,
        required=False,
        choices=(0, 1),
        help="Debe ingresar 0 para estado inactivo y 1 para estado activo."
    )

    def get(self, _id):
        curso = CursoModel.buscar_por_id(_id)
        if curso:
            return curso.obtener_datos()
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404

    def delete(self, _id):
        curso = CursoModel.buscar_por_id(_id)
        if curso:
            try:
                curso.eliminar()
                return {'message': 'Curso eliminado con éxito'}
            except Exception as e:
                return {'message': 'No se pudo realizar la eliminación Error: {}'.format(str(e))}, 500
        else :
            return {'mensaje': 'No se encontró el recurso solicitado'}, 404

    def put(self, _id):
        data = Curso.parser.parse_args()

        curso = CursoModel.buscar_por_id(_id)
        if curso:
            curso.nombre = data['nombre']
            curso.id_profesor = data['id_profesor']
            curso.nivel = data['nivel']
            curso.activo = data['activo']

            try:
                curso.guardar()
            except Exception as e:
                return {"message": "No se pudo resolver su petición. Error: {}".format(str(e))}, 500
            return curso.obtener_datos(), 200
        else:
            return {'mensaje': 'No se encontró el recurso solicitado'}, 404


#crear PUT


class Cursos(Curso):
    def get(self):
        cursos = CursoModel.obtener_todos()
        return [curso.obtener_datos() for curso in cursos], 200
    def post(self):
        data = Cursos.parser.parse_args() 

        if CursoModel.buscar_existencia(data['nombre']):
            return {'message': "Ya existe un curso llamado '{}'. Póngase creativo!".format(data['nombre'])}, 400
        if ProfesorModel.buscar_por_id(data['id_profesor']):
            fecha_creacion = data.get('fecha_creacion')  # Usa get en lugar de []
            if fecha_creacion is None: 
                fecha_actual = datetime.now()
                fecha_creacion = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

            activo = data.get('activo')  # Usa get en lugar de []
            if activo is None:
                activo = 1

            curso = CursoModel(data['nombre'],data['id_profesor'], data['nivel'], activo, fecha_creacion)

            try:
                curso.guardar()
            except Exception as e:
                return {"message": "No se pudo resolver su petición. Error: {}".format(str(e))}, 500
            return curso.obtener_datos(), 201

        else :
            return {'message': "El identificador del profesor ingresado no es válido"}, 400

class AlumnosCurso(Resource):


    def get(self, _id):
        curso = CursoModel.buscar_por_id(_id)
        if curso:
            return curso.obtener_alumnos()
        return {'mensaje': 'No se encontró el recurso solicitado'}, 404
