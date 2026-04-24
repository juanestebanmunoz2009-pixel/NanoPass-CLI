import argparse
import secrets
import string
import sys
import os

# --- LÓGICA DE GENERACIÓN ---
def generar_password(longitud, usar_mayus, usar_nums, usar_simbolos):
    caracteres = string.ascii_lowercase
    if usar_mayus: caracteres += string.ascii_uppercase
    if usar_nums: caracteres += string.digits
    if usar_simbolos: caracteres += string.punctuation
    
    return ''.join(secrets.choice(caracteres) for _ in range(longitud))

# --- REGULACIÓN DE SEGURIDAD ---
def validar_nombre_archivo(nombre):
    nombre_sucio = os.path.basename(nombre)
    nombre_base, ext = os.path.splitext(nombre_sucio)
    
    ext_seguras = ['.txt', '.log']
    if ext.lower() not in ext_seguras:
        print(f"\033[1;33m[!] Regulación: La extensión '{ext}' no es permitida. Cambiando a .txt\033[0m")
        ext = ".txt"
    
    prohibidos = '<>:"/\\|?*'
    for char in prohibidos:
        nombre_base = nombre_base.replace(char, "")

    if not nombre_base: nombre_base = "password"
    return nombre_base + ext

def exportar_a_archivo(nombre_usuario, password):
    nombre_final = validar_nombre_archivo(nombre_usuario)
    try:
        with open(nombre_final, "w") as f:
            f.write(f"Tu contraseña segura es: {password}\n")
        print(f"\033[1;32m[+] Éxito: Contraseña exportada a {nombre_final}\033[0m")
    except Exception as e:
        print(f"\033[1;31m[-] Error al escribir: {e}\033[0m", file=sys.stderr)

# --- INTERFAZ ESTILO SHERLOCK ---
def main():
    # El ArgumentParser ahora tiene un epílogo con ejemplos, como Sherlock
    parser = argparse.ArgumentParser(
        description="🛡️  Generador de contraseñas By ElCaucano hecho con amor.",
        epilog="Ejemplo: python3 generador.py -l 16 -m -n -s -e claves.txt",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # GRUPO 1: Configuración de la clave
    config = parser.add_argument_group('CONFIGURACIÓN')
    config.add_argument("-l", "--long", type=int, default=12, metavar="LONG", help="Longitud de la contraseña (default: 12)")
    config.add_argument("-m", "--mayusculas", action="store_true", help="Incluir letras mayúsculas")
    config.add_argument("-n", "--numeros", action="store_true", help="Incluir números")
    config.add_argument("-s", "--simbolos", action="store_true", help="Incluir símbolos especiales")

    # GRUPO 2: Opciones de guardado
    salida = parser.add_argument_group('EXPORTAR RESULTADOS')
    salida.add_argument("-e", "--exportar", type=str, metavar="ARCHIVO", help="Nombre del archivo donde se guardará")

    args = parser.parse_args()

    # Ejecución
    password = generar_password(args.long, args.mayusculas, args.numeros, args.simbolos)
    
    # Imprimimos el resultado con un formato visual más atractivo
    print("\n" + "─" * 45)
    print(f"🔑 TU CONTRASEÑA:  \033[1;92m{password}\033[0m") # Verde brillante
    print("─" * 45 + "\n")

    if args.exportar:
        exportar_a_archivo(args.exportar, password)

if __name__ == "__main__":
    main()
