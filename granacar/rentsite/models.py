from django.db import models

class Puesto(models.Model):
  nombre_puesto = models.CharField(max_length=40, primary_key=True)
  departamento = models.CharField(max_length=40)
  numero_de_vacantes = models.IntegerField()
  aptitudes_necesarias = models.CharField(max_length=250, blank = True, null = True)
  requisitos_puesto = models.CharField(max_length=250, blank = True, null = True)
  sueldo = models.IntegerField()

class Factura(models.Model):
    #Hay que fijar en el formulario que la longitud mínima sea tmb 5, el id siempre tiene longitud 5
    id=models.CharField(max_length=5, primary_key=True)
    fecha=models.DateField()
    proveedor=models.CharField(max_length=50,blank=True,null=True)
    total=models.DecimalField("Precio total",max_digits=5,decimal_places=2)

    def __str__(self):
        return "Factura " + self.id + " con fecha " + '{}'.format(self.fecha)


class InformeContable(models.Model):
    id=models.CharField(max_length=5, primary_key=True)
    fecha=models.DateField("Fecha de realización del informe")

    def __str__(self):
        return "Informe " + self.id + " con fecha " + '{}'.format(self.fecha)

    class Meta:
	    verbose_name_plural ="InformesContables"

class Bien(models.Model):
    id=models.CharField(max_length=5, primary_key=True)
    nombre=models.CharField(max_length=50)
    descripcion=models.TextField(blank=True,max_length=200,null=True)
    valor=models.DecimalField(max_digits=8,decimal_places=2)
    informe=models.ForeignKey(InformeContable,on_delete=models.CASCADE,default=None)

    def __str__(self):
        return self.nombre + " con identificador " + self.id

    class Meta:
	    verbose_name_plural ="bienes"

# class ConsultaInformeContable(models.Model):
#     informe=models.ForeignKey(InformeContable,primary_key=True,on_delete=models.CASCADE)
#     balance=models.ForeignKey(BalanceFinanciero,on_delete=models.CASCADE)   
#         class Meta:
# 	        verbose_name_plural ="consultas informes contables"
#             unique_together = (('informe', 'balance'),)
class Vehiculo(models.Model):
    matricula = models.CharField(max_length=9, primary_key = True)
    numero_pasajeros = models.IntegerField()
    combustible = models.CharField(max_length=30)
    trasmision = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30)

    DISPONIBLE = 'Disponible'
    NO_DISPONIBLE = 'No disponible'
    TALLER = 'En taller'

    OPCIONES = [(DISPONIBLE, 'Entregado'),(NO_DISPONIBLE, 'No disponible'),(TALLER, 'En taller')]

    estado = models.CharField(choices=OPCIONES, max_length=30, default=DISPONIBLE)

    NECESARIO = 'Necesario'
    NO_NECESARIO = 'No necesario'

    OPCIONES = [
		(NECESARIO, 'Necesario'),
		(NO_NECESARIO, 'No necesario')
	]

    mantenimiento = models.CharField(choices=OPCIONES, max_length=30, default=DISPONIBLE)
    situacion = models.CharField(max_length=100)


class Producto(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE,default=None)
    idProducto = models.IntegerField()
    nombre = models.CharField(max_length=10)
    cantidad = models.IntegerField()
    precio = models.IntegerField()


class EmpleadoTrabaja(models.Model):
  idEmpleado = models.CharField(max_length=10, primary_key=True)
  nombre = models.CharField(max_length=20)
  apellidos = models.CharField(max_length=20)
  nombre_puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
  cuenta_bancaria = models.CharField(max_length=24)
  fecha_pago = models.DateField()
  fecha_alta = models.DateField()
  fecha_baja = models.DateField(blank=True, null=True)


class BalanceFinanciero(models.Model):
  idBalance = models.CharField(max_length=10)
  fecha_realizacion = models.DateField()
  total_gastos = models.DecimalField(max_digits=20,decimal_places=2)
  total_ingresos = models.DecimalField(max_digits=20,decimal_places=2)
  bienes_actuales = models.DecimalField(max_digits=20,decimal_places=2)
  deudas = models.DecimalField(max_digits=20,decimal_places=2)





"""
class ConsultaEmpleado(models.Model):
  class Meta:
        unique_together = (('balance', 'empleado'),)
  balance =  models.ForeignKey(BalanceFinanciero, on_delete=models.CASCADE)
  empleado = models.ForeignKey(EmpleadoTrabaja, on_delete=models.CASCADE)


class ConsultaInformeContable(models.Model):
    informe=models.ForeignKey(InformeContable,primary_key=True,on_delete=models.CASCADE)
    balance=models.ForeignKey(BalanceFinanciero,on_delete=models.CASCADE)   
        class Meta:
	        verbose_name_plural ="consultas informes contables"
            unique_together = (('informe', 'balance'),)


class Contiene(models.Model):
    alquiler = models.ForeignKey(SolicitaAlquiler, primary_key=True)
    vehiculo = models.ForeignKey(Vehiculo)

class ConsultaFactura(models.Model):
    balanceFinaciero = models.ForeignKey(BalanceFinanciero, primary_key=True)
    factura = models.ForeignKey(Factura)
"""

