import argparse
import secrets
import string
import sys
import os
import re

# --- LÓGICA DE EVALUACIÓN ---
def evaluar_seguridad(password):
    puntuacion = 0
    
    # 1. Longitud
    longitud = len(password)
    if longitud >= 16: puntuacion += 4
    elif longitud >= 12: puntuacion += 3
    elif longitud >= 8: puntuacion += 1

    # 2. Variedad (Usando Regex)
    pool = 0
    if re.search(r"[a-z]", password): 
        puntuacion += 1.5
        pool += 26
    if re.search(r"[A-Z]", password): 
        puntuacion += 1.5
        pool += 26
    if re.search(r"\d", password):    
        puntuacion += 1.5
        pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>+=\-_/]", password): 
        puntuacion += 1.5
        pool += 32

    puntuacion = min(10, int(puntuacion))

    # 3. Tiempo de Fuerza Bruta (Estimación)
    # Combinaciones = pool ^ longitud
    if pool > 0:
        combinaciones = pool ** longitud
        segundos = combinaciones / 1e11 # 100 mil millones de intentos/seg
        
        if segundos < 1: tiempo = "Instantáneo"
        elif segundos < 3600: tiempo = f"{int(segundos/60)} minutos"
        elif segundos < 86400: tiempo = f"{int(segundos/3600)} horas"
        elif segundos < 31536000: tiempo = f"{int(segundos/86400)} días"
        else: tiempo = f"{int(segundos/31536000):,} años"
    else:
        tiempo = "Desconocido"

    return puntuacion, tiempo

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

# --- INTERFAZ ---
def main():
    parser = argparse.ArgumentParser(
        description="🛡️  NanoPass-CLI: Generador seguro de contraseñas.",
        epilog="Ejemplo: python3 generador.py -l 16 -m -n -s",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    config = parser.add_argument_group('CONFIGURACIÓN')
    config.add_argument("-l", "--long", type=int, default=12, metavar="LONG", help="Longitud (default: 12)")
    config.add_argument("-m", "--mayusculas", action="store_true", help="Incluir mayúsculas")
    config.add_argument("-n", "--numeros", action="store_true", help="Incluir números")
    config.add_argument("-s", "--simbolos", action="store_true", help="Incluir símbolos")

    salida = parser.add_argument_group('EXPORTAR RESULTADOS')
    salida.add_argument("-e", "--exportar", type=str, metavar="ARCHIVO", help="Guardar en archivo")

    args = parser.parse_args()

    # Validación de seguridad
    if args.long == 0:
        print("\n\033[1;31m[!] Error de capa 8: Amigo, una contraseña de 0 caracteres no protege nada. 😂\033[0m")
        sys.exit(1)
    
    if args.long < 12:
        print(f"\n\033[1;33m[!] Aviso: {args.long} caracteres es muy poco para NanoPass-CLI.")
        print("[*] Ajustando al mínimo de seguridad: 12 caracteres.\033[0m")
        args.long = 12

    # Ejecución
    password = generar_password(args.long, args.mayusculas, args.numeros, args.simbolos)
    score, tiempo = evaluar_seguridad(password)
    
    # Colores para el score
    color_score = "\033[1;92m" if score >= 8 else "\033[1;93m" if score >= 5 else "\033[1;91m"

    print("\n" + "─" * 50)
    print(f"🔑 CONTRASEÑA:  \033[1;97m{password}\033[0m")
    print(f"📊 SEGURIDAD:   {color_score}{score}/10\033[0m")
    print(f"⏳ TIEMPO CRACK: {tiempo} (aprox.)")
    print("─" * 50 + "\n")

    if args.exportar:
        exportar_a_archivo(args.exportar, password)

if __name__ == "__main__":
    main()
