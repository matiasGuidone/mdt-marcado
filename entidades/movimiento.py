class movimiento:
    id = None
    fechahora = None
    tipo = None
    observaciones = None
    per_id = None
 
    def __init__(self,fechahora = None ,tipo = None ,observaciones = None ,per_id = None, id = None, p= None): 
        if p != None:
            self.id=p[0]
            self.fechahora=p[1]
            self.tipo=p[2]
            self.observaciones=p[3]
            self.per_id = p[4]
          

        else: 
            self.id=id
            self.fechahora=fechahora
            self.tipo=tipo
            self.observaciones=observaciones
            self.per_id = per_id
 

    def startCall(self):

        pass
 
    def endCall(self):

        pass
