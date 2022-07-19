class Client():
    def __init__(self, id_cliente, nombre_cl, rut_cl, cumpleaños_cl, fecha_registro, telefono_casa, telefono_movil, telefono_trabajo,correo_cl, facebook_cl, derivado, direccion_cl, referencias_direc, notas_cl="") -> None:
        self.id_cliente = id_cliente
        self.nombre_cl = nombre_cl
        self.rut_cl = rut_cl
        self.cumpleaños_cl = cumpleaños_cl
        self.fecha_registro = fecha_registro
        self.telefono_casa = telefono_casa
        self.telefono_movil = telefono_movil
        self.telefono_trabajo = telefono_trabajo
        self.correo_cl = correo_cl
        self.facebook_cl = facebook_cl
        self.derivado = derivado
        self.direccion_cl = direccion_cl
        self.referencias_direc = referencias_direc
        self.notas_cl = notas_cl
