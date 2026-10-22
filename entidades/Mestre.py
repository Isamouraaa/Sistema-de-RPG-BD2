class Mestre:
    def __init__(self, id_mestre: int | None = None, nome: str = "") -> None:
        self.id_mestre = id_mestre
        self.nome = nome

    def getId(self) -> int | None:
        return self.id_mestre

    def getNome(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"Mestre(id={self.id_mestre!r}, nome={self.nome!r})"
