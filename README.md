# FastAPI Deployment Practice
Proyek ini adalah latihan dasar **deployment dengan FastAPI**. 
Tujuan utama adalah memahami cara membuat environment terisolasi, mengelola konfigurasi dengan `.env`, 
dan menjalankan API sederhana yang nantinya bisa dikembangkan untuk deployment model *Machine Learning*.

## Setup Project
1. Clone repo.
2. Buat virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
3. Install depedencies yang dibutuhkan
    ```bash
    pip install -r requirements.txt
4. Buat file `.env` sesuai kebutuhan.
5. Jalankan program (server) dengan kode berikut:
    ```bash
    fastapi dev main.py
    ```
    atau dengan uvicorn

    ```bash
    uvicorn main:app --reload
    ```

## Tambahan (Best Practice)
- Buat `requirements.txt`
    ```bash
    pip freeze > requirements.txt
    ```
- Tambahkan `.gitignore` sesuai kebutuhan
    ```bash
    venv/
    __pycache__/
    .env*
    ```

## Endpoints
- `GET /` → Hello World
- `GET /test` → Info environment (expose password/DB hanya untuk testing didalam development)
- `GET /items/{item_id}` → Return item by ID
- `POST /items/` → Create item (mengirim data dalam JSON body)

## Contoh `.env.development`
```env
ENV=development
DEBUG=True

DB_USER=user
DB_PASSWORD=password
DB_NAME=name
DB_HOST=host
DB_PORT=port
DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}
```

## Project Structure
```
├── main.py
├── requirements.txt
├── .env.development
├── .env.production
├── .env.staging
├── .gitignore
├── README.md
└── venv/
```