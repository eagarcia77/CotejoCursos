# WebApp Generador de Reportes de Evaluación

Aplicación web que permite subir archivos Excel con evaluaciones de cursos, generar reportes individuales y un informe global en formato PDF, y descargarlos en un archivo ZIP.

## Estructura del Repositorio

```
.
├── backend/          # Lógica en FastAPI para procesar los reportes
│   ├── main.py
│   └── requirements.txt
└── frontend/         # Interfaz en HTML5 para subir archivo y descargar reportes
    └── index.html
```

---

## 🚀 Despliegue

### 🟦 Backend en Render

1. Sube solo la carpeta `backend/` a un nuevo repositorio GitHub.
2. Entra a [https://render.com](https://render.com) y crea un nuevo Web Service:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host=0.0.0.0 --port=10000`
3. Obtén la URL del backend (por ejemplo: `https://reportes-api.onrender.com`)

---

### 🟩 Frontend en Vercel

1. Sube solo la carpeta `frontend/` a otro repositorio GitHub.
2. Ve a [https://vercel.com](https://vercel.com) y crea un proyecto nuevo.
3. Asegúrate de que `index.html` utilice la URL correcta del backend en su `fetch()`.

---

### ✅ Alternativa Local

```bash
# Desde el directorio /backend/
pip install -r requirements.txt
uvicorn main:app --reload
```
Abre `frontend/index.html` en el navegador.

---

Desarrollado por: ✨ Tu asistente AI ✨
