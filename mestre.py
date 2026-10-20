from __future__ import annotations


class Mestre:

    def __init__(self, id_mestre: int | None, nome: str) -> None:
        self._id_mestre = id_mestre
        self._nome = nome

    @property
    def id_mestre(self) -> int | None:
        return self._id_mestre

    @id_mestre.setter
    def id_mestre(self, valor: int) -> None:
        self._id_mestre = valor

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome = valor

    def __repr__(self) -> str:
        return f"Mestre(id={self._id_mestre!r}, nome={self._nome!r})"
