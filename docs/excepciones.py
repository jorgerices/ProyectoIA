'''
try: intentar, pudiera causar error
except: si sucede ese error, haz X
raise: lanza explícitamente una excepción
finally: ejecuta SIEMPRE sin importar si hubo o no excepción
else: lo que se va a ejecutar si NO hubo ningún error
'''

try:
    x = 10
    y = 0
    resultado = x / y
except ZeroDivisionError:
    print("Error: No se puede dividir por cero.")

try:
    numero = int("hola")
    print(numero)
except ValueError:
    print("Error: No se puede convertir a entero.")

texto = "Hola clase!"
num = 22
try:
    frase = texto + str(num)
except TypeError:
    print("Error: No se puede concatenar una cadena con un número.")

try:
    frutas = ["manzana", "banana", "naranja"]
    print(frutas[5])
except IndexError:
    print("Error: Índice fuera de rango.")

try:
    estudiante = {
        "nombre": "Juan",
        "edad": 20
    }
    print(estudiante["email"])
except KeyError:
    print("Error: La clave no existe en el diccionario.")

def dividir():
    try:
        num1 = int(input("Ingrese el primer número: "))
        num2 = int(input("Ingrese el segundo número: "))
        resultado = num1 / num2
        print(f"El resultado de la división es: {resultado}")
    except ValueError:
        print("Error: Por favor, ingrese números enteros.")
    except ZeroDivisionError:
        print("Error: No se puede dividir por cero.")
    except Exception as error: #Atrapa errores de manera general, error tendrá los detalles de la excepción
        print(f"Error inesperado: {error}")
    finally:
        print("Gracias por usar la función de división.")
dividir()

try:
    bebidas = ["agua", "jugo", "refresco"]
    bebida_deseada = input("Ingrese el nombre de la bebida que desea: ")
    if bebida_deseada not in bebidas:
        raise ValueError("La bebida ingresada no está disponible.") #raise -> levantando una excepción
    else:
        print(f"Disfrute su {bebida_deseada}!")
except ValueError as error:
    print(f"Error: {error}")