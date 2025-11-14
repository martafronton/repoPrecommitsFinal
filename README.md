# repoPrecommitsFinal
Formateo, Estilo de Código y Análisis con SonarQube
# Manual de uso y ejemplos

## 1. Ejecutar la aplicación con Docker

1. Asegúrate de tener **Docker** y **Docker Compose** instalados y en ejecución.

2. Desde la raíz del proyecto, levanta todos los servicios con:

```bash
docker-compose up -d
```

-d → ejecuta los contenedores en segundo plano

Esto levantará la app y cualquier servicio definido en el docker-compose.yml

3. Accede en tu navegador a: http://localhost:5000


4. Para detener los contenedores:
   
```bash
docker-compose down
```
Esto detiene y elimina los contenedores creados por docker-compose

No elimina las imágenes, volúmenes o datos persistentes salvo que se especifique

## 2. ¿Qué es SonarQube?
SonarQube es una plataforma de inspección continua de calidad de código que detecta bugs, vulnerabilidades, code smells, duplicación y mide métricas (complejidad, cobertura, mantenibilidad, etc).

### 2.1 Instalación rápida con Docker
Levanta el servidor:
`docker run -d --name sonarqube -p 9000:9000 sonarqube:latest`

Accede a `http://localhost:9000`. Credenciales por defecto `admin/admin`

### 2.2 Crear proyecto y token
1. En la interfaz crea un nuevo proyecto.
2. Genera un **token** (Project → Administration → Security → Generate Token).

### 2.3 Analizar el proyecto (usando Sonar Scanner CLI en Docker)
Ejecuta desde la raíz del repo:

```bash
docker run --rm \
  -e SONAR_HOST_URL="http://host.docker.internal:9000" \
  -e SONAR_TOKEN="TOKEN_GENERADO" \
  -v "${PWD}:/usr/src" \
  sonarsource/sonar-scanner-cli \
  "-Dsonar.projectKey=Key_del_proyecto" \
  "-Dsonar.sources=."
```
Tras ejecutar el análisis, los resultados estarán disponibles en http://localhost:9000



## 3. Buenas prácticas

- **Uso de ramas claras**:  
  `feature/`, `fix/`, `refactor/`, `docs/`.  
  Esto facilita revisiones y evita conflictos.  

- **Convenciones de código (Python)**:  
  - Funciones y variables → `snake_case`  
  - Clases → `PascalCase`  
  - Constantes → `MAYUSCULAS_CON_GUIONES_BAJOS`  
  - Líneas < 80 caracteres  
  - Comentarios y docstrings descriptivos  

- **Control de calidad con SonarQube**:  
  - Detecta errores, duplicados y code smells  
  - Mide cobertura y complejidad  
  - Se revisa antes de mergear a main  

- **Pre-commit hooks**:  
  - `black` → formatea automáticamente el código  
  - `pytest` → comprueba que los tests pasan
  - `commit-msg hook` → exige que los mensajes sigan el formato `feat:`, `fix:`, `chore`, etc.
  - Evita commits de archivos muy grandes  

- **GitHub Actions / CI**:  
  - Ejecuta tests y comprueba formateo en cada push/PR  
  - Analiza código automáticamente con SonarQube

## 4. Documentación Ejecicios

### 1. Ejercicio creacion de precommit hooks

Como los documentos en `.git` no se suben al proyecto hemos decidido introducir los commandos a introducir dentro
del precommit hook en este apartado.

- **Pre commit para pasar los tests**
```bash
#!/bin/sh
echo "Ejecutando pre-commit: tests con Docker..."

# Tests
echo "Ejecutando tests con pytest..."
TEST_OUTPUT=$(docker compose run --rm -T dev sh -lc 'pytest -q --disable-warnings --color=no')
TEST_EXIT=$?
echo "$TEST_OUTPUT"
if [ $TEST_EXIT -ne 0 ]; then
  echo "Algunos tests fallaron. Corrige los errores antes de commitear."
  exit 1
fi

echo "Pre-commit finalizado correctamente."
exit 0

```
- **pre commit para formatear el código**
```bash
docker compose run --rm -T dev black .
```
- **pre commit para evitar commits que contengan archivos con un tamaño demasiado grande**
```bash
#!/bin/bash

# Tamaño máximo en KB 
MAX_SIZE=102.400 #100 MB

# Busca archivos añadidos o modificados en el commit
FILES=$(git diff --cached --name-only)

for file in $FILES; do
    if [ -f "$file" ]; then
        SIZE=$(du -k "$file" | cut -f1)
        if [ "$SIZE" -gt "$MAX_SIZE" ]; then
            echo "❌ El archivo '$file' excede el tamaño máximo permitido (${MAX_SIZE} KB)."
            echo "Commit bloqueado."
            exit 1
        fi
    fi
done

echo "✅ Todos los archivos cumplen con el límite de tamaño."
exit 
```
- **pre commit para exigir un formato tipo feat:, fix:, chore:**
```bash
#!/bin/sh
# Valida que el mensaje de commit empiece con feat:, fix:, chore:, refactor:, docs:, test:

COMMIT_MSG_FILE=$1
COMMIT_MSG=$(head -n1 "$COMMIT_MSG_FILE")

if ! echo "$COMMIT_MSG" | grep -Eq '^(feat|fix|chore|refactor|docs|test):'; then
  echo "Formato de commit inválido."
  echo "El mensaje debe comenzar con uno de los siguientes prefijos:"
  echo "  feat:, fix:, chore:, refactor:, docs:, test:"
  exit 1
fi

exit 0

```

### 2. Ejercicio creacion de Convertir la aplicación en una imagen docker
- Nosotros partimos de que ya tenemmos el dockerfile hecho si en caso de no tenerlo se añadiría estos campos:
```bash

FROM python:3.11-slim

WORKDIR /app 

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python", "app.py"] #app.py se puede cambiar por el nombre de la aplicación en nuestro caso es app.py
```
- El siguiente paso, sería ejecutar este comando en el directorio raiz del proyecto
```bash
docker build -t nombre_aplicacion .
```
 
## Autores
* **Victor Albert Bat-Llosera** - [@BatlloseraDev](https://github.com/BatlloseraDev)
* **Marta Frontón** - [@martafronton](https://github.com/martafronton)




