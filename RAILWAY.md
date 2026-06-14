# DUNK — Desplegar en Railway (cuentas en la nube)

El juego ya trae un servidor (`server.js`, Express) que sirve el juego **y** la API de cuentas.
- En tu PC, sin base de datos, guarda en un archivo local (`.data/store.json`).
- En Railway, si añades Postgres, usa la base de datos automáticamente (`DATABASE_URL`).

## Probar en tu PC (con cuentas)
```bash
cd NBAjuego
npm install
npm start
```
Abre **http://localhost:3000** → verás la pantalla de login. Crea una cuenta y listo.
(Si solo quieres jugar sin cuenta, también sirve `python3 -m http.server` y pulsas "Jugar sin cuenta".)

## Desplegar en Railway
1. Entra a **railway.app** → inicia sesión → **New Project**.
2. **Deploy from GitHub repo** (sube antes esta carpeta `NBAjuego` a un repo) — o usa la **Railway CLI**:
   ```bash
   npm i -g @railway/cli
   railway login
   cd NBAjuego
   railway init        # crea el proyecto
   railway up          # sube y despliega
   ```
   > Si despliegas el repo entero, en Railway → Settings → **Root Directory** pon `NBAjuego`.
3. En el proyecto de Railway: **New → Database → Add PostgreSQL**.
   Railway crea la variable **`DATABASE_URL`** y el servidor la detecta solo (crea las tablas al arrancar).
4. En **Variables** del servicio, añade:
   - `JWT_SECRET` = una frase larga y aleatoria (p. ej. 30+ caracteres). **Guárdala**; es la que firma las sesiones.
5. Railway detecta Node por `package.json` y ejecuta `npm install` + `npm start`.
6. En **Settings → Networking → Generate Domain** para obtener tu URL pública.
   Esa URL sirve el juego y la API en el mismo sitio (el frontend ya apunta al mismo origen).

## Notas
- Las contraseñas se guardan **cifradas** (bcrypt); el servidor nunca guarda la contraseña en claro.
- El progreso (colección, balones, quinteto, mensajes) se guarda por cuenta y **sincroniza entre dispositivos**.
- `node_modules/` y `.data/` están en `.gitignore` (no se suben).
- Endpoints: `POST /api/register`, `POST /api/login`, `GET /api/me`, `GET/PUT /api/save`, `GET /api/health`.
