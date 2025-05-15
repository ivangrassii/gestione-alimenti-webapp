from flask import Flask, render_template, request
import json

app = Flask(__name__)

def carica_alimenti():
    with open('alimenti.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    categorie = sorted(set([a["categoria"] for a in carica_alimenti()]))
    return render_template('home.html', categorie=categorie)

@app.route('/categoria/<nome>', methods=['GET', 'POST'])
def categoria(nome):
    alimenti = [a for a in carica_alimenti() if a["categoria"] == nome]
    dose_totale = None

    if request.method == 'POST':
        rapporto_ic = float(request.form['rapporto_ic'])
        carbo_totali = 0

        for alimento in alimenti:
            qty = request.form.get(alimento['nome'])
            if qty:
                try:
                    qty = float(qty)
                    carbo_totali += qty * alimento['carboidrati_per_dose']
                except:
                    pass

        if rapporto_ic <= 20:
            dose_totale = round(carbo_totali / rapporto_ic, 1)
        else:
            dose_totale = 'Il rapporto I/C non può superare 20'

    return render_template('categoria.html', categoria=nome, alimenti=alimenti, dose=dose_totale)

//mancaif

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port)

