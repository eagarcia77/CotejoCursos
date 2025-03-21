from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
import shutil
from fpdf import FPDF
import matplotlib.pyplot as plt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "reportes"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", style='B', size=12)
        self.cell(200, 10, "Universidad Interamericana de Puerto Rico", ln=True, align="C")
        self.cell(200, 10, "Recinto de Guayama", ln=True, align="C")
        self.cell(200, 10, "Centro de Informática, Telecomunicaciones y Educación en Línea", ln=True, align="C")
        self.ln(10)

@app.post("/generar-reportes/")
async def generar_reportes(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)

    data = pd.read_excel(file_location, sheet_name="Sheet1")
    temp_dir = os.path.join(OUTPUT_DIR, os.path.splitext(file.filename)[0])
    os.makedirs(temp_dir, exist_ok=True)

    for _, row in data.iterrows():
        profesor = row['Nombre del Profesor']
        curso = row['Curso']
        seccion = row['Sección ']
        termino = row['Término Académico']
        fecha = row['Fecha de la Evaluación']
        comentario = str(row["Comentarios Adicionales"]) if pd.notnull(row["Comentarios Adicionales"]) else ""

        pdf = PDF()
        pdf.set_auto_page_break(auto=False)
        pdf.add_page()
        pdf.set_font("Arial", size=10)

        pdf.cell(0, 6, f"Profesor: {profesor}", ln=True)
        pdf.cell(0, 6, f"Curso: {curso} - Sección: {seccion}", ln=True)
        pdf.cell(0, 6, f"Término: {termino}", ln=True)
        pdf.cell(0, 6, f"Fecha de Evaluación: {fecha}", ln=True)
        pdf.ln(6)

        pdf.set_font("Arial", style='B', size=10)
        pdf.cell(0, 6, "Criterios de Evaluación", ln=True)
        pdf.set_font("Arial", size=9)

        col_crit = 140
        col_res = 40

        pdf.cell(col_crit, 6, "Criterio", border=1, align="C")
        pdf.cell(col_res, 6, "Resultado", border=1, align="C")
        pdf.ln()

        for col in data.columns[5:-1]:
            resultado = row[col]
            y_before = pdf.get_y()
            pdf.multi_cell(col_crit, 5, col, border=1, align="L")
            y_after = pdf.get_y()
            pdf.set_xy(pdf.l_margin + col_crit, y_before)
            pdf.cell(col_res, y_after - y_before, resultado, border=1, align="C")
            pdf.ln(y_after - y_before)

        pdf.ln(3)
        pdf.set_font("Arial", style='B', size=10)
        pdf.cell(0, 6, "Comentarios Adicionales:", ln=True)
        pdf.set_font("Arial", size=9)
        pdf.multi_cell(0, 5, comentario)

        pdf_path = os.path.join(temp_dir, f"Reporte_{curso.replace(' ', '_')}_{seccion}.pdf")
        pdf.output(pdf_path)

    zip_path = shutil.make_archive(temp_dir, 'zip', temp_dir)
    return FileResponse(zip_path, filename=os.path.basename(zip_path), media_type='application/zip')
