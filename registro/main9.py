from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import csv
import os
from datetime import datetime
import secrets
import hashlib

app = FastAPI(title="Sistema de Autenticación")

# CORS - Muy importante
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos CSV
USERS_FILE = "users.csv"
SESSIONS_FILE = "sessions.csv"

# Modelos
class UserRegister(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    nombre: str
    email: str
    fecha_registro: str
    token: str

# Inicializar archivos CSV
def init_csv_files():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nombre', 'email', 'password_hash', 'fecha_registro'])
        print(f"✅ {USERS_FILE} creado")
    
    if not os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['token', 'user_id', 'fecha_creacion'])
        print(f"✅ {SESSIONS_FILE} creado")

init_csv_files()

# Funciones auxiliares (SIN bcrypt, más simple)
def hash_password(password: str) -> str:
    """Hash simple con SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar contraseña"""
    return hash_password(plain_password) == hashed_password

def generate_token() -> str:
    """Generar token aleatorio"""
    return secrets.token_urlsafe(32)

def get_user_by_email(email: str):
    """Buscar usuario por email"""
    try:
        if not os.path.exists(USERS_FILE):
            return None
            
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'].lower() == email.lower():
                    return row
    except Exception as e:
        print(f"❌ Error al leer usuarios: {e}")
    return None

def save_user(user_data: dict):
    """Guardar nuevo usuario"""
    try:
        with open(USERS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                user_data['id'],
                user_data['nombre'],
                user_data['email'],
                user_data['password_hash'],
                user_data['fecha_registro']
            ])
        print(f"✅ Usuario guardado: {user_data['email']}")
        return True
    except Exception as e:
        print(f"❌ Error al guardar usuario: {e}")
        return False

def save_session(token: str, user_id: str):
    """Guardar sesión"""
    try:
        with open(SESSIONS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([token, user_id, datetime.now().isoformat()])
        print(f"✅ Sesión creada")
        return True
    except Exception as e:
        print(f"❌ Error al crear sesión: {e}")
        return False

# Endpoints
@app.get("/")
def root():
    print("✅ GET / - OK")
    return {"message": "API de Autenticación funcionando correctamente"}

@app.post("/api/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserRegister):
    print(f"\n📝 POST /api/register")
    print(f"   Nombre: {user.nombre}")
    print(f"   Email: {user.email}")
    
    try:
        # Validaciones básicas
        if len(user.nombre) < 3:
            print("❌ Nombre muy corto")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre debe tener al menos 3 caracteres"
            )
        
        if len(user.password) < 6:
            print("❌ Contraseña muy corta")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La contraseña debe tener al menos 6 caracteres"
            )
        
        # Verificar si el email ya existe
        existing_user = get_user_by_email(user.email)
        if existing_user:
            print(f"❌ Email ya registrado: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Crear nuevo usuario
        user_id = secrets.token_urlsafe(16)
        password_hash = hash_password(user.password)
        fecha_registro = datetime.now().isoformat()
        
        user_data = {
            'id': user_id,
            'nombre': user.nombre,
            'email': user.email,
            'password_hash': password_hash,
            'fecha_registro': fecha_registro
        }
        
        # Guardar usuario
        if not save_user(user_data):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al guardar usuario"
            )
        
        # Crear sesión
        token = generate_token()
        if not save_session(token, user_id):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear sesión"
            )
        
        print(f"✅ Usuario registrado exitosamente: {user.email}\n")
        
        return UserResponse(
            id=user_id,
            nombre=user.nombre,
            email=user.email,
            fecha_registro=fecha_registro,
            token=token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        print(f"   Tipo: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.post("/api/login", response_model=UserResponse)
def login(credentials: UserLogin):
    print(f"\n🔐 POST /api/login")
    print(f"   Email: {credentials.email}")
    
    try:
        # Buscar usuario
        user = get_user_by_email(credentials.email)
        
        if not user:
            print(f"❌ Usuario no encontrado")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        # Verificar contraseña
        if not verify_password(credentials.password, user['password_hash']):
            print(f"❌ Contraseña incorrecta")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        # Crear nueva sesión
        token = generate_token()
        if not save_session(token, user['id']):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al crear sesión"
            )
        
        print(f"✅ Login exitoso: {credentials.email}\n")
        
        return UserResponse(
            id=user['id'],
            nombre=user['nombre'],
            email=user['email'],
            fecha_registro=user['fecha_registro'],
            token=token
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get("/api/verify")
def verify_token(token: str):
    print(f"\n🔍 GET /api/verify")
    
    try:
        if not os.path.exists(SESSIONS_FILE):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
            
        with open(SESSIONS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['token'] == token:
                    user_id = row['user_id']
                    # Buscar el usuario
                    with open(USERS_FILE, 'r', encoding='utf-8') as uf:
                        user_reader = csv.DictReader(uf)
                        for user in user_reader:
                            if user['id'] == user_id:
                                print(f"✅ Token válido\n")
                                return {
                                    "valid": True,
                                    "user": {
                                        "id": user['id'],
                                        "nombre": user['nombre'],
                                        "email": user['email']
                                    }
                                }
        
        print(f"❌ Token no encontrado\n")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*60)
    print("🚀 SERVIDOR DE AUTENTICACIÓN")
    print("="*60)
    print("📍 URL: http://localhost:8000")
    print("📝 Documentación: http://localhost:8000/docs")
    print("🔒 CORS: Habilitado")
    print("💾 Almacenamiento: CSV (sin bcrypt)")
    print("="*60 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)