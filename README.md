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
('Introduce aquí el comando')
```
- **pre commit para formatear el código**
```bash
('Introduce aquí el comando')
```
- **pre commit para evitar commits que contengan archivos con un tamaño demasiado grande**
```bash
('Introduce aquí el comando')
```
- **pre commit para exigir un formato tipo feat:, fix:, chore:**
```bash
('Introduce aquí el comando')
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




