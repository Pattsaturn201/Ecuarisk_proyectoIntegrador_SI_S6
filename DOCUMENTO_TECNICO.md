# Documento de Respaldo Técnico - Ecuarisk

## 1. Diagrama de Arquitectura del Sistema

El sistema sigue una arquitectura Modelo-Vista-Controlador (MVC) adaptada a servicios, desacoplando la lógica de negocio de las rutas de la API.

```mermaid
graph TD
    Client[Cliente Web (Navegador)] <-->|HTTP/JSON| FlaskApp[Servidor Flask]
    
    subgraph "Backend (Python/Flask)"
        FlaskApp --> Routes[Rutas / Blueprints]
        Routes --> Services[Capa de Servicios]
        Services --> Models[Modelos / Validaciones]
        Services --> Config[Configuración DB]
    end
    
    subgraph "Persistencia"
        Config <-->|PyMongo Driver| MongoDB[(MongoDB Atlas)]
    end
    
    subgraph "Frontend"
        HTML[Plantillas HTML5]
        CSS[Estilos CSS3 Premium]
        JS[JavaScript Vanilla / Fetch API]
    end
    
    Routes -->|Renderiza| HTML
    JS <-->|API Calls| Routes
```

## 2. Desarrollo y Herramientas

### Metodología de Desarrollo
Se utilizó una metodología ágil iterativa, dividiendo el proyecto en módulos funcionales (Activos, Riesgos, Tratamiento, Residual, Comunicación). El backend se construyó con **Flask** para exponer una API RESTful y servir vistas, mientras que el frontend consume estos servicios de manera asíncrona para una experiencia de usuario fluida sin recargas constantes.

### Herramientas Utilizadas
*   **Lenguaje**: Python 3.x
*   **Framework Web**: Flask (Microframework ligero y flexible).
*   **Base de Datos**: MongoDB Atlas (NoSQL) para manejo flexible de esquemas JSON.
*   **Driver DB**: PyMongo.
*   **Frontend**: HTML5, CSS3 (Diseño responsivo "Dark Mode"), JavaScript (ES6+).
*   **Control de Versiones**: Git.
*   **Entorno Virtual**: venv.

## 3. Funcionamiento del Sistema (Capturas)

> *Nota: Inserte aquí las capturas de pantalla de su sistema en funcionamiento.*

**Figura 1: Dashboard Principal**
![Captura del Dashboard - Vista general de los módulos]

**Figura 2: Inventario de Activos**
![Captura de Activos - Tabla con valoración de confidencialidad, integridad y disponibilidad]

**Figura 3: Matriz de Riesgos y Tratamiento**
![Captura de Riesgos - Evaluación de impacto/probabilidad y selección de controles ISO]

**Figura 4: Reporte Integral**
![Captura del Reporte - Vista consolidada y botón de descarga]

## 4. Conclusiones
1.  **Centralización de la Información**: El sistema permite unificar el inventario de activos y la gestión de riesgos en una sola plataforma, eliminando el uso de hojas de cálculo dispersas.
2.  **Automatización de Cálculos**: La evaluación automática del riesgo inherente y residual reduce errores humanos y estandariza los criterios de clasificación (Bajo, Medio, Alto, Crítico).
3.  **Cumplimiento Normativo**: La estructura alineada con ISO 27001/27002 facilita futuras auditorías y certificaciones de seguridad.
4.  **Escalabilidad**: El uso de MongoDB permite agregar nuevos campos a los activos o riesgos sin necesidad de migraciones complejas de base de datos.
5.  **Experiencia de Usuario**: La interfaz moderna y el feedback inmediato (alertas, validaciones) mejoran la adopción de la herramienta por parte del personal.

## 5. Recomendaciones
1.  **Implementación de Autenticación**: Para un entorno productivo, se recomienda añadir un módulo de Login/Registro con roles (Admin, Auditor, Usuario) utilizando `Flask-Login` y `JWT`.
2.  **Backup Automático**: Configurar tareas programadas para realizar copias de seguridad periódicas de la base de datos de MongoDB.
3.  **Dashboard Gráfico**: Implementar librerías como `Chart.js` para visualizar estadísticas de riesgos en tiempo real (ej. % de riesgos críticos vs tratados).
4.  **Despliegue en Nube**: Migrar el servidor de desarrollo a una plataforma como Heroku, AWS o Google Cloud Run para acceso remoto seguro.
5.  **Logs de Auditoría**: Registrar quién hizo qué cambio (creación, edición, eliminación) para mantener un rastro de auditoría completo.
