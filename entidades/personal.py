
class personal:
    id = None
    nombre = None
    apellido = None
    nrosocio = None
    codigomarcado = None
    horaentradamat = None
    horasalidamat = None
    horaentradaves = None
    horasalidaves = None
    horaentradasab = None
    horasalidasab = None
    huella = None
    legajo = None
    

    # `per_nombre`, 
    #             `per_apellido`, 
    #             `per_nrosocio`, 
    #             `per_codigomarcado`, 
    #             `per_horaentradamatutino`,
    #              `per_horasalidamatutino`, 
    #              `per_horaentradavespertino`, 
    #              `per_horasalidavespertino`, 
    #              `per_horaentradasabado`, 
    #              `per_horasalidasabado`, 
    #              `per_huellaid`, 
    #              `id`, 
    #              `per_legajo`

    def __init__(self,nombre = None,apellido= None,nrosocio = None,codigomarcado = None,horaentradamat = None, horasalidamat = None, horaentradaves = None, horasalidaves = None, horaentradasab = None, horasalidasab = None, huella = None, id = None, legajo = None, p= None): 
        if p != None:
            try:
                self.id=p[11]
                self.nombre=p[0]
                self.apellido=p[1]
                self.nrosocio=p[2]
                self.codigomarcado = p[3]
                self.horaentradamat = p[4]
                self.horasalidamat = p[5]
                self.horaentradaves = p[6]
                self.horasalidaves = p[7]
                self.horaentradasab = p[8]
                self.horasalidasab = p[9]
                self.huella = p[10]
                self.legajo = p[12]
            except:
                self.id=p['id']
                self.nombre=p['nombre']
                self.apellido=p['apellido']
                self.nrosocio=p['nrosocio']
                self.codigomarcado = p['codigomarcado']
                self.horaentradamat = p['horaentradamat']
                self.horasalidamat = p['horasalidamat']
                self.horaentradaves = p['horaentradaves']
                self.horasalidaves = p['horasalidaves']
                self.horaentradasab = p['horaentradasab']
                self.horasalidasab = p['horasalidasab']
                self.huella = p['huella']
                self.legajo = p['legajo']
                pass
             
        else: 
            self.id=id
            self.nombre=nombre
            self.apellido=apellido
            self.nrosocio=nrosocio
            self.codigomarcado = codigomarcado
            self.horaentradamat = horaentradamat
            self.horasalidamat = horasalidamat
            self.horaentradaves = horaentradaves
            self.horasalidaves = horasalidaves
            self.horaentradasab = horaentradasab
            self.horasalidasab = horasalidasab
            self.huella = huella
            self.legajo = legajo
 

    def startCall(self):

        pass
 
    def endCall(self):

        pass
