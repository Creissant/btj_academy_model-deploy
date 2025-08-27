# FastAPI Deployment Practice
Proyek ini adalah latihan dasar **deployment dengan FastAPI**. 
Tujuan utama adalah memahami cara membuat environment terisolasi, mengelola konfigurasi dengan `.env`, 
dan menjalankan API sederhana yang nantinya bisa dikembangkan untuk deployment model *Machine Learning*.

## Setup Project
1. Clone this repo.
    ```bash
    git clone <repo_url>
    cd <repo_name>
    ```
2. Buat virtual environment.
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
3. Install depedencies yang dibutuhkan
    ```bash
    pip install -r requirements.txt
4. Buat file `.env` sesuai kebutuhan.
5. Jalankan program (**server backend**) dengan kode berikut:
    ```bash
    fastapi dev main.py
    ```
    atau dengan uvicorn

    ```bash
    uvicorn main:app --reload
    ```
6. Jalankan program (**server frontend**) dengan kode berikut:
    ```bash
    streamlit run frontend/app.py
    ```
7. Jalankan program (**server model machine learning**) dengan kode berikut:
    ```bash
    mlflow server --host [host ip] --port [port]
    ```
8. training model di MLflow dengan kode berikut:
    ```bash
    python mlflow/train/train_pipeline.py
    ```

## Tambahan (Best Practice)
Lakukan hal ini setelah anda menyelesaikan projek dan ingin publish di Github:
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
- `GET /` → Hello World.
- `GET /env` → Info environment (expose password/DB hanya untuk testing didalam development).
- `GET /items/{item_id}` → Return item by ID.
- `POST /items/` → Create item (mengirim data dalam JSON body).
- `POST /predict/titanic/v1` → Melakukan prediksi penumpang titanic selamat atau tidak berdasarkan model lokal.
- `POST /predict/titanic/v2` → Melakukan prediksi penumpang titanic selamat atau tidak berdasarkan model dari MLflow.

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
btj_academy_model-deploy/
├── api/
│   ├── predict/
│   ├── schema.py # Pydantic models for request/response
│   ├── service.py # Business logic / model inference
│   └── views.py # Endpoint FastAPI (router)
│
├── models/
│   └── titanic_model.pkl # Serialized ML model (not included)
│
├── frontend/
│   ├── api/
│   │   └── prediction.py # helper request to backend
│   └── app.py # index frontend with streamlit
│
├── mlflow/
│   ├── load_model/
│   │   └── load_model.py # Load model from MLflow model registry
│   ├── train/
│   │   └── train_pipeline.py # training model ML script with logging to MLflow
│
├── venv/ # Virtual environment
│
├── .env.development # Environment config (development)
├── .env.production # Environment config (production)
├── .env.staging # Environment config (staging)
├── .gitignore # Ignore rules for git
├── main.py # Entry point FastAPI app
├── README.md # Project documentation
└── requirements.txt # Python dependencies
```