from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from app.database import db, Mercati
from app.auth import login_required, admin_required

bp = Blueprint('mercati', __name__, url_prefix='/mercati')

@login_required
@admin_required
@bp.route('/visualizza', methods=('GET', 'POST'))
def visualizza():
  mercati = db.session.scalars(db.select(Mercati).order_by(Mercati.nome))
  return render_template('mercati.html', mercati=mercati)