#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aplicacion.db import db
from sqlalchemy import Table, Column, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship
from aplicacion.helpers.utilidades import Utilidades
from aplicacion.modelos.alumno import AlumnoModel
from sqlalchemy.sql import func
from sqlalchemy.sql import expression
from datetime import datetime



# Se define la tabla que contiene la relación mucho a muchos
# Se aconseja que las tablas intermedias no tengan modelo. No se por qué.
# De todos modos, si se fijan en los modelos agregué esto :
# __table_args__ = {'extend_existing': True}  (linea 27 aprox en este archivo)
# Eso ayudará a que se pueda hacer multiples referencias a la misma tabla
curso_alumno = db.Table('alumno_curso',
    db.Column('id_curso', db.Integer, db.ForeignKey('curso.id'), primary_key=True),
    db.Column('id_alumno', db.Integer, db.ForeignKey('alumno.id'), primary_key=True)
)


class CursoModel(db.Model):
    __tablename__ = 'curso'
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    # Se define la relación entre el curso y el profesor (Un curso es impartido por un solo profesor)
    id_profesor = db.Column(db.Integer, db.ForeignKey('profesor.id'), nullable=False)
    nivel = db.Column(db.SMALLINT, nullable=False)
    activo = db.Column(db.Boolean, nullable=False, server_default=expression.true())
    fecha_creacion = db.Column(db.DateTime, nullable=False, server_default=func.now())

    
   
    
    # Se crea el objeto profesor
    #profesor = db.relationship('ProfesorModel',backref=db.backref('curso', lazy=True))

    # Se crea el objeto de alumnos.
    alumnos = db.relationship('AlumnoModel', secondary=curso_alumno, lazy='subquery',
    backref=db.backref('alumno-cursos', lazy=True))



    def __init__(self, nombre, id_profesor, nivel, activo, fecha_creacion):
        self.nombre = nombre
        self.id_profesor = id_profesor
        self.nivel = nivel
        self.activo = activo
        self.fecha_creacion = fecha_creacion
    


    def obtener_datos(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'id_profesor': self.id_profesor,
            'nivel': self.nivel,
            'activo': self.activo,
            'fecha_creacion': self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S") if self.fecha_creacion else None,
        }

    def obtener_alumnos(self):
        dataProfesor = {'id': self.id_profesor, 'nombres':self.profesor.nombres,
            'apellidos':self.profesor.apellidos}

        listaAlumnos = {}
        for alumno in self.alumnos:
            listaAlumnos[alumno.id] = {"nombres":alumno.nombres,"apellidos":alumno.apellidos,"fecha_inscripcion":Utilidades.formatoFecha(alumno.fecha_inscripcion), "activo":alumno.activo}
        return {'id': self.id, 'nombre': self.nombre, 'nivel': self.nivel, 'activo':  self.activo, 'profesor':dataProfesor, "alumnos":listaAlumnos}


    # Se puede ver que usamos funciones que llevan el decorador @classmethod
    # La diferencia está en que las que NO llevan el decorador se inicializan con
    # una instancia de la clase, por ende, requiere una instancia de la clase.
    # Con el decorador classmethod inicializamos implícitamente con la clase misma.
    # En este caso particular, los usamos para crear una instancia de la clase
    # en base a una consulta a la base de datos.
    # También existe el decorador @staticmethod, con lo que la función no recibe
    # implicitamente ni la clase ni una instancia de la clase. Por esto, puede ser
    # utilizada desde otra funcion de la clase o desde una instancia de esta.

    @classmethod
    def buscar_por_id(cls, id_curso):
        curso = cls.query.get(id_curso)
        if curso:
            return curso
        return None
    # Busca si existe un alumno con igual nombre y apellido.
    # No permitiremos el ingreso de coinsidencias de nombre-apellido para ejemplificar el uso de multiples filtros.
    @classmethod
    def buscar_existencia(cls, nombre):
        return cls.query.filter_by(nombre=nombre).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
