from flask import Flask, render_template,request,redirect,session
from base.main import base
app = Flask(__name__)
app.secret_key = "reservation"


@app.route('/', methods=["GET", "POST"])
def index():
  return render_template('index.html')

@app.route('/client.html')
def client():
  return render_template('client.html',books_taken = base.list_taken(), all_books = base.list_all_books(), pov_client = base.client_pov(), books_not_taken=base.list_not_taken())

@app.route('/libraire.html')
def libraire():
  return render_template('libraire.html', libraire_emprunt = base.library_emprunt(), libraire_date = base.library_date(), libraire_client = base.library_client())

@app.route('/name.html', methods = ["POST"])
def name():
  session["reservation"] = request.form.getlist("reservation")
  if len(session["reservation"]) == 0:
    return redirect('client.html')
  print(session["reservation"])
  return render_template('name.html')

@app.route('/reservation.html', methods=["POST"])
def reservation():
  form = request.form
  lst_name = form.get("identifiant")
  id_user = base.sweep_name(lst_name)
  lst_title = session["reservation"]
  for title in lst_title:
    id_books = base.sweep_id(title)
    base.reservation(id_user, id_books)
  return render_template('reservation.html')




app.run(host='0.0.0.0', port=8080)