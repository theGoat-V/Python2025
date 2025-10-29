from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import csv
import os
from datetime import datetime
import hashlib
import uuid

app = FastAPI(title="Sistema de Autenticación y Reservas Deportivas")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos CSV
USERS_FILE = "users.csv"
COURTS_FILE = "courts.csv"

# Modelos Pydantic
class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    created_at: str

class Court(BaseModel):
    id: str
    sport_id: str
    name: str
    status: str
    schedule: str
    available_days: str
    features: str
    price_per_hour: int

# Funciones auxiliares
def hash_password(password: str) -> str:
    """Hashea la contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_users_csv():
    """Inicializa el archivo CSV de usuarios"""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'name', 'email', 'password', 'created_at'])

def initialize_courts_csv():
    """Inicializa el archivo CSV de canchas con datos de ejemplo"""
    if not os.path.exists(COURTS_FILE):
        with open(COURTS_FILE, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'sport_id', 'name', 'status', 'schedule', 
                           'available_days', 'features', 'price_per_hour'])
            
            # Datos de ejemplo para cada deporte
            courts_data = [
                # Raquetbol
                ['r1', 'raquetbol', 'Cancha Raquetbol 1', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Cancha profesional con piso de madera', 250],
                ['r2', 'raquetbol', 'Cancha Raquetbol 2', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Cancha climatizada, iluminación LED', 280],
                ['r3', 'raquetbol', 'Cancha Raquetbol 3', 'Disponible', '8:00 AM - 8:00 PM', 'Lun-Sab', 'Cancha estándar con vestidores', 220],
                
                # Tenis
                ['t1', 'tenis', 'Cancha Tenis 1', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Superficie dura, iluminación nocturna', 350],
                ['t2', 'tenis', 'Cancha Tenis 2', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Superficie dura profesional', 350],
                ['t3', 'tenis', 'Cancha Tenis 3', 'Disponible', '7:00 AM - 9:00 PM', 'Lun-Vie', 'Superficie sintética, ideal para principiantes', 280],
                ['t4', 'tenis', 'Cancha Tenis VIP', 'Disponible', '6:00 AM - 11:00 PM', 'Lun-Dom', 'Cancha premium con gradas y equipamiento', 450],
                
                # Pádel
                ['p1', 'padel', 'Cancha Pádel 1', 'Disponible', '7:00 AM - 11:00 PM', 'Lun-Dom', 'Cancha de cristal panorámica', 320],
                ['p2', 'padel', 'Cancha Pádel 2', 'Disponible', '7:00 AM - 11:00 PM', 'Lun-Dom', 'Césped sintético premium', 320],
                ['p3', 'padel', 'Cancha Pádel 3', 'Disponible', '8:00 AM - 10:00 PM', 'Lun-Sab', 'Cancha techada con iluminación', 300],
                
                # Pickleball
                ['pk1', 'pickleball', 'Cancha Pickleball 1', 'Disponible', '6:00 AM - 9:00 PM', 'Lun-Dom', 'Cancha doble, superficie acrílica', 180],
                ['pk2', 'pickleball', 'Cancha Pickleball 2', 'Disponible', '6:00 AM - 9:00 PM', 'Lun-Dom', 'Cancha cubierta, equipamiento incluido', 200],
                ['pk3', 'pickleball', 'Cancha Pickleball 3', 'Disponible', '7:00 AM - 8:00 PM', 'Lun-Vie', 'Cancha estándar al aire libre', 150],
                
                # Voleibol
                ['v1', 'voleibol', 'Cancha Voleibol Indoor 1', 'Disponible', '6:00 AM - 11:00 PM', 'Lun-Dom', 'Piso de duela, red profesional', 400],
                ['v2', 'voleibol', 'Cancha Voleibol Indoor 2', 'Disponible', '6:00 AM - 11:00 PM', 'Lun-Dom', 'Cancha climatizada, gradas para 50 personas', 450],
                ['v3', 'voleibol', 'Cancha Voleibol Arena', 'Disponible', '8:00 AM - 8:00 PM', 'Lun-Sab', 'Cancha de arena, ideal para beach volley', 350],
                
                # Baloncesto
                ['b1', 'baloncesto', 'Cancha Baloncesto 1', 'Disponible', '6:00 AM - 11:00 PM', 'Lun-Dom', 'Cancha profesional, tableros hidráulicos', 500],
                ['b2', 'baloncesto', 'Cancha Baloncesto 2', 'Disponible', '6:00 AM - 11:00 PM', 'Lun-Dom', 'Media cancha, ideal para entrenamientos', 300],
                ['b3', 'baloncesto', 'Cancha Baloncesto Outdoor', 'Disponible', '7:00 AM - 9:00 PM', 'Lun-Dom', 'Cancha al aire libre, piso sintético', 250],
                
                # Bádminton
                ['bd1', 'badminton', 'Cancha Bádminton 1', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Cancha doble, sin corrientes de aire', 220],
                ['bd2', 'badminton', 'Cancha Bádminton 2', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Cancha individual con piso de madera', 200],
                ['bd3', 'badminton', 'Cancha Bádminton 3', 'Disponible', '7:00 AM - 9:00 PM', 'Lun-Vie', 'Cancha climatizada, iluminación óptima', 240],
                
                # Squash
                ['s1', 'squash', 'Cancha Squash 1', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Cancha de cristal profesional', 280],
                ['s2', 'squash', 'Cancha Squash 2', 'Disponible', '6:00 AM - 10:00 PM', 'Lun-Dom', 'Cancha climatizada con ventilación', 280],
                ['s3', 'squash', 'Cancha Squash 3', 'Disponible', '8:00 AM - 8:00 PM', 'Lun-Sab', 'Cancha estándar con paredes blancas', 250],
            ]
            
            for court in courts_data:
                writer.writerow(court)

def get_user_by_email(email: str) -> Optional[dict]:
    """Busca un usuario por email en el CSV"""
    if not os.path.exists(USERS_FILE):
        return None
    
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['email'].lower() == email.lower():
                return row
    return None

def save_user(user_data: dict):
    """Guarda un nuevo usuario en el CSV"""
    with open(USERS_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            user_data['id'],
            user_data['name'],
            user_data['email'],
            user_data['password'],
            user_data['created_at']
        ])

def get_courts_by_sport(sport_id: str) -> List[dict]:
    """Obtiene todas las canchas de un deporte específico"""
    if not os.path.exists(COURTS_FILE):
        return []
    
    courts = []
    with open(COURTS_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['sport_id'] == sport_id:
                courts.append({
                    'id': row['id'],
                    'sport_id': row['sport_id'],
                    'name': row['name'],
                    'status': row['status'],
                    'schedule': row['schedule'],
                    'available_days': row['available_days'],
                    'features': row['features'],
                    'price_per_hour': int(row['price_per_hour'])
                })
    return courts

# Eventos de inicio
@app.on_event("startup")
async def startup_event():
    """Inicializa los archivos CSV al arrancar la aplicación"""
    initialize_users_csv()
    initialize_courts_csv()
    print("✅ Sistema iniciado correctamente")
    print(f"📁 Archivo de usuarios: {USERS_FILE}")
    print(f"🏟️  Archivo de canchas: {COURTS_FILE}")

# Endpoints de autenticación
@app.get("/")
async def root():
    """Endpoint raíz para verificar que la API está funcionando"""
    return {
        "message": "API de Autenticación y Reservas Deportivas",
        "version": "2.0",
        "endpoints": {
            "auth": {
                "register": "/register",
                "login": "/login",
                "users": "/users"
            },
            "courts": {
                "by_sport": "/courts/{sport_id}",
                "all": "/courts"
            }
        }
    }

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister):
    """Registra un nuevo usuario"""
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ya está registrado"
        )
    
    if len(user.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña debe tener al menos 6 caracteres"
        )
    
    user_id = str(uuid.uuid4())
    hashed_password = hash_password(user.password)
    created_at = datetime.now().isoformat()
    
    user_data = {
        'id': user_id,
        'name': user.name,
        'email': user.email,
        'password': hashed_password,
        'created_at': created_at
    }
    
    save_user(user_data)
    
    return UserResponse(
        id=user_id,
        name=user.name,
        email=user.email,
        created_at=created_at
    )

@app.post("/login", response_model=UserResponse)
async def login(credentials: UserLogin):
    """Inicia sesión de un usuario"""
    user = get_user_by_email(credentials.email)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    hashed_password = hash_password(credentials.password)
    if user['password'] != hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    return UserResponse(
        id=user['id'],
        name=user['name'],
        email=user['email'],
        created_at=user['created_at']
    )

@app.get("/users")
async def get_all_users():
    """Obtiene todos los usuarios (sin contraseñas)"""
    if not os.path.exists(USERS_FILE):
        return []
    
    users = []
    with open(USERS_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append({
                'id': row['id'],
                'name': row['name'],
                'email': row['email'],
                'created_at': row['created_at']
            })
    
    return users

# Endpoints de canchas
@app.get("/courts/{sport_id}")
async def get_courts(sport_id: str):
    """Obtiene todas las canchas de un deporte específico"""
    valid_sports = ['raquetbol', 'tenis', 'padel', 'pickleball', 
                   'voleibol', 'baloncesto', 'badminton', 'squash']
    
    if sport_id not in valid_sports:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deporte no encontrado. Deportes válidos: {', '.join(valid_sports)}"
        )
    
    courts = get_courts_by_sport(sport_id)
    return courts

@app.get("/courts")
async def get_all_courts():
    """Obtiene todas las canchas disponibles"""
    if not os.path.exists(COURTS_FILE):
        return []
    
    courts = []
    with open(COURTS_FILE, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            courts.append({
                'id': row['id'],
                'sport_id': row['sport_id'],
                'name': row['name'],
                'status': row['status'],
                'schedule': row['schedule'],
                'available_days': row['available_days'],
                'features': row['features'],
                'price_per_hour': int(row['price_per_hour'])
            })
    
    return courts

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)