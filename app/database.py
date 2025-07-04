from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, DDL, event, ForeignKey
from typing import Literal, Optional
import datetime
import sqlite3

def init_db(app):
  class Base(DeclarativeBase):
    pass

  db = SQLAlchemy(model_class=Base)

  """
  Tabelle
  """

  # Utenti

  class Utenti(db.Model):
    __tablename__ = 'Utenti'

    user_name: Mapped[str] = mapped_column(primary_key=True)
    password: Mapped[str]
    is_admin: Mapped[bool]

  # Mercati

  Giorno = Literal['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

  class Mercati(db.Model):
    __tablename__ = 'Mercati'

    nome: Mapped[str] = mapped_column(primary_key=True)
    giorno: Mapped[Giorno] = mapped_column(primary_key=True)
    is_evento: Mapped[bool]
    is_attuale: Mapped[Optional[bool]]

    __table_args__ = (
       CheckConstraint(
        "giorno IN ('Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica')",
        name='giorno_dominio'
      ),
      CheckConstraint(
        '(is_evento = 1 AND is_attuale IS NULL) OR (is_evento = 0 AND is_attuale IS NOT NULL)',
        name="check_is_attuale"
      ),
      CheckConstraint(
        "(is_attuale = 0 AND nome LIKE '%_old') OR (is_attuale IS NULL OR is_attuale != 0)",
        name="check_nome_old",
      )
    )

  # Corrispettivi

  class Corrispettivi(db.Model):
    __tablename__ = 'Corrispettivi'

    ts: Mapped[datetime.datetime] = mapped_column(primary_key=True)
    inserito_da: Mapped[str]
    data: Mapped[datetime.date]
    mercato: Mapped[str]
    giorno_mercato: Mapped[Giorno]
    reparto1: Mapped[Optional[float]]
    reparto2: Mapped[Optional[float]]
    reparto3: Mapped[Optional[float]]
    reparto4: Mapped[Optional[float]]
    reparto5: Mapped[Optional[float]]

    __table_args__ =(
      ForeignKeyConstraint(
        ['inserito_da'], ['Utenti.user_name']
      ),
      ForeignKeyConstraint(
        ['mercato', 'giorno_mercato'], ['Mercati.nome', 'Mercati.giorno']
      ),
      CheckConstraint(
        'data <= ts',
        name="data_futura_check"
      )
    )
  
  mercato_attuale_trigger = DDL("""
  CREATE TRIGGER IF NOT EXISTS mercato_attuale_trigger
  BEFORE INSERT ON corrispettivi
  FOR EACH ROW
  WHEN NOT EXISTS (
    SELECT * FROM mercati
    WHERE mercati.nome = NEW.mercato
      AND mercati.giorno = NEW.giorno_mercato
      AND mercati.is_evento = 0
      AND mercati.is_attuale = 1
  )
  BEGIN
    SELECT RAISE(FAIL, 'Il mercato referenziato non è attuale');
  END;
  """)

  event.listen(Corrispettivi.__table__, 'after_create', mercato_attuale_trigger)

  db.init_app(app)

  with app.app_context():
    # attiviamo il vincolo di chiave esterna che in SQLite non è attivo di default
    @event.listens_for(db.engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
      if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    with db.engine.connect() as conn:
      res = conn.execute(db.text("PRAGMA foreign_keys")).scalar()
      print("FOREIGN KEYS ATTIVI:", res)  # Deve stampare 1
    
    db.create_all()

    # popoliamo il database con dati di prova
    db.session.add_all([
      Utenti(
        user_name='Dario',
        password='pw',
        is_admin=True
      ),
      Utenti(
        user_name='Yuuki',
        password='pw',
        is_admin=False
      ),
      Mercati(
        nome='Centro',
        giorno='Sabato',
        is_evento=False,
        is_attuale=True
      ),
      Mercati(
        nome='Centro_old',
        giorno='Martedì',
        is_evento=False,
        is_attuale=False
      )
    ])
    db.session.commit()
    
  return db