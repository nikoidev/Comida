# 🚀 Guía de Inicio Rápido - Post Mejoras

## Instalación Completa

### 1. Clonar e Instalar Dependencias

```bash
# Clonar repositorio
git clone <tu-repo>
cd Comida

# Instalar dependencias backend
cd backend
pipenv install --dev

# Instalar dependencias frontend
cd ../frontend
npm install
```

### 2. Configurar Variables de Entorno

```bash
# Backend
cd backend
cp .env.example .env

# Editar .env con tus valores
# IMPORTANTE: Cambiar SECRET_KEY y SECRET_KEY_ENCRYPTION
```

### 3. Iniciar Base de Datos

```bash
# Desde la raíz del proyecto
docker-compose up -d

# Verificar que esté corriendo
docker-compose ps
```

### 4. Inicializar Base de Datos

```bash
cd backend

# Ejecutar migraciones
pipenv run python migrate_to_v2.py

# Cargar datos iniciales
pipenv run python init_db.py
```

### 5. Ejecutar Tests (Opcional pero Recomendado)

```bash
# Backend tests
cd backend
pipenv run pytest --cov=app

# Verificar que todo pase ✅
```

### 6. Iniciar Aplicación

```bash
# Terminal 1: Backend
cd backend
pipenv run python run.py

# Terminal 2: Frontend
cd frontend
npm run build
npm run start
```

### 7. Acceder a la Aplicación

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050

---

## Credenciales por Defecto

```
Admin:
  Usuario: admin
  Contraseña: admin123

Usuario Regular:
  Usuario: user
  Contraseña: user123
```

⚠️ **Cambiar en producción!**

---

## Verificar Instalación

### Health Check
```bash
curl http://localhost:8000/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "version": "2.0.0"
}
```

### Ver Logs
```bash
# Logs de aplicación
tail -f backend/logs/app.log

# Logs de errores
tail -f backend/logs/error.log
```

---

## Comandos Útiles

### Backend
```bash
# Ejecutar tests
pipenv run pytest

# Con coverage
pipenv run pytest --cov=app --cov-report=html

# Linting
pipenv run flake8 app/

# Formateo
pipenv run black app/

# Iniciar servidor desarrollo
pipenv run python run.py
```

### Frontend
```bash
# Desarrollo (hot reload)
npm run dev

# Build producción
npm run build

# Iniciar producción
npm run start

# Linting
npm run lint
```

### Docker
```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down

# Reiniciar servicios
docker-compose restart
```

---

## Troubleshooting

### Error: "Database connection failed"
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps

# Reiniciar PostgreSQL
docker-compose restart usuarios_postgres
```

### Error: "Port already in use"
```bash
# Backend (puerto 8000)
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Frontend (puerto 3000)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Error: "Module not found"
```bash
# Backend
cd backend
pipenv install

# Frontend
cd frontend
npm install
```

---

## Próximos Pasos

1. ✅ Cambiar credenciales por defecto
2. ✅ Configurar SMTP para emails
3. ✅ Revisar variables de entorno
4. ✅ Ejecutar tests
5. ✅ Explorar la aplicación
6. ✅ Leer documentación completa en README.md

---

## Recursos

- 📖 [README.md](README.md) - Documentación completa
- 🧪 [TESTING_GUIDE.md](TESTING_GUIDE.md) - Guía de testing
- 📋 [FASE2_IMPLEMENTADA.md](FASE2_IMPLEMENTADA.md) - Features Fase 2
- 🎯 [implementation_plan.md](.gemini/antigravity/brain/.../implementation_plan.md) - Mejoras Fase 3

---

**¿Problemas?** Abre un issue en GitHub o consulta la documentación.
