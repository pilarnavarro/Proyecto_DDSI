from django.db import models

class Puesto(models.Model):
  nombre_puesto = models.CharField(max_length=40, primary_key=True)
  departamento = models.CharField(max_length=40)
  numero_de_vacantes = models.IntegerField()
  aptitudes_necesarias = models.CharField(max_length=250, blank = True, null = True)
  requisitos_puesto = models.CharField(max_length=250, blank = True, null = True)
  sueldo = models.IntegerField()

  def __str__(self):
      return self.nombre_puesto + " del departamento " + self.departamento

class Factura(models.Model):
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

    def __str__(self):
      return self.matricula


class Producto(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE,default=None)
    idProducto = models.CharField(max_length=5)
    nombre = models.CharField(max_length=10)
    cantidad = models.IntegerField()
    precio = models.IntegerField()

    def __str__(self):
        return self.nombre + " con identificador " + self.idProducto
    
    class Meta:
        unique_together = (('idProducto', 'factura'),)


class EmpleadoTrabaja(models.Model):
  idEmpleado = models.CharField(max_length=10, primary_key=True)
  nombre = models.CharField(max_length=20)
  apellidos = models.CharField(max_length=20)
  nombre_puesto = models.ForeignKey(Puesto, on_delete=models.CASCADE)
  cuenta_bancaria = models.CharField(max_length=24)
  fecha_pago = models.DateField(blank=True, null=True)
  fecha_alta = models.DateField()
  fecha_baja = models.DateField(blank=True, null=True)

  def __str__(self):
    return self.nombre + " con identificador " + self.idEmpleado


class BalanceFinanciero(models.Model):
  idBalance = models.CharField(max_length=5)
  fecha_realizacion = models.DateField("Fecha de realización")
  total_gastos = models.DecimalField(max_digits=20,decimal_places=2)
  total_ingresos = models.DecimalField(max_digits=20,decimal_places=2)
  bienes_actuales = models.DecimalField(max_digits=20,decimal_places=2)
  deudas = models.DecimalField(max_digits=20,decimal_places=2)

  def __str__(self):
    return self.idBalance

#IDBalance VARCHAR(10) REFERENCES BalanceFinanciero(IDBalance) NOT NULL,
# IDEmpleado VARCHAR(10) NOT NULL,
#  Primary KEy ( IDBalance, IDEmpleado)

class ConsultaEmpleado(models.Model):
  class Meta:
        unique_together = (('idBalance', 'idEmpleado'),)
  idBalance =  models.ForeignKey(BalanceFinanciero, on_delete=models.CASCADE)
  idEmpleado = models.ForeignKey(EmpleadoTrabaja, on_delete=models.CASCADE)

  def __str__(self):
    return "idBalance " + self.idBalance + "idEmpleado " + self.idEmpleado


#DNI VARCHAR(9) primary key references SolicitaAlquiler(dni), Nombrecliente VARCHAR(40));
class Cliente(models.Model):
    dni = models.CharField(max_length=9, primary_key=True)
    nombrecliente= models.CharField("Nombre del cliente", max_length=40)

    def __str__(self):
      return self.nombrecliente + " con identificador " + self.dni


#SolicitaAlquiler(  IDalquiler VARCHAR(5) PRIMARY KEY , ganancia REAL , precio REAL, duracion VARCHAR(34), dni VARCHAR(9) NOT NULL);
class SolicitaAlquiler(models.Model):
  idAlquiler = models.CharField(max_length=5, primary_key=True)
  ganancia = models.DecimalField(max_digits=8,decimal_places=2)
  precio = models.DecimalField(max_digits=8,decimal_places=2)
  duracion = models.IntegerField()
  cliente =  models.ForeignKey(Cliente, on_delete=models.CASCADE,default=None)

  def __str__(self):
    return self.idAlquiler + " alquilado por " + self.cliente.dni

class ConsultaAlquiler(models.Model):
  class Meta:
    unique_together = (('idAlquiler', 'idBalance'),)
  idAlquiler = models.ForeignKey(SolicitaAlquiler, on_delete=models.CASCADE) 
  idBalance = models.ForeignKey(BalanceFinanciero, on_delete=models.CASCADE) 

  def __str__(self):
    return "idAlquiler " + self.idAlquiler.idAlquiler + " idBalance " + self.idBalance.idBalance


class Contiene(models.Model):
    alquiler = models.ForeignKey(SolicitaAlquiler, primary_key=True, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)

    def __str__(self):
        return "Alquiler " + self.alquiler.idAlquiler + " con vehiculo " + self.vehiculo.matricula



class ConsultaEmpleado(models.Model):
  class Meta:
    unique_together = (('balance', 'empleado'),)
  balance =  models.ForeignKey(BalanceFinanciero, on_delete=models.CASCADE)
  empleado = models.ForeignKey(EmpleadoTrabaja, on_delete=models.CASCADE)

  def __str__(self):
    return "balance " + self.balance.idBalance + " con empleado " + self.empleado.idEmpleado


class ConsultaInformeContable(models.Model):
    informe=models.ForeignKey(InformeContable,on_delete=models.CASCADE)
    balance=models.ForeignKey(BalanceFinanciero,on_delete=models.CASCADE)
    class Meta:
      verbose_name_plural ="consultas informes contables"
      unique_together = (('informe', 'balance'),)

    def __str__(self):
        return "Informe"  + self.informe.id + " con balance " + self.balance.idBalance

class ConsultaFactura(models.Model):
    balanceFinanciero = models.ForeignKey(BalanceFinanciero, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)

    def __str__(self):
      return "BalanceFinanciero " + self.balanceFinanciero.idBalance + " con factura " + self.factura.id

    class Meta:
      verbose_name_plural ="consultas facturas"
      unique_together = (('balanceFinanciero', 'factura'),)