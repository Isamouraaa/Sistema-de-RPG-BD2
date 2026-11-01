import sqlite3

from entidades.personagem import Personagem
from entidades.jogador import Jogador


class CrudPersonagem:

    def __init__(self, conexao):
        self._conexao = conexao
        self._conexao.execute("PRAGMA foreign_keys = ON;")
        self._criarTabelas()

    def _criarTabelas(self):
        sql1 = """
            CREATE TABLE IF NOT EXISTS personagens (
                _idPersonagem   INTEGER PRIMARY KEY AUTOINCREMENT,
                _nomePersonagem VARCHAR(255) NOT NULL,
                _descricao      VARCHAR(255) NOT NULL,
                _tipo           VARCHAR(255) NOT NULL,
                _raca           VARCHAR(255) NOT NULL,
                _classe         VARCHAR(255) NOT NULL,
                _forca          INT NOT NULL,
                _inteligencia   INT NOT NULL,
                _vigor          INT NOT NULL,
                _destreza       INT NOT NULL,
                _sabedoria      INT NOT NULL,
                _iniciativa     INT NOT NULL,
                _idJogador      INT,
                _idJogo         INT,
                CONSTRAINT FK_Jogadores FOREIGN KEY (_idJogador)
                REFERENCES jogadores(_idJogador),
                CONSTRAINT FK_Jogos FOREIGN KEY (_idJogo)
                REFERENCES jogos(id_jogo)
            );
        """

        sql2 = """
            CREATE TABLE IF NOT EXISTS habilidades (
                _idHabilidade   INTEGER PRIMARY KEY AUTOINCREMENT,
                _nomeHabilidade VARCHAR(255) NOT NULL UNIQUE
            );
        """

        sql3 = """
            CREATE TABLE IF NOT EXISTS personagensHabilidades (
                _idPersonagem INT NOT NULL,
                _idHabilidade INT NOT NULL,
                PRIMARY KEY (_idPersonagem, _idHabilidade),
                CONSTRAINT fk_ph_personagem
                    FOREIGN KEY (_idPersonagem)
                    REFERENCES personagens(_idPersonagem)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE,
                CONSTRAINT fk_ph_habilidade
                    FOREIGN KEY (_idHabilidade)
                    REFERENCES habilidades(_idHabilidade)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            );
        """
        self._conexao.execute(sql1)
        self._conexao.execute(sql2)
        self._conexao.execute(sql3)
        self._conexao.commit()

    def bdCriarPersonagem(self, personagem):
        sql = """
            INSERT INTO personagens (
                _nomePersonagem, _descricao, _tipo, _raca, _classe, _forca,
                _inteligencia, _vigor, _destreza, _sabedoria, _iniciativa,
                _idJogador, _idJogo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        cursor = self._conexao.execute(
            sql,
            (
                personagem.getNomePersonagem(),
                personagem.getDescricao(),
                personagem.getTipo(),
                personagem.getRaca(),
                personagem.getClasse(),
                personagem.getForca(),
                personagem.getInteligencia(),
                personagem.getVigor(),
                personagem.getDestreza(),
                personagem.getSabedoria(),
                personagem.getIniciativa(),
                personagem.getIdJogador(),
                personagem.getIdJogo(),
            ),
        )
        self._conexao.commit()
        personagem.setIdPersonagem(cursor.lastrowid)

        for nomeHab in personagem.getHabilidades() or []:
            self.bdVincularHabilidade(personagem.getIdPersonagem(), nomeHab)

    def bdCriarHabilidade(self, nomeHabilidade):
        sql = "INSERT OR IGNORE INTO habilidades (_nomeHabilidade) VALUES (?)"
        cursor = self._conexao.execute(sql, (nomeHabilidade,))
        self._conexao.commit()

        if cursor.lastrowid:
            return cursor.lastrowid

        linha = self._conexao.execute(
            "SELECT _idHabilidade FROM habilidades WHERE _nomeHabilidade = ?",
            (nomeHabilidade,),
        ).fetchone()
        return linha[0] if linha else None

    def bdVincularHabilidade(self, idPersonagem, nomeHabilidade):
        idHabilidade = self.bdCriarHabilidade(nomeHabilidade)
        if idHabilidade is None:
            return

        sql = """
            INSERT OR IGNORE INTO personagensHabilidades (_idPersonagem, _idHabilidade)
            VALUES (?, ?)
        """
        self._conexao.execute(sql, (idPersonagem, idHabilidade))
        self._conexao.commit()

    def bdAlterarHabilidade(self, idPersonagem, habAntiga, habNova):
        linha = self._conexao.execute(
            "SELECT _idHabilidade FROM habilidades WHERE _nomeHabilidade = ?",
            (habAntiga,),
        ).fetchone()

        if linha is None:
            print("Este personagem não possui habilidades.")
            return

        idAntigo = linha[0]
        self._conexao.execute(
            """
            DELETE FROM personagensHabilidades 
            WHERE _idPersonagem = ? AND _idHabilidade = ?
            """,
            (idPersonagem, idAntigo),
        )

        idNovo = self.bdCriarHabilidade(habNova)
        self._conexao.execute(
            """
            INSERT OR IGNORE INTO personagensHabilidades (_idPersonagem, _idHabilidade)
            VALUES (?, ?)
            """,
            (idPersonagem, idNovo),
        )
        self._conexao.commit()

    def bdDeletarHabilidade(self, idPersonagem, nomeHab):
        sql = """
            DELETE FROM personagensHabilidades
            WHERE _idPersonagem = ?
              AND _idHabilidade = (
                  SELECT _idHabilidade
                  FROM habilidades
                  WHERE _nomeHabilidade = ?
              )
        """
        self._conexao.execute(sql, (idPersonagem, nomeHab))
        self._conexao.commit()

    def bdListarHabilidadesPersonagem(self, idPersonagem):
        sql = """
            SELECT habilidades._nomeHabilidade
            FROM habilidades
            JOIN personagensHabilidades 
              ON personagensHabilidades._idHabilidade = habilidades._idHabilidade
            WHERE personagensHabilidades._idPersonagem = ?
            ORDER BY habilidades._nomeHabilidade
        """
        cursor = self._conexao.execute(sql, (idPersonagem,))
        return [hab[0] for hab in cursor.fetchall()]

    def bdEditarPersonagem(self, idPersonagem, personagem):
        sql = """
            UPDATE personagens SET
                _nomePersonagem = ?,
                _descricao = ?,
                _tipo = ?,
                _raca = ?,
                _classe = ?,
                _forca = ?,
                _inteligencia = ?,
                _vigor = ?,
                _destreza = ?,
                _sabedoria = ?,
                _iniciativa = ?,
                _idJogo = ?
            WHERE _idPersonagem = ?
        """
        self._conexao.execute(
            sql,
            (
                personagem.getNomePersonagem(),
                personagem.getDescricao(),
                personagem.getTipo(),
                personagem.getRaca(),
                personagem.getClasse(),
                personagem.getForca(),
                personagem.getInteligencia(),
                personagem.getVigor(),
                personagem.getDestreza(),
                personagem.getSabedoria(),
                personagem.getIniciativa(),
                personagem.getIdJogo(),
                idPersonagem,
            ),
        )
        self._conexao.commit()

    def bdExcluirPersonagem(self, idPersonagem):
        sql = "DELETE FROM personagens WHERE _idPersonagem = ?"
        self._conexao.execute(sql, (idPersonagem,))
        self._conexao.commit()

    def bdListarTodosPersonagens(self):
        sql = """
            SELECT _idPersonagem, _nomePersonagem
            FROM personagens
            ORDER BY _idPersonagem
        """
        return self._conexao.execute(sql).fetchall()

    def bdObterPersonagem(self, idPersonagem):
        sql = """
            SELECT _idPersonagem, _nomePersonagem, _descricao, _tipo, _raca, _classe,
                   _forca, _inteligencia, _vigor, _destreza, _sabedoria, _iniciativa, _idJogador, _idJogo
            FROM personagens
            WHERE _idPersonagem = ?
        """
        linha = self._conexao.execute(sql, (idPersonagem,)).fetchone()
        if linha is None:
            return None
        return self._linhaParaPersonagem(linha)

    def _linhaParaPersonagem(self, linha):
        idPersonagem = linha[0]
        return Personagem(
            idPersonagem=idPersonagem,
            nomePersonagem=linha[1],
            descricao=linha[2],
            tipo=linha[3],
            raca=linha[4],
            classe=linha[5],
            forca=linha[6],
            inteligencia=linha[7],
            vigor=linha[8],
            destreza=linha[9],
            sabedoria=linha[10],
            iniciativa=linha[11],
            habilidades=self.bdListarHabilidadesPersonagem(idPersonagem),
            idJogador=linha[12],
            idJogo=linha[13] if len(linha) > 13 else None,
        )

    def bdListarPersonagensPorJogador(self, idJogador):
        sql = """
            SELECT _idPersonagem, _nomePersonagem
            FROM personagens
            WHERE _idJogador = ?
            ORDER BY _nomePersonagem
        """
        return self._conexao.execute(sql, (idJogador,)).fetchall()
