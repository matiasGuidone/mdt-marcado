from conexion.conexion import conexion
from flask import Flask, session, render_template, flash, redirect, url_for, request, jsonify, make_response
from flask import request
import json
import sys
import os
import flask
import qrcode
import base64
from entidades.personal import personal
from entidades.movimiento import movimiento
from datetime import date
from datetime import datetime


try:
    from BytesIO import BytesIO
except ImportError:
    from io import BytesIO

sys.path.append(os.getcwd())
# sys.path.append("/home/matias/.local/lib/python3.8/site-packages/")
# try:
#     from flask.ext.cors import CORS, cross_origin  # The typical way to import flask-cors
# except ImportError:
#     # Path hack allows examples to be run without installation.
#     import os
#     parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#     os.sys.path.insert(0, parentdir)

#     from flask.ext.cors import CORS, cross_origin
# from entidades.celular import celular


app = Flask(__name__)

#cors = CORS(app)
#app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def index():
    con = conexion()
    return render_template('index.html')


def random_qr():
    code = generacode()
    qr = qrcode.QRCode(version=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=20,
                       border=4)

    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image()
    return img


@app.route('/qr')
def get_qrimg():
    img_buf = BytesIO()
    img = random_qr()
    img.save(img_buf)
    img_buf.seek(0)
    img_str = base64.b64encode(img_buf.getvalue())
    img_str = str(img_str).replace(
        "b'", "data:image/png;base64,").replace("'", "")
    return render_template('qrreloj.html', qr_image=img_str)

##############MOVIMIENTOS################


@app.route("/mov", methods=["OPTIONS"])
def api_movimiento():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route("/mov", methods=['POST'])
def add_movimiento():
    data = request.get_json()
    con = conexion()
    mov = movimiento(data['fechahora'], data['tipo'],
                     data['observaciones'], data['id'], data['id'])
    con.insert(mov, 'reloj_movimientos')
    return _corsify_actual_response(jsonify({"result": "OK"}))
    pass


@app.route("/movs", methods=["OPTIONS"])
def api_movimientos():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


@app.route("/movs", methods=['POST'])
def add_movimientos():
    data = request.get_json()
    con = conexion()
    for n in data:
        mov = movimiento(n['fechahora'], n['tipo'],
                         n['observaciones'], n['id'], n['id'])
        dat = con.selectAll('reloj_movimientos', [
                            'rlm_fechahora', n['fechahora'], 'rlm_tipo', n['tipo'], 'per_id', n['id']])
        if len(dat) == 0:
            con.insert(mov, 'reloj_movimientos')

    return _corsify_actual_response(jsonify({"result": "OK"}))
    pass


@app.route("/movimientos", methods=['GET'])
# @cross_origin()
def form_movimientos():

    id = request.headers.get('id')

    if request.args.__contains__('del'):
        session['fil'] =None
        session['pag'] =None
        session['lim'] =None
        session['ord'] =None 

    if request.args.__contains__('lim'):
        session['lim'] = int(request.args['lim'])
    elif not session.get('logged_in'):
        session['lim'] = 20

    if request.args.__contains__('ord'):
        if str(session['ord']).startswith(request.args['ord']):
            if str(session['ord']).__contains__('ASC'):
                session['ord'] = request.args['ord'] + ' DESC'
            else:
                session['ord'] = request.args['ord'] + ' ASC'
        else:
            session['ord'] = request.args['ord'] + ' ASC'
    elif not session.get('ord'):
        session['ord'] = ' 1 ASC '

    if request.args.__contains__('pag'):
        session['pag'] = int(request.args['pag'])
    elif not session.get('pag'):
        session['pag'] = 0

    if request.args.__contains__('fil'):
        if not session.get('fil'):
            session['fil'] = request.args['fil']
        else:
            if session['fil'].split(";").__contains__(request.args['fil'].split(";")[0]):
                par = [] 
                par = session['fil'].split(";")
                for l in range(len(par)) :
                    if par[l] == request.args['fil'].split(";")[0]:
                        val = par[l+1]
                par = [request.args['fil'].split(";")[1] if (i==val) else i for i in par]
                session['fil'] = ";". join(par)                 
            else:
                session['fil'] += ";"+request.args['fil']
    elif not session.get('fil'):
        session['fil'] = None

    fil = None
    if session['fil'] != None:
        fil = session['fil'].split(';')
     
    try:
        if id == None:
            con = conexion()
            movimientos = con.selectMovimientos(fil)
            nropaginas = list(range(0, int(len(movimientos)/session['lim'])+1))
            movimientos = con.selectMovimientos(fil, str(
                session['pag']*session['lim']), str(session['lim']), str(session['ord']))

            return render_template('movimientos.html', listmovimientos=movimientos, cantpaginas=nropaginas)
        else:
            con = conexion()
            nropaginas = int(len(movimientos)/20)
            movimientos = con.selectAll("reloj_movimientos")
            return render_template('movimientos.html', listmovimientos=movimientos, cantpaginas=nropaginas)

        pass
    except :
        session['fil'] =None
        session['pag'] =None
        session['lim'] =None
        session['ord'] =None 
        pass
   


@app.route("/marcar", methods=['POST'])
def add_mov_reloj():
    ####validacion###
    now = datetime.now()

    # if not request.form['codigo']:
    #     flash('Debe ingresar el código')
    cod = request.form['codigo']
    con = conexion()
    per = con.selectAll('personal', ['per_codigomarcado', cod])
    msj = ""
    tipo = ""

    if request.form.__contains__('E') or request.form.__contains__('I'):

        if request.form.__contains__('E'):
            tipo = 'E'
        elif request.form.__contains__('I'):
            tipo = 'I'

        mov = movimiento(
            now, tipo, request.form['observaciones'], per[0]['id'], per[0]['id'])
        con.insert(mov, 'reloj_movimientos')
        msj = "Movimiento de "+tipo+", " + \
            per[0]['nombre']+" "+per[0]['apellido'] + \
            " - "+str(now).split('.')[0]

    else:
        if len(per) > 0:

            if per[0]['horasalidasab'] == "" and per[0]['horaentradasab'] == "" and per[0]['horaentradamat'] == "" and per[0]['horasalidamat'] == "" and per[0]['horaentradaves'] == "" and per[0]['horasalidaves'] == "":

                img_buf = BytesIO()
                img = random_qr()
                img.save(img_buf)
                img_buf.seek(0)
                img_str = base64.b64encode(img_buf.getvalue())
                img_str = str(img_str).replace(
                    "b'", "data:image/png;base64,").replace("'", "")

                return render_template('qrreloj.html', qr_image=img_str, eligeopt='true', codigo=cod, observaciones=request.form['observaciones'])

            elif now.day == 6:
                if int(per[0]['horaentradasab'].split(':')[0])-1 <= now.hour and int(per[0]['horaentradasab'].split(':')[0])+1 >= now.hour:
                    tipo = "I"
                elif int(per[0]['horasalidasab'].split(':')[0])-1 <= now.hour and int(per[0]['horasalidasab'].split(':')[0])+1 >= now.hour:
                    tipo = "E"
                else:
                    tipo = "I"
            else:
                if int(per[0]['horaentradamat'].split(':')[0])-1 <= now.hour and int(per[0]['horaentradamat'].split(':')[0])+1 >= now.hour:
                    tipo = "I"
                elif int(per[0]['horasalidamat'].split(':')[0])-1 <= now.hour and int(per[0]['horasalidamat'].split(':')[0])+1 >= now.hour:
                    tipo = "E"
                elif int(per[0]['horaentradaves'].split(':')[0])-1 <= now.hour and int(per[0]['horaentradaves'].split(':')[0])+1 >= now.hour:
                    tipo = "I"
                elif int(per[0]['horasalidaves'].split(':')[0])-1 <= now.hour and int(per[0]['horasalidaves'].split(':')[0])+1 >= now.hour:
                    tipo = "E"
                else:
                    tipo = "I"

            # n['fechahora'],n['tipo'],n['observaciones'],n['id'],n['id'] )
            mov = movimiento(
                now, tipo, request.form['observaciones'], per[0]['id'], per[0]['id'])
            con.insert(mov, 'reloj_movimientos')
            msj = "Movimiento de "+tipo+", " + \
                per[0]['nombre']+" "+per[0]['apellido'] + \
                " - "+str(now).split('.')[0]
            pass
        else:
            msj = "El código ingresado no es válido"
            pass

    style = "danger"
    if tipo == "E":
        style = "primary"
    elif tipo == "I":
        style = "success"

    img_buf = BytesIO()
    img = random_qr()
    img.save(img_buf)
    img_buf.seek(0)
    img_str = base64.b64encode(img_buf.getvalue())
    img_str = str(img_str).replace(
        "b'", "data:image/png;base64,").replace("'", "")
    return render_template('qrreloj.html', qr_image=img_str, textoalerta=msj, alertstyle=style, istext='true')


def generacode():
    dia = date.today()
    cod = ""
    d = dia.day
    m = dia.month
    a = dia.year
    cod = dia.strftime('%Y%m%d')
    cod += str(d+m+a)
    cod += str(a-m-d)
    cod += str(a*m*d)
    return "MUTUAL"+cod

##############PERSONAL################


@app.route("/personal", methods=["OPTIONS"])
def api_personal():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_prelight_response()
    else:
        raise RuntimeError(
            "Weird - don't know how to handle method {}".format(request.method))


def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response


def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/personal", methods=['POST'])
def add_personal():

    ####validacion###

    if not request.form['nombre']:
        flash('Debe ingresar Nombre')

    if not request.form['apellido']:
        flash('Debe ingresar Apellido')

    if not request.form['codigomarcado']:
        flash('Debe ingresar Codigo de marcado')

    if not request.form['legajo']:
        flash('Debe ingresar Numero de legajo')
    id = request.form['id']
    if id == None or id == '0' or id == '':
        con = conexion()
        pers = personal(p=request.form)
        con.insert(pers, 'personal')
    else:
        con = conexion()
        pers = personal(p=request.form)
        con.update(pers, 'personal')
    pass

    con = conexion()
    personales = con.selectAll("personal")
    return render_template('personal.html', listpersonal=personales)


@app.route("/personal", methods=['GET'])
# @cross_origin()
def form_personal():

    id = request.headers.get('id')
    codigo = request.headers.get('codigomdt')

    if codigo != None:

        con = conexion()
        personales = con.selectAll("personal", ["per_codigomarcado", codigo])
        return _corsify_actual_response(jsonify({"data": [personales]}))

    elif id == None:
        con = conexion()
        personales = con.selectAll("personal")
        return render_template('personal.html', listpersonal=personales)
    else:
        con = conexion()
        personales = con.selectAll("personal")
        return render_template('personal.html', listpersonal=personales)


@app.route("/personal", methods=['DELETE'])
def del_personal():

    con = conexion()
    con.delete(request.form['id'], 'personal')

    con = conexion()
    personales = con.selectAll("personal")
    return render_template('personal.html', listpersonal=personales)


if __name__ == "app":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    imagen = None
    app.run(host="http://192.168.0.125", debug=True, port=8888)
