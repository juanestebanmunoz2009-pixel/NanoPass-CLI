# NanoPass-CLI 🛡️
Generador de contraseñas seguro hecho en python.

**NanoPass-CLI** es una herramienta de línea de comandos potente y ligera escrita en Python, diseñada para generar contraseñas de alta seguridad y evaluar su resistencia contra ataques de fuerza bruta.

## ✨ Características

- 🚀 **Generación Instantánea:** Crea contraseñas seguras con un solo comando.
- 📊 **Evaluador de Seguridad:** Calcula una puntuación del 1 al 10 basada en la entropía de la clave.
- ⏳ **Estimador de Crackeo:** Muestra cuánto tiempo tardaría una GPU moderna en descifrar tu clave.
- 🛡️ **Validación Inteligente:** No permite contraseñas menores a 12 caracteres (Estándar NanoPass).
- 📂 **Exportación Segura:** Guarda tus contraseñas en archivos `.txt` o `.log` con limpieza automática de caracteres prohibidos.
- 🎨 **Interfaz Colorida:** Salida visual clara y organizada en la terminal.

## 🚀 Instalación

Asegúrate de tener Python 3 instalado en tu sistema.

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/juanestebanmunoz2009-pixel/NanoPass-CLI.git](https://github.com/juanestebanmunoz2009-pixel/NanoPass-CLI.git)


2. Entra a la carpeta: cd NanoPass-CLI

##🛠️ Uso: python3 generador.py [OPCIONES]

   Argumentos disponibles:

     -l, --long: Longitud de la contraseña (mínimo 12).

     -m, --mayusculas: Incluir letras mayúsculas.

     -n, --numeros: Incluir números.

     -s, --simbolos: Incluir símbolos especiales.

     -e, --exportar: Nombre del archivo para guardar el resultado.

##Ejemplo:

     python3 generador.py -l 16 -m -n -s -e mis_claves.txt

🧠¿Cómo funciona la seguridad?

NanoPass-CLI utiliza la fórmula de combinaciones exponenciales:
Combinaciones = Pool de caracteres ^ Longitud

El estimador de tiempo asume un ataque de 100 mil millones de intentos por segundo, simulando hardware de ataque profesional.

Hecho con ❤️  por ElCaucano
