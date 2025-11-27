# 🔧 Solución al Error de Bcrypt y Base de Datos

## ❌ Errores Encontrados

### 1. Error de Bcrypt
```
AttributeError: module 'bcrypt' has no attribute '__about__'
password cannot be longer than 72 bytes
```

**Causa**: Incompatibilidad entre `bcrypt 5.0.0` (nueva) y `passlib 1.7.4` (antigua)

### 2. Error de Datos Duplicados
```
duplicate key value violates unique constraint
```

**Causa**: La base de datos ya tiene algunos datos parciales de intentos anteriores

## ✅ Soluciones Aplicadas

### 1. Bcrypt Corregido
Se actualizó `app/core/security.py` con:
- ✅ Configuración compatible: `bcrypt__ident="2b"`
- ✅ Validación de longitud de contraseña (máx 72 bytes)
- ✅ Documentación de funciones

### 2. Script de Reset
Se creó `reset_db.py` para limpiar la base de datos

## 🚀 Pasos para Inicializar Correctamente

### Opción 1: Reset Completo (Recomendado)

```bash
cd backend

# 1. Resetear base de datos (elimina todo)
pipenv run python reset_db.py
# Cuando pregunte, escribe: yes

# 2. Inicializar con datos por defecto
pipenv run python init_db.py
```

### Opción 2: Reset Manual con pgAdmin

1. Abrir pgAdmin: http://localhost:5051
2. Conectar a la base de datos `usuarios_db`
3. Click derecho en cada tabla → Delete/Drop
4. Ejecutar: `pipenv run python init_db.py`

### Opción 3: Recrear Contenedor Docker

```bash
# Desde la raíz del proyecto
docker-compose down -v
docker-compose up -d

# Luego inicializar
cd backend
pipenv run python init_db.py
```

## ✅ Verificación

Después de ejecutar `init_db.py`, deberías ver:

```
Database initialized successfully!
Admin user created: username='admin', password='admin123'
Regular user created: username='user', password='user123'
```

## � Tablas Creadas

- ✅ `users` - Usuarios del sistema
- ✅ `roles` - Roles (Administrador, Usuario)
- ✅ `permissions` - Permisos (12 permisos por defecto)
- ✅ `user_roles` - Relación usuarios-roles
- ✅ `role_permissions` - Relación roles-permisos
- ✅ `audit_logs` - Registro de actividad

## 🎯 Datos Iniciales

### Usuarios
| Username | Password | Rol |
|----------|----------|-----|
| admin | admin123 | Administrador |
| user | user123 | Usuario |

### Roles
- **Administrador**: Todos los permisos
- **Usuario**: Solo permisos de lectura

### Permisos (12 total)
- Usuarios: create, read, update, delete
- Roles: create, read, update, delete
- Permisos: create, read, update, delete

## 🔍 Comandos Útiles

```bash
# Ver estado de contenedores
docker-compose ps

# Ver logs de PostgreSQL
docker-compose logs usuarios_postgres

# Conectar a PostgreSQL directamente
docker exec -it usuarios_postgres psql -U admin -d usuarios_db

# Listar tablas (dentro de psql)
\dt

# Salir de psql
\q
```

## ⚠️ Notas Importantes

1. **Contraseñas por defecto**: Cambiar en producción
2. **Bcrypt límite**: Las contraseñas no pueden exceder 72 bytes
3. **Reset elimina TODO**: Usar con cuidado en producción

---

**Resumen**: 
1. Ejecuta `reset_db.py` (escribe "yes")
2. Ejecuta `init_db.py`
3. ¡Listo para usar!
