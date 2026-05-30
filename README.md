# math-to-braille

&nbsp;

## 1. Cómo arrancar

### 1.1. Crear entorno virtual e instalar dependencias
> python -m venv venv

> source venv/bin/activate          # Windows: venv\Scripts\activate

> pip install -r requirements.txt

### 1.2. Instalar dependencia de sistema (solo una vez. No se incluye en requirements.txt)
> sudo apt install libmagic1

### 1.3. Arrancar el servidor
> uvicorn app.main:app --reload

### 1.4. Verificar que funciona
> http://localhost:8000/health  → {"status":"ok"}

> http://localhost:8000/docs    → Swagger UI 

### 1.5. Correr los tests
> pytest tests/

&nbsp;

## 2. Funcionalidades actuales

Backend expone 2 endpoints:

**GET /health** — devuelve {"status": "ok"}

**POST /api/ocr** — recibe una imagen, valida que el MIME sea real (PNG, JPEG, TIFF o PDF), y llama a pix2tex para extraer LaTeX