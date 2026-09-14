
import os, sqlite3, csv, io
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, abort

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
DB = os.environ.get("DATABASE_PATH", "cadastros.db")
ADMIN_PASSWORD = os.environ["ADMIN_PASSWORD"]

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    con.execute("""CREATE TABLE IF NOT EXISTS inscritos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        criado_em TEXT NOT NULL
    )""")
    con.commit()
    con.close()

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("login"))
        return fn(*args, **kwargs)
    return wrapper

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        cpf = request.form.get("cpf", "").strip()
        email = request.form.get("email", "").strip().lower()
        aceitou = request.form.get("aceitou")
        if not nome or not cpf or not email or not aceitou:
            flash("Preencha todos os campos e aceite os termos.", "error")
            return redirect(url_for("index"))
        try:
            con = db()
            con.execute("INSERT INTO inscritos (nome, cpf, email, criado_em) VALUES (?, ?, ?, ?)",
                        (nome, cpf, email, datetime.now().isoformat(timespec="seconds")))
            con.commit()
            con.close()
            flash("Inscrição realizada com sucesso!", "success")
        except sqlite3.IntegrityError:
            flash("Este CPF já possui uma inscrição.", "error")
        return redirect(url_for("index"))
    return render_template("index.html")

@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("Senha incorreta.", "error")
    return render_template("login.html")

@app.route("/admin/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin")
@admin_required
def admin():
    con = db()
    inscritos = con.execute("SELECT * FROM inscritos ORDER BY id DESC").fetchall()
    total = con.execute("SELECT COUNT(*) FROM inscritos").fetchone()[0]
    con.close()
    return render_template("admin.html", inscritos=inscritos, total=total)

@app.route("/admin/exportar.csv")
@admin_required
def exportar():
    con = db()
    rows = con.execute("SELECT id, nome, cpf, email, criado_em FROM inscritos ORDER BY id DESC").fetchall()
    con.close()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Nome", "CPF", "E-mail", "Data da inscrição"])
    writer.writerows([tuple(r) for r in rows])
    data = io.BytesIO(output.getvalue().encode("utf-8-sig"))
    return send_file(data, mimetype="text/csv", as_attachment=True, download_name="inscritos.csv")

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=5000, debug=False)
