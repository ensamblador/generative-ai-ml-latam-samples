# MIT No Attribution
#
# Copyright 2024 Amazon Web Services
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import math

from pydantic import BaseModel, Field
from typing import List

class InformacionGeneral(BaseModel):
    """Informacion general acerca de la sociedad o compañia"""
    name: str = Field("", description="El nombre de la sociedad")
    expedition_date: str = Field("", description="La fecha de registro de la sociedad")
    expedition_city: str = Field("", description="La ciudad donde la sociedad fue registrada")
    duration: str = Field("", description="La duracion de sociedad en años")
    social_object: List[str] = Field(description="Un listado de los objetivos de la sociedad")
    nationality: str = Field("", description="La nacionalidad de la sociedad. Depende de en que pais fue registrada la sociedad")
    open_to_foreigners: bool = Field(True, description="Acepta la sociedad miembros extranjeros?")
    fixed_social_capital: str = Field("", description="La cantidad total de dinero invertido en la sociedad")
    total_stock: str = Field("", description="El total de acciones de las que se conforma la sociedad")

    def to_tuples_table(self):
        """How is this object represented a set of tuples that can be printed to a PDF using the fpdf library"""

        cell_max_char = 150 # Max number of characters per cell
        temp_table = []

        social_object_txt = '\n'.join([f"{i + 1}.- {objective}" for i, objective in zip(range(len(self.social_object)), self.social_object)])

        tuples_table = (
            ("Constitución", ""),
            ("Nombre del titular", self.name),
            ("Fecha de Constitución", self.expedition_date),
            ("Domicilio Social", self.expedition_city),
            ("Duración", self.duration),
            ("Objetivos Sociales", social_object_txt[:cell_max_char]),
        )

        for i in range(1, (math.ceil(len(social_object_txt)/cell_max_char)-1)):
            temp_table.append(("", f"{i}.-" + social_object_txt[cell_max_char*i:cell_max_char*(i+1)]))

        if len(temp_table)>0:
            tuples_table += tuple(temp_table)

        tuples_table += (
            ("Nacionalidad", self.nationality),
            ("Admisión de Extranjeros", "Si" if self.open_to_foreigners else "No"),
            ("Total de capital social mínimo fijo", str(self.fixed_social_capital)),
            ("Total de números de acciones o partes sociales", str(self.total_stock))
        )

        print(tuples_table)

        return tuples_table


class InformacionAccionista(BaseModel):
    """Informacion sobre los accionistas"""
    shareholder_name: str = Field(description="Nombre del accionista")
    stock_units: str = Field(description="Numero de acciones que posee el accionista")
    stocks_value: str = Field("", description="El valor (en dinero) del las acciones que posee el accionista")


class CapitalSocial(BaseModel):
    """Informacion acerca del capital social de la sociedad"""
    shareholders: List[InformacionAccionista] = Field([], description="La lista de accionistas de la sociedad")

    def to_tuples_table(self):
        """How is this object represented a set of tuples that can be printed to a PDF using the fpdf library"""

        tuples_table = [
            ("", "Capital Social", ""),
            ("Socios", "Número de acciones o partes", "Valor")
        ]

        for stocks_info in self.shareholders:
            stocks_element = (stocks_info.shareholder_name,
                              str(stocks_info.stock_units),
                              str(stocks_info.stocks_value))
            tuples_table.append(stocks_element)

        return tuples_table


class InformacionAdministrador(BaseModel):
    """Informacion acerca de un administrado de la socidad. Un administrador es cualquier persona con poderes y facultades dentro de la sociedad y que pertenece a ella."""
    name: str = Field(description="El nombre del administrador")
    position: str = Field(description="La posicion que el administrador ostenta dentro de la sociedad")
    powers: List[str] = Field(description="Un listado de los poderes que el administrador tiene dentro de la sociedad")


class InformacionAdministracion(BaseModel):
    """Informacion acerca de la administracion de la sociedad"""
    managers: List[InformacionAdministrador] = Field([], description="Un listado con informacion acerca de cada administrador de la sociedad. Un administrador es cualquier persona que con poderes y facultades dentro de la sociedad y que pertenece a ella.")

    def to_tuples_table(self):
        """How is this object represented a set of tuples that can be printed to a PDF using the fpdf library"""

        cell_max_char = 150 # Max number of characters per cell

        tuples_table = [
            ("", "Administración", ""),
            ("Nombre", "Puesto", "Poderes"),
        ]

        for manager_info in self.managers:

            temp_table = []
            powers_list = '\n'.join([f"{i+1}.- {power}" for i, power in zip(range(len(manager_info.powers)), manager_info.powers)])

            administration_element = (
                manager_info.name,
                manager_info.position,
                powers_list[:cell_max_char]
            )

            tuples_table.append(administration_element)

            for i in range(1, (math.ceil(len(powers_list) / cell_max_char) - 1)):
                powers_row = ("", "", powers_list[cell_max_char * i:cell_max_char * (i + 1)])
                temp_table.append(powers_row)

            if len(temp_table)>0:
                tuples_table += tuple(temp_table)

        return tuples_table


class RepresentanteLegal(BaseModel):
    """Informacion acerca del representante legal de la sociedad. Un representante legal es cualquier persona que puede representar a la sociedad en un proceso legal. Usualmente es la persona con mas poderes dentro de la sociedad."""
    name: str = Field(description="El nombre del representante legal de la sociedad")
    position: str = Field(description="La posicion que el representante legal ocupa dentro de la sociedad")
    powers: List[str] = Field(description="Los poderes conferidos al representante legal dentro de la sociedad")

    def to_tuples_table(self):
        """How is this object represented a set of tuples that can be printed to a PDF using the fpdf library"""

        cell_max_char = 150  # Max number of characters per cell

        tuples_table = [
            ("", "Apoderados", ""),
            ("Nombre", "Puesto", "Poderes"),
        ]

        temp_table = []
        powers_list = '\n'.join([f"{i+1}.- {power}" for i, power in zip(range(len(self.powers)), self.powers)])

        legal_rep_element = (
            self.name,
            self.position,
            powers_list[:cell_max_char]
        )

        tuples_table.append(legal_rep_element)

        for i in range(1, (math.ceil(len(powers_list) / cell_max_char) - 1)):
            powers_row = ("", "", powers_list[cell_max_char * i:cell_max_char * (i + 1)])
            temp_table.append(powers_row)

        if len(temp_table) > 0:
            tuples_table += tuple(temp_table)

        return tuples_table


class InformacionNotario(BaseModel):
    """Informacion acerca del notario publico. El notario publico es un funcionario de gobierno que legitimiza la creacion de la sociedad"""
    notary_name: str = Field(description="El nombre del notario publico")
    document_number: str = Field(description="El numero de documento, asignado por la notaria")
    notary_number: str = Field(description="El numero del notario")
    entity_of_creation: str = Field(description="El estado en el que la sociedad es creada")

    def to_tuples_table(self):
        """How is this object represented a set of tuples that can be printed to a PDF using the fpdf library"""

        tuples_table = [
            ("", "Fedatario", "", ""),
            ("Póliza o escritura pública No.", "Nombre del fedatario", "Número del fedatario", "Estado"),
            (self.document_number, self.notary_name, self.notary_number, self.entity_of_creation)
        ]

        return tuples_table