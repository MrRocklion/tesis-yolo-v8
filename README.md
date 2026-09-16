# Sistema de reconocimiento de pictogramas y generación de narrativas

Aplicación gráfica para Raspberry Pi 5 que combina visión por computador y generación de lenguaje natural. El sistema guía al usuario por una selección de nombre, género, edad y estado de ánimo; captura imágenes de una cámara, detecta un pictograma con un modelo YOLOv8 en formato ONNX y consulta servicios externos para clasificarlo, generar una narrativa breve y producir audio. La narrativa y sus parámetros se almacenan en Firebase.

El proyecto está orientado a generar explicaciones sencillas y contextualizadas para infantes con Trastorno del Espectro Autista (TEA). No es una herramienta de diagnóstico ni sustituye el criterio de profesionales de salud o educación.

## Requisitos

Se recomienda una Raspberry Pi 5 con cámara o webcam, conexión a Internet, salida de audio y **Raspberry Pi OS Bookworm de 64 bits con escritorio**. La edición con escritorio es necesaria para mostrar la interfaz PySide6. Instale el sistema con Raspberry Pi Imager seleccionando `Raspberry Pi OS (64-bit)` basado en Bookworm.

El proyecto también requiere:

- Python 3 y soporte para entornos virtuales.
- Git.
- `mpg123` para reproducir los archivos MP3 generados.
- Credenciales válidas de OpenAI, Ultralytics y Firebase.
- El modelo local `models/best.onnx`, incluido en este repositorio.

## Instalación

### 1. Instalar Git, Python y las dependencias del sistema

Actualice el índice de paquetes e instale Git:

```bash
sudo apt update
sudo apt install -y git
git --version
```

Python suele venir instalado en Raspberry Pi OS. Si el módulo `venv` no está incluido, instálelo junto con las demás dependencias básicas:

```bash
sudo apt install -y python3 python3-venv python3-pip mpg123 libgl1
python3 --version
```

El usuario que ejecuta la aplicación debe tener acceso a la cámara. Normalmente el usuario inicial de Raspberry Pi OS ya pertenece al grupo `video`. Puede comprobarlo con `groups`.

### 2. Descargar el proyecto

```bash
git clone URL_DEL_REPOSITORIO tesis-yolo-v8
cd tesis-yolo-v8
```

Reemplace `URL_DEL_REPOSITORIO` por la dirección Git del repositorio.

### 3. Crear el entorno virtual fuera del proyecto

La estructura esperada es la siguiente:

```text
carpeta-de-trabajo/
├── env/
└── tesis-yolo-v8/
```

Desde la carpeta que contiene el proyecto, cree el entorno llamado `env`:

```bash
cd ..
python3 -m venv env
```

Actívelo e instale el archivo `requirements.txt`:

```bash
source env/bin/activate
python -m pip install --upgrade pip
python -m pip install -r tesis-yolo-v8/requirements.txt
```

`requirements.txt` es una lista de paquetes y versiones requeridas. El comando anterior hace que `pip` lea esa lista e instale las dependencias dentro del entorno virtual, sin modificar la instalación global de Python.

### 4. Configurar las credenciales

Entre en el proyecto y cree `.env` a partir de la plantilla:

```bash
cd tesis-yolo-v8
cp .env.example .env
nano .env
```

Complete todos los valores de `.env`:

- `OPENAI_API_KEY`: clave de la API de OpenAI.
- `ULTRALYTICS_API_KEY`: clave de la API de inferencia de Ultralytics.
- `ULTRALYTICS_MODEL_URL`: URL del modelo alojado en Ultralytics HUB.
- Variables de Firebase: datos del JSON de una cuenta de servicio. Mantenga la clave privada entre comillas y sus saltos como `\n`.

No comparta ni suba `.env` al repositorio. El archivo ya está ignorado por Git; `.env.example` contiene únicamente valores de muestra.

Si alguna clave real estuvo previamente escrita en el código o publicada en Git, debe revocarse y generarse de nuevo en el servicio correspondiente.

## Ejecutar la aplicación manualmente

Con el entorno creado fuera del proyecto:

```bash
cd /ruta/a/carpeta-de-trabajo
source env/bin/activate
cd tesis-yolo-v8
python main.py
```

Para salir del entorno al terminar:

```bash
deactivate
```

## Ejecutar con `script.sh`

El archivo `script.sh` localiza el proyecto, activa automáticamente `../env/bin/activate` y ejecuta `python main.py`. Dé permiso de ejecución una sola vez:

```bash
cd /ruta/a/carpeta-de-trabajo/tesis-yolo-v8
chmod +x script.sh
./script.sh
```

Puede abrirlo con doble clic desde el escritorio si el administrador de archivos está configurado para ejecutar scripts. Para un inicio automático más confiable use systemd.

## Inicio automático con systemd

Como la aplicación tiene interfaz gráfica, el servicio debe iniciarse cuando esté disponible el escritorio. Cree un servicio de usuario (sin `sudo`) y reemplace `/home/pi` si su usuario o ruta son diferentes:

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/tesis-yolo-v8.service
```

Contenido del archivo:

```ini
[Unit]
Description=Sistema de reconocimiento de pictogramas YOLOv8
After=graphical-session.target network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=/home/pi/tesis-yolo-v8
ExecStart=/home/pi/tesis-yolo-v8/script.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=graphical-session.target
```

Active y pruebe el servicio desde una terminal abierta en la sesión gráfica:

```bash
systemctl --user daemon-reload
systemctl --user enable --now tesis-yolo-v8.service
systemctl --user status tesis-yolo-v8.service
```

Para consultar los mensajes de la aplicación:

```bash
journalctl --user -u tesis-yolo-v8.service -f
```

Para detener y desactivar el inicio automático:

```bash
systemctl --user disable --now tesis-yolo-v8.service
```

Si la interfaz no aparece al arrancar, compruebe que Raspberry Pi OS inicia sesión en el escritorio automáticamente y que las rutas `WorkingDirectory` y `ExecStart` coinciden con la ubicación real.

## Funcionamiento general

El flujo principal es:

1. El usuario inicia una sesión desde el menú.
2. Selecciona género, edad y estado de ánimo.
3. La cámara muestra video en tiempo real y el modelo ONNX local detecta un pictograma.
4. Tras mantener una detección con suficiente confianza, se guarda temporalmente el recorte de la imagen.
5. La API de Ultralytics identifica el contenido del pictograma.
6. OpenAI genera una explicación breve con los parámetros seleccionados y crea su audio.
7. El resultado se presenta en pantalla y los datos de la interacción se guardan en Firebase.

El uso de OpenAI, Ultralytics y Firebase requiere Internet y puede generar costos según las condiciones de cada proveedor.

## Vistas de la interfaz

- **Ajustes:** permite registrar el nombre que se usará para personalizar la explicación.
- **Menú:** ofrece iniciar, abrir ajustes o salir.
- **Género:** permite seleccionar niño o niña.
- **Edad:** presenta opciones entre 6 y 13 años.
- **Estado de ánimo:** permite elegir contento, enojado, triste, aburrido o relajado.
- **Captura:** muestra la cámara y ejecuta la detección local del pictograma.
- **Carga:** procesa las consultas a los servicios externos sin bloquear la interfaz.
- **Resultado:** muestra la narrativa, reproduce el audio y permite reintentar o volver al menú.

## Estructura del proyecto

```text
tesis-yolo-v8/
├── main.py                 # Entrada de la aplicación y navegación entre vistas
├── script.sh               # Activación del entorno y arranque
├── requirements.txt        # Dependencias de Python
├── .env.example            # Plantilla de configuración sin secretos
├── controllers/            # Estado compartido y comunicación entre vistas
├── screens/                # Pantallas de la interfaz gráfica
├── widgets/                # Botones y componentes visuales reutilizables
├── yolov8/                 # Inferencia y utilidades del modelo ONNX
├── models/best.onnx        # Modelo local de detección de pictogramas
├── icons/                  # Recursos gráficos
└── test/                   # Scripts y datos auxiliares de evaluación
```

Durante la ejecución se crean `target.jpg` y la carpeta `audio/`; ambos están excluidos de Git.

## Autoría

Este proyecto fue creado por **Joan David Encarnacion Diaz**.

- Correo: [david.diaz190799@gmail.com](mailto:david.diaz190799@gmail.com)
- Sitio web: [www.mecdevs.com](https://www.mecdevs.com)
