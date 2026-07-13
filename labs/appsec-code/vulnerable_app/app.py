# -*- coding: utf-8 -*-
"""
App DELIBERADAMENTE VULNERABLE para el laboratorio de code review / SAST.
NO la despliegues: es material didáctico para encontrar y corregir fallos con
análisis estático (Semgrep/Bandit) y revisión manual. Cada función esconde al
menos una vulnerabilidad clásica. Ver SOLUCION.md tras intentarlo.
"""
import hashlib
import os
import pickle
import sqlite3
import subprocess

from flask import Flask, request

app = Flask(__name__)

# Vuln 1: secreto embebido en el código (hardcoded credential).
DB_PASSWORD = "SuperSecreta123!"
AWS_KEY = "AKIAIOSFODNN7EXAMPLE"


@app.route("/user")
def get_user():
    # Vuln 2: inyección SQL por concatenación de la entrada del usuario.
    name = request.args.get("name", "")
    conn = sqlite3.connect("app.db")
    query = "SELECT * FROM users WHERE name = '" + name + "'"
    rows = conn.execute(query).fetchall()
    return {"rows": rows}


@app.route("/ping")
def ping():
    # Vuln 3: inyección de comandos del SO (shell=True + entrada del usuario).
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.check_output("ping -c 1 " + host, shell=True)
    return out


@app.route("/hash")
def hash_password():
    # Vuln 4: algoritmo de hash débil para contraseñas (MD5, sin sal).
    pwd = request.args.get("pwd", "")
    return {"hash": hashlib.md5(pwd.encode()).hexdigest()}


@app.route("/load")
def load_object():
    # Vuln 5: deserialización insegura de datos no confiables (pickle).
    data = request.get_data()
    obj = pickle.loads(data)
    return {"loaded": str(obj)}


@app.route("/read")
def read_file():
    # Vuln 6: path traversal (la entrada llega directo a la ruta del archivo).
    filename = request.args.get("file", "notes.txt")
    with open("/var/data/" + filename) as fh:
        return fh.read()


@app.route("/calc")
def calc():
    # Vuln 7: evaluación de código arbitrario (eval sobre entrada del usuario).
    expr = request.args.get("expr", "1+1")
    return {"result": eval(expr)}


if __name__ == "__main__":
    # Vuln 8: modo debug activado en producción (expone la consola de Werkzeug).
    app.run(host="0.0.0.0", debug=True)
