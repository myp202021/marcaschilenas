# Radar de Percepción M&P

Una aplicación de análisis automático para evaluar la percepción digital de marcas chilenas basado en menciones públicas, utilizando técnicas de web scraping, análisis de sentimiento y evaluación estadística.

## 🎯 Objetivo

El sistema permite a cualquier usuario buscar una marca chilena y obtener su percepción digital, calculada mediante:

- Scraping en vivo de medios públicos
- Clasificación de sentimiento
- Ponderación por canal
- Modelo de evaluación basado en campana de Gauss

## 🚀 Características

- **Análisis de marca en tiempo real**: Evalúa menciones en noticias, blogs y redes sociales.
- **Score de percepción**: Puntuación de 0-100 basada en distribución normal.
- **Radar de atributos**: Innovación, servicio, reputación y presencia digital.
- **Comparación competitiva**: Benchmarking contra marcas similares.
- **Recomendaciones accionables**: Insights estratégicos fundamentados estadísticamente.

## 🛠️ Tecnologías

- **Frontend**: HTML, Tailwind CSS, Chart.js
- **Backend**: Python con Flask
- **Análisis**: BeautifulSoup, SciPy
- **Deploy**: Compatible con Replit u otros servidores

## 📋 Requisitos previos

- Python 3.8+
- Pip (gestor de paquetes de Python)

## ⚙️ Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu-usuario/radar-percepcion.git
cd radar-percepcion
```

2. Crea un entorno virtual (opcional pero recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Prepara la estructura de archivos:
```
/app
  |- main.py               # Backend Flask
  |- templates/
     |- index.html         # Formulario + landing page
     |- result.html        # Panel de resultados
  |- static/
     |- css/
        |- style.css       # Estilos personalizados
     |- js/
        |- script.js       # Javascript
  |- data/
     |- top100_marcas.csv  # Ranking simulado
```

## 🚀 Uso

1. Inicia la aplicación:
```bash
python app/main.py
```

2. Accede a la aplicación en tu navegador:
```
http://localhost:8080
```

3. Completa el formulario con los datos requeridos:
   - Nombre de la marca chilena
   - Datos de contacto
   - Información empresarial

4. Recibe un análisis completo con:
   - Score de percepción
   - Distribución de sentimiento
   - Radar de atributos
   - Frases destacadas
   - Comparación con competidores
   - Recomendaciones estratégicas

## 📊 Funcionamiento

1. **Input**: El usuario ingresa una marca chilena junto con sus datos de contacto.

2. **Procesamiento**:
   - Se recolectan menciones públicas de la marca mediante scraping.
   - Se clasifica el sentimiento de cada mención.
   - Se pondera cada mención según la relevancia del medio.
   - Se calcula un score de percepción utilizando distribución normal.

3. **Output**:
   - Visualización gráfica del score y atributos.
   - Listado de menciones relevantes.
   - Recomendaciones de acción personalizadas.

## 🔄 Extensiones futuras

- Login y panel histórico.
- Integración con APIs de redes sociales.
- Comparador entre marcas.
- Score histórico por mes.
- Análisis de temas específicos.

## 📞 Contacto

- Sitio web: [www.mulleryperez.cl](https://www.mulleryperez.cl)
- WhatsApp: [+56 9 9225 8137](https://wa.me/56992258137?text=Quiero%20analizar%20mi%20marca)
- Email: contacto@mulleryperez.cl

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---
*"Aquí no opinamos, medimos. Cada mención es un dato. Cada dato, una decisión."*
