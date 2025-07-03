from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import CheckConstraint, ForeignKeyConstraint, DDL, event, ForeignKey
from typing import Literal, Optional
import datetime

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

  # Mercati

  Giorno = Literal['Lunedì', 'Mertedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

  class Mercati(db.Model):
    __tablename__ = 'Mercati'

    nome: Mapped[str] = mapped_column(primary_key=True)
    giorno: Mapped[Giorno] = mapped_column(primary_key=True)
    is_evento: Mapped[bool]
    is_attuale: Mapped[Optional[bool]]

    __table_args__ = (
      CheckConstraint(
        '(is_evento = 1 AND is_attuale IS NULL) OR (is_evento = 0 AND is_attuale IS NOT NULL)',
        name="check_is_attuale"
      ),
      CheckConstraint(
        "is_attuale = 0 AND nome LIKE '%_old'",
        name="check_nome_old"
      )
    )

  old_trigger = DDL("""
    CREATE TRIGGER IF NOT EXISTS trg_append_old
      AFTER UPDATE ON mercati
      FOR EACH ROW
      WHEN 
        NEW.is_attuale = 0
        AND OLD.is_attuale IS NOT 0
        AND substr(NEW.nome, -4) != '_old'
      BEGIN
        UPDATE mercati
        SET nome = nome || '_old'
        WHERE nome = NEW.nome AND giorno = NEW.giorno;
      END;
      """
  )

  event.listen(Mercati.__table__, 'after_create', old_trigger)

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
    print("say")
    db.create_all()

  return db