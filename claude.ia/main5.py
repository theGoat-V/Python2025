from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import csv
import os
from datetime import datetime
import hashlib

app = FastAPI(title="Auth API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivo CSV
USERS_FILE = "users.csv"

# Inicializar CSV
def init_csv():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['email', 'password', 'created_at'])

init_csv()

# Modelos
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirmPassword: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

# Funciones de utilidad
def hash_password(password: str) -> str:
    """Hash simple de contraseña (en producción usar bcrypt)"""
    return hashlib.sha256(password.encode()).hexdigest()

def email_exists(email: str) -> bool:
    """Verifica si el email ya está registrado"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'].lower() == email.lower():
                    return True
    except:
        pass
    return False

def save_user(email: str, password: str) -> bool:
    """Guarda un nuevo usuario en CSV"""
    try:
        hashed = hash_password(password)
        with open(USERS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([email, hashed, datetime.now().isoformat()])
        return True
    except Exception as e:
        print(f"Error guardando usuario: {e}")
        return False

def verify_credentials(email: str, password: str) -> bool:
    """Verifica las credenciales del usuario"""
    try:
        hashed = hash_password(password)
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'].lower() == email.lower() and row['password'] == hashed:
                    return True
    except:
        pass
    return False

# Endpoints
@app.get("/")
def root():
    return {
        "message": "Auth API with CSV Storage",
        "version": "1.0.0",
        "endpoints": {
            "register": "/api/register",
            "login": "/api/login",
            "stats": "/api/stats"
        }
    }

@app.post("/api/register")
def register(data: RegisterRequest):
    """Registro de nuevo usuario"""
    # Validaciones
    if len(data.password) < 6:
        raise HTTPException(
            status_code=400, 
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    if data.password != data.confirmPassword:
        raise HTTPException(
            status_code=400, 
            detail="Las contraseñas no coinciden"
        )
    
    if email_exists(data.email):
        raise HTTPException(
            status_code=400, 
            detail="Este correo ya está registrado"
        )
    
    # Guardar usuario
    if save_user(data.email, data.password):
        return {
            "success": True,
            "message": "Usuario registrado exitosamente",
            "email": data.email
        }
    else:
        raise HTTPException(
            status_code=500, 
            detail="Error al registrar usuario"
        )

@app.post("/api/login")
def login(data: LoginRequest):
    """Inicio de sesión"""
    if verify_credentials(data.email, data.password):
        return {
            "success": True,
            "message": "Inicio de sesión exitoso",
            "email": data.email
        }
    else:
        raise HTTPException(
            status_code=401, 
            detail="Credenciales incorrectas"
        )

@app.get("/api/stats")
def get_stats():
    """Estadísticas del sistema"""
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            users = list(reader)
            return {
                "total_users": len(users),
                "last_registration": users[-1]['created_at'] if users else None
            }
    except:
        return {"total_users": 0, "last_registration": None}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)