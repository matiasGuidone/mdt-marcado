
class personalmov:
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
    idmov = None
    fechahora = None
    tipo = None
    observaciones = None

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

    def __init__(self, p= None): 
        if p != None:
            self.id=p[4]
            self.nombre=p[5]
            self.apellido=p[6]
            self.nrosocio=p[7]
            self.codigomarcado = p[8]
            self.horaentradamat = p[9]
            self.horasalidamat = p[10]
            self.horaentradaves = p[11]
            self.horasalidaves = p[12]
            self.horaentradasab = p[13]
            self.horasalidasab = p[14]
            self.huella = p[15]
            self.legajo = p[17]
            self.idmov = p[0]
            self.fechahora = p[1]
            self.tipo = p[2]
            self.observaciones = p[3]
 

    def startCall(self):

        pass
 
    def endCall(self):

        pass
