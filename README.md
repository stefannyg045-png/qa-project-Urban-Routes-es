# QA Project: Urban Routes (Sprint 9)

## Descripción del proyecto
Suite de pruebas automatizadas End-to-End (E2E) para el flujo de solicitud de taxi en **Urban Routes**, cubriendo la configuración de ruta, selección de tarifa **Comfort**, verificación telefónica vía SMS, registro de tarjeta de crédito, comentario para el conductor, selección de extras (manta y pañuelos, y helados), confirmación del pedido y visualización de la información del conductor asignado.

## Tecnologías y técnicas utilizadas
* **Lenguaje y entorno**: Python 3.13.17 con entorno virtual (`.venv`).
* **Automatización y testing**: Selenium WebDriver (4.53.0) y `pytest`.
* **Patrón de diseño**: Page Object Model (POM) separando localizadores y acciones de página en `main.py` y los datos/configuración en `data.py`.
* **Sincronización y captura**: esperas explícitas con `WebDriverWait` y `expected_conditions`, manejo de desplazamientos (`scrollIntoView`) y lectura de logs de rendimiento de Chrome (`goog:loggingPrefs`) para obtener el código de confirmación telefónica.

## Requisitos previos
1. Tener Google Chrome instalado.
2. Activar el entorno virtual y asegurarse de tener instaladas las dependencias:
   ```bash
   pip install selenium pytest