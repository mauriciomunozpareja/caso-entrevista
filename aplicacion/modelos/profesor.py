from aplicacion.db import db
from sqlalchemy.sql import expression

#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ProfesorModel(db.Model):
    __tablename__ = 'profesor'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    activo = db.Column(db.Boolean, nullable=False, server_default=expression.true())
    cursos = db.relationship('CursoModel', backref='profesor', lazy=True)

    def __init__(self, nombres: str, apellidos: str, activo: bool = None):
        self._id = None
        self.nombres = nombres
        self.apellidos = apellidos
        self.activo = activo

    def obtener_datos(self) -> dict:
        return {'id': self.id, 'nombres': self.nombres, 'apellidos': self.apellidos, 'activo': self.activo}

    @staticmethod
    def buscar_por_id(_id: int) -> 'ProfesorModel':
        return ProfesorModel.query.filter_by(id=_id).first()

    @staticmethod
    def buscar_existencia(nombres: str, apellidos: str) -> 'ProfesorModel':
        return ProfesorModel.query.filter_by(nombres=nombres).filter_by(apellidos=apellidos).first()

    def guardar(self):
        db.session.add(self)
        db.session.commit()

    def eliminar(self):
        db.session.delete(self)
        db.session.commit()
