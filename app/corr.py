from flask import (
    Blueprint, render_template
)
from sqlalchemy import or_
from app.database import db, Mercati
import datetime

from app.auth import login_required
from app.database import db

bp = Blueprint('corr', __name__, url_prefix='/corr')

@bp.route('/inserisci', methods=('GET', 'POST'))
@login_required
def inserisci():
  # Va castato a list perché scalars ritorna un iteratore che consuma i dati quando ci iteri sopra, quindi non posso
  # iterarci due volte senza rifare la query
  mercati = list(db.session.scalars(db.select(Mercati).where(or_(Mercati.is_attuale==True, Mercati.is_evento==True))))
  mercati_nomi = set([ mercato.nome for mercato in mercati ])
  mercati_dict = [ { 'mercato': mercato.nome, 'giorno': mercato.giorno } for mercato in mercati ]
  print(mercati_dict)
  
  return render_template('corr/inserisci.html', today=datetime.date.today(), mercati=mercati_dict, mercati_nomi=mercati_nomi)