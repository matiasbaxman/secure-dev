# Informe EV3 – OCY1102 – SecureDev Tickets
Alumno: ______  Repositorio: ______  Fecha: ______

## 1. Arquitectura del pipeline
(Captura: Jenkins Stage View. Etapas: Checkout → Build → Test → SAST+Dependencias → Deploy → OWASP ZAP)

## 2. Revisiones de seguridad y vulnerabilidades (IL 3.1 / 3.4)
| # | Vulnerabilidad | Archivo / línea | Riesgo | Cómo se detectó | Corrección aplicada | Commit | Estado |
|---|---|---|---|---|---|---|---|
| 1 | SQL Injection | app.py /search | Alto | Revisión de código + test | Consulta parametrizada | | Corregida |
| 2 | XSS almacenado | ticket.html (`\| safe`) | Alto | Revisión + test | Se quitó `safe` (autoescape Jinja) | | Corregida |
| 3 | IDOR (tickets ajenos) | /tickets/<id>, comentarios | Alto | Test | Verificar owner_id | | Corregida |
| 4 | CSRF | todos los POST | Medio | ZAP + test | Token CSRF en sesión | | Corregida |
| 5 | SECRET_KEY hardcodeada | app.py, compose.yaml | Alto | Revisión | Variable de entorno / aleatoria | | Corregida |
| 6 | Sin límite de intentos de login | /login | Medio | Revisión + Grafana | Bloqueo tras 10 fallos (429) | | Corregida |
| 7 | Faltan cabeceras de seguridad | respuestas HTTP | Medio | ZAP | CSP, X-Frame-Options, nosniff, etc. | | Corregida |
| 8 | Cookies sin SameSite/HttpOnly/Secure | sesión | Bajo | ZAP | Flags en config (Secure vía COOKIE_SECURE=1 con HTTPS) | | Corregida / riesgo aceptado (HTTP local) |
| 9 | Contenedor como root + servidor de desarrollo | Dockerfile | Medio | Revisión | Usuario no root + gunicorn | | Corregida |
| 10 | Dependencias desactualizadas | requirements.txt | Alto | pip-audit / Dependabot | Actualización de versiones | | Corregida |

## 3. Pruebas automatizadas – OWASP ZAP (IL 3.2)
- Build #1 (código vulnerable): alertas encontradas (captura/tabla) …
- Build #2 (código corregido): alertas restantes …
- Alertas pendientes y justificación …

## 4. Gestión de dependencias – Dependabot (IL 3.3)
| Paquete | Versión antes | Versión después | CVE resueltos |
|---|---|---|---|
(Capturas: PR de Dependabot, salida de pip-audit antes/después, build verde)

## 5. Monitorización – Grafana (IL 3.2)
- Dashboard (captura en estado normal)
- Incidente simulado: fuerza bruta de login (fecha/hora, captura del pico en "login fallidos")
- Detección, respuesta (rate limit 429, revisión de logs, bloqueo) y resultado

## 6. Trazabilidad (IL 3.4)
| Fecha | Actividad | Commit / Build | Evidencia |
|---|---|---|---|
