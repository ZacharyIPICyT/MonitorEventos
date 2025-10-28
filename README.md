# 🐭 Video Event Monitor

Una aplicación para monitorear y analizar eventos de comportamiento en videos, diseñada específicamente para estudios etológicos con roedores.

## 📋 Características

- **🎬 Control de reproducción**: Reproduce videos a diferentes velocidades (0.125x a 8x)
- **⌨️ Registro de eventos**: Asigna teclas personalizadas para diferentes comportamientos
- **📊 Exportación de datos**: Genera archivos CSV y reportes detallados en TXT
- **🐭 Organización por sujeto**: Crea carpetas automáticamente para cada ID de ratón
- **⏱️ Precisión temporal**: Registra tiempos exactos del video, independientemente de pausas

## 🚀 Instalación

### Opción 1: Ejecutable de Windows (Recomendado)

1. Ve a la sección [Releases](https://github.com/ZachayIPICyT/MonitorsEventos/releases)
2. Descarga el archivo `VideoEventMonitor.exe` más reciente
3. Ejecuta el archivo directamente - **no requiere instalación de Python**

### Opción 2: Desde código fuente

```bash
# Clonar el repositorio
git clone https://github.com/ZacharyIPICyT/MonitorEvemtos.git
cd video-event-monitor

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python main.py
```

## 📦 Dependencias

- Python 3.8+
- OpenCV-Python
- Pandas
- NumPy

## 🎮 Cómo usar

### Configuración inicial

1. **Ingresa la ruta del video** a analizar
2. **Introduce el ID del ratón** (ej: "Raton_001")
3. **Configura las teclas** para cada comportamiento:
   - Acicalamiento
   - Exploración en pared
   - Exploración en arena
   - Interacción con objeto nuevo
   - Interacción con objeto control

### Controles durante la reproducción

| Tecla | Función |
|-------|---------|
| `Espacio` | Pausar/Reanudar video |
| `+` | Aumentar velocidad |
| `-` | Disminuir velocidad |
| `1` | Velocidad normal (1x) |
| `2` | Velocidad rápida (0.5x) |
| `3` | Velocidad muy rápida (0.25x) |
| `.` | Velocidad lenta (0.5x) |
| `r` | Reiniciar evento actual |
| `s` | Guardar progreso |
| `q` | Salir y guardar |

### Registro de eventos

- **Activar evento**: Presiona la tecla asignada al comportamiento
- **Desactivar evento**: Presiona cualquier otra tecla
- **Solo un evento activo** a la vez
- **Los controles especiales** no desactivan eventos

## 📁 Estructura de archivos generados

```
Carpeta_del_proyecto/
├── VideoEventMonitor.exe
├── Raton_001/                          ← Carpeta por ID de ratón
│   ├── Raton_001_20231215_143022_video1.csv
│   └── Raton_001_15-12-2023.txt
└── Raton_002/
    ├── Raton_002_20231215_150155_video2.csv
    └── Raton_002_15-12-2023.txt
```

### Formatos de archivo

- **CSV**: Datos tabulares con todos los eventos registrados
- **TXT**: Reporte detallado con estadísticas y resúmenes

## 🔧 Desarrollo

### Build desde código fuente

```bash
# Instalar PyInstaller
pip install pyinstaller

# Crear ejecutable
pyinstaller --onefile --console --name="VideoEventMonitor" main.py
```

### Build automático con GitHub Actions

El repositorio incluye un workflow que genera automáticamente el ejecutable cuando:
- Se crea un nuevo release
- Se hace push de un tag `v*`
- Se ejecuta manualmente desde GitHub Actions

## 📊 Salida de datos

### Archivo CSV
```csv
mouse_id,evento,inicio,fin,duracion,evento_numero
Raton_001,Acicalamiento,120.50,145.25,24.75,1
Raton_001,Exploración en pared,180.00,195.50,15.50,1
```

### Reporte TXT
```
INFORME DE ANÁLISIS DE COMPORTAMIENTO
========================================

INFORMACIÓN GENERAL
----------------------------------------
ID del animal: Raton_001
Fecha de la prueba: 15/12/2023
Video analizado: video_prueba.mp4
Duración total del video: 600.00 segundos

RESUMEN DE COMPORTAMIENTOS
----------------------------------------
Acicalamiento:
  Tiempo total: 85.25s
  Frecuencia: 3 interacciones
```

## 🐛 Reportar problemas

Si encuentras algún error o tienes sugerencias:

1. Ve a la pestaña [Issues](https://github.com/ZacharyIPICyT/MonitorEventos/issues)
2. Crea un nuevo issue
3. Describe el problema incluyendo:
   - Versión del sistema operativo
   - Pasos para reproducir el error
   - Mensajes de error (si los hay)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📞 Contacto

Tu Nombre - [marco.moreno@ipicyt.edu.mx](marco.zach.moreno@gmail.com)

Link del proyecto: [https://github.com/ZacharyIPICyT/MonitorEventos](https://github.com/ZacharyIPICyT/MonitorEventos)

---

**¡Importante**: Esta herramienta está diseñada para investigación científica. Verifica siempre la calibración temporal y valida los datos generados según los protocolos de tu institución.
