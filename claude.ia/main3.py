from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import csv
import os
from datetime import datetime
from typing import Optional
import uuid

app = FastAPI()

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
PRODUCTS_FILE = "products.csv"

# Crear archivos CSV si no existen
def init_csv():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['email', 'password'])
    
    if not os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'name', 'description', 'price', 'category', 'stock', 'email', 'created_at'])

init_csv()

# Modelos Pydantic
class RegisterRequest(BaseModel):
    email: str
    password: str
    confirmPassword: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    category: str
    stock: int

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock: Optional[int] = None

# Funciones de Usuarios
def email_exists(email: str) -> bool:
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    return True
    except:
        pass
    return False

def save_user(email: str, password: str):
    try:
        with open(USERS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([email, password])
        return True
    except:
        return False

def verify_user(email: str, password: str) -> bool:
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email and row['password'] == password:
                    return True
    except:
        pass
    return False

# Funciones de Productos
def save_product(name: str, description: str, price: float, category: str, stock: int, email: str):
    try:
        product_id = str(uuid.uuid4())[:8]
        with open(PRODUCTS_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([product_id, name, description, price, category, stock, email, datetime.now().isoformat()])
        return product_id
    except:
        return None

def get_user_products(email: str):
    products = []
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    products.append(row)
    except:
        pass
    return products

def get_product_by_id(product_id: str, email: str):
    try:
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == product_id and row['email'] == email:
                    return row
    except:
        pass
    return None

def update_product(product_id: str, email: str, data: ProductUpdate):
    try:
        rows = []
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['id'] == product_id and row['email'] == email:
                    if data.name:
                        row['name'] = data.name
                    if data.description:
                        row['description'] = data.description
                    if data.price is not None:
                        row['price'] = data.price
                    if data.category:
                        row['category'] = data.category
                    if data.stock is not None:
                        row['stock'] = data.stock
                rows.append(row)
        
        with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
        return True
    except:
        return False

def delete_product(product_id: str, email: str):
    try:
        rows = []
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not (row['id'] == product_id and row['email'] == email):
                    rows.append(row)
        
        with open(PRODUCTS_FILE, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            else:
                writer = csv.writer(f)
                writer.writerow(['id', 'name', 'description', 'price', 'category', 'stock', 'email', 'created_at'])
        return True
    except:
        return False

# Endpoints de Autenticación
@app.get("/")
def read_root():
    return {"message": "API de Gestión de Productos funcionando"}

@app.post("/api/register")
def register(data: RegisterRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email y contraseña son requeridos")
    
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="La contraseña debe tener al menos 6 caracteres")
    
    if data.password != data.confirmPassword:
        raise HTTPException(status_code=400, detail="Las contraseñas no coinciden")
    
    if email_exists(data.email):
        raise HTTPException(status_code=400, detail="Este correo ya está registrado")
    
    if save_user(data.email, data.password):
        return {"message": "Usuario registrado exitosamente", "email": data.email}
    else:
        raise HTTPException(status_code=500, detail="Error al registrar el usuario")

@app.post("/api/login")
def login(data: LoginRequest):
    if not data.email or not data.password:
        raise HTTPException(status_code=400, detail="Email y contraseña son requeridos")
    
    if verify_user(data.email, data.password):
        return {"message": "Sesión iniciada exitosamente", "email": data.email}
    else:
        raise HTTPException(status_code=401, detail="Correo o contraseña incorrectos")

# Endpoints de Productos
@app.post("/api/products")
def create_product(product: ProductRequest, email: str):
    if not email:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    if not product.name or product.price <= 0 or product.stock < 0:
        raise HTTPException(status_code=400, detail="Datos inválidos")
    
    product_id = save_product(
        product.name, product.description, product.price, 
        product.category, product.stock, email
    )
    
    if product_id:
        return {"message": "Producto creado exitosamente", "id": product_id}
    else:
        raise HTTPException(status_code=500, detail="Error al crear el producto")

@app.get("/api/products")
def get_products(email: str):
    if not email:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    products = get_user_products(email)
    return {"products": products}

@app.get("/api/products/{product_id}")
def get_product(product_id: str, email: str):
    if not email:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    product = get_product_by_id(product_id, email)
    if product:
        return product
    else:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.put("/api/products/{product_id}")
def update_product_endpoint(product_id: str, data: ProductUpdate, email: str):
    if not email:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    if not get_product_by_id(product_id, email):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if update_product(product_id, email, data):
        return {"message": "Producto actualizado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al actualizar el producto")

@app.delete("/api/products/{product_id}")
def delete_product_endpoint(product_id: str, email: str):
    if not email:
        raise HTTPException(status_code=401, detail="No autorizado")
    
    if not get_product_by_id(product_id, email):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if delete_product(product_id, email):
        return {"message": "Producto eliminado exitosamente"}
    else:
        raise HTTPException(status_code=500, detail="Error al eliminar el producto")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)