import sys, os
sys.path.append(os.getcwd())
import mysql.connector
from entidades.encodeJson import EncodeJson 
from entidades.personal import personal 
from entidades.personalmov import personalmov 
from entidades.movimiento import movimiento 


class conexion:

    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      password="",
      database='mdt'
    )
   

    # con = sqlite3.connect("abm.db")

    def insert_case(self, argument, p): 
            if argument == "personal" : return f"INSERT INTO personal (per_nombre, per_apellido, per_nrosocio, per_codigomarcado, per_horaentradamatutino, per_horasalidamatutino, per_horaentradavespertino, per_horasalidavespertino, per_horaentradasabado, per_horasalidasabado, per_huellaid, per_legajo) VALUES ('{p.nombre}', '{p.apellido}', '{p.nrosocio}', '{p.codigomarcado}', '{p.horaentradamat}', '{p.horasalidamat}', '{p.horaentradaves}', '{p.horasalidaves}', '{p.horaentradasab}', '{p.horasalidasab}', '{p.huella}', '{p.legajo}')"
            if argument == "reloj_movimientos" : return f"INSERT INTO reloj_movimientos (rlm_fechahora, rlm_tipo, rlm_observaciones, per_id ) VALUES ('{p.fechahora}', '{p.tipo}', '{p.observaciones}', {p.per_id} )"
            pass
         
    def update_case(self, argument, p):
            if argument == "personal": return f"UPDATE personal SET per_nombre = '{p.nombre}', per_apellido = '{p.apellido}' , per_nrosocio = '{p.nrosocio}' , per_codigomarcado = '{p.codigomarcado}' , per_horaentradamatutino = '{p.horaentradamat}' , per_horasalidamatutino = '{p.horasalidamat}' , per_horaentradavespertino = '{p.horaentradaves}' , per_horasalidavespertino = '{p.horasalidaves}' , per_horaentradasabado = '{p.horaentradasab}' , per_horasalidasabado = '{p.horasalidasab}' , per_huellaid = '{p.huella}' , per_legajo = '{p.legajo}' WHERE id = {p.id} "
            pass

    def selectId_case(self, argument, id):
            return f"select * from {argument} where id = {id}"
            pass

    def delete_case(self, argument, id):
            return f"delete from {argument} where id = {id}"
            pass

    def object_case(self, argument):
            if argument == "personal": return personal
            if argument == "reloj_movimientos": return movimiento
            pass
 
     
    #consultas
    def insert(self, parameter_list, tabla):
        # self.con = sqlite3.connect("abm.db")
        self.conectar()
        cursor = self.mydb.cursor()
        cursor.execute(self.insert_case(tabla ,parameter_list))
        self.mydb.commit()
        # cur = self.con.cursor()
        # cur.execute(self.insert_case(tabla), parameter_list)
        # self.con.commit()

    def update(self, parameter_list, tabla):
        # self.con = sqlite3.connect("abm.db")
        self.conectar()
        cursor = self.mydb.cursor()
        cursor.execute(self.update_case(tabla ,parameter_list))
        self.mydb.commit()
 

    def delete(self, id, tabla): 
        # self.con = sqlite3.connect("abm.db")
        self.conectar()
        cursor = self.mydb.cursor()
        cursor.execute(self.delete_case(tabla,id))
        self.mydb.commit()

    # def selectId(self, id, tabla): 
    #     # self.con = sqlite3.connect("abm.db")
    #     cursor=self.con.execute(self.selectId_case(tabla),[id])
    #     return cursor.fetchall()

    def conectar(self):
        self.mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database='mdt'
                ) 
        pass

    def selectAll(self, tabla, condiciones = None, offset=None, limit=None): 
        #self.con = sqlite3.connect("abm.db")
        self.conectar()
        cursor = self.mydb.cursor()
        if condiciones == None :
            #cursor = self.mydb.execute("select * from "+tabla)
            consulta = "select * from "+tabla
            
            if limit != None:
                consulta += " LIMIT "+limit
                if offset != None:
                    consulta += " OFFSET "+offset


            cursor.execute(consulta)#fetchall() 

            dt = cursor.fetchall()
            lista = []
            
            for row in dt:
                lista.append(EncodeJson().default(self.object_case(tabla)(p=row)))
            pass
            return lista
        else :
            consulta = "select * from "+tabla
            consulta += " where 1 = 1 "
            for i in range(len(condiciones)):
                if i%2==0 :
                    consulta += " and "+str(condiciones[i])
                else :
                    consulta += " = '"+str(condiciones[i])+"'"

            if limit != None:
                consulta += " LIMIT "+limit
                if offset != None:
                    consulta += " OFFSET "+offset

            cursor.execute(consulta)
            dt = cursor.fetchall()
            lista = []
            for row in dt:
                lista.append(EncodeJson().default(self.object_case(tabla)(p=row)))
            pass
            return lista
    
    def getoperando(self, letra ):
        if letra == "l":
            return "like"
        if letra == "i":
            return "="
        if letra == "m":
            return ">"
        if letra == "n":
            return "<"



    def selectMovimientos(self, condiciones = None, offset=None, limit=None, orderby= None): 
        #self.con = sqlite3.connect("abm.db")
        self.conectar()
        cursor = self.mydb.cursor()
        if 1 :
            #cursor = self.mydb.execute("select * from "+tabla)
            consulta = "SELECT * FROM reloj_movimientos join personal on reloj_movimientos.per_id = personal.id "
            
            if condiciones != None :
                consulta += " where 1 = 1 "
                for i in range(len(condiciones)):
                    if i%2==0 :
                        consulta += " and "+str(condiciones[i])[1:len(str(condiciones[i]))] + " " + self.getoperando(str(condiciones[i])[0:1])
                    else :
                        consulta += " '"+str(condiciones[i])+"'"
                        
            if orderby != None:
                consulta += " ORDER BY "+orderby
                        
            if limit != None:
                consulta += " LIMIT "+limit
                if offset != None:
                    consulta += " OFFSET "+offset

            cursor.execute(consulta)#fetchall() 
            dt = cursor.fetchall()
            lista = []
            
            for row in dt:
                lista.append(EncodeJson().default(personalmov(p=row)))
            pass
            
            return lista
        