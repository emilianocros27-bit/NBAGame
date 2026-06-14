/* ============================================================
   DUNK - servidor (Express + Postgres) para Railway
   - Sirve el juego (estático) y la API de cuentas.
   - Auth: registro/login con bcrypt + JWT.
   - Guarda el progreso de cada cuenta en la nube.
   - Si hay DATABASE_URL -> usa Postgres (Railway).
     Si no -> usa un archivo local .data/store.json (para probar en tu PC).
   ============================================================ */
const express = require("express");
const cors = require("cors");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const path = require("path");
const fs = require("fs");

const JWT_SECRET = process.env.JWT_SECRET || "dev-secret-cambia-esto";
const PORT = process.env.PORT || 3000;

const app = express();
app.use(cors());
app.use(express.json({ limit: "2mb" }));

/* ---------- Almacén de datos ---------- */
let store;
if (process.env.DATABASE_URL) {
  const { Pool } = require("pg");
  const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false },
  });
  store = {
    async init() {
      await pool.query(`CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        pass_hash TEXT NOT NULL,
        created_at TIMESTAMPTZ DEFAULT now())`);
      await pool.query(`CREATE TABLE IF NOT EXISTS saves(
        user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
        data JSONB,
        updated_at TIMESTAMPTZ DEFAULT now())`);
    },
    async getUser(u) { return (await pool.query("SELECT * FROM users WHERE username=$1", [u])).rows[0]; },
    async getUserById(id) { return (await pool.query("SELECT id,username FROM users WHERE id=$1", [id])).rows[0]; },
    async createUser(u, h) { return (await pool.query("INSERT INTO users(username,pass_hash) VALUES($1,$2) RETURNING id,username", [u, h])).rows[0]; },
    async getSave(id) { const r = await pool.query("SELECT data FROM saves WHERE user_id=$1", [id]); return r.rows[0] ? r.rows[0].data : null; },
    async setSave(id, data) { await pool.query("INSERT INTO saves(user_id,data,updated_at) VALUES($1,$2,now()) ON CONFLICT(user_id) DO UPDATE SET data=$2, updated_at=now()", [id, data]); },
  };
} else {
  const FILE = path.join(__dirname, ".data", "store.json");
  fs.mkdirSync(path.dirname(FILE), { recursive: true });
  let db = { users: [], saves: {}, seq: 1 };
  try { db = JSON.parse(fs.readFileSync(FILE, "utf8")); } catch (e) {}
  const persist = () => fs.writeFileSync(FILE, JSON.stringify(db));
  store = {
    async init() {},
    async getUser(u) { return db.users.find(x => x.username === u); },
    async getUserById(id) { const u = db.users.find(x => x.id === id); return u ? { id: u.id, username: u.username } : null; },
    async createUser(u, h) { const o = { id: db.seq++, username: u, pass_hash: h }; db.users.push(o); persist(); return { id: o.id, username: o.username }; },
    async getSave(id) { return db.saves[id] || null; },
    async setSave(id, data) { db.saves[id] = data; persist(); },
  };
}

/* ---------- Helpers ---------- */
const norm = s => String(s || "").trim();
const sign = u => jwt.sign({ uid: u.id }, JWT_SECRET, { expiresIn: "180d" });
function auth(req, res, next) {
  const t = (req.headers.authorization || "").replace("Bearer ", "");
  try { req.userId = jwt.verify(t, JWT_SECRET).uid; next(); }
  catch (e) { res.status(401).json({ error: "Sesión no válida" }); }
}

/* ---------- API ---------- */
app.post("/api/register", async (req, res) => {
  try {
    const username = norm(req.body.username).toLowerCase();
    const password = String(req.body.password || "");
    if (username.length < 3) return res.status(400).json({ error: "El usuario debe tener al menos 3 caracteres" });
    if (!/^[a-z0-9_]+$/.test(username)) return res.status(400).json({ error: "Usuario: solo letras, números y _" });
    if (password.length < 4) return res.status(400).json({ error: "La contraseña debe tener al menos 4 caracteres" });
    if (await store.getUser(username)) return res.status(409).json({ error: "Ese usuario ya existe" });
    const u = await store.createUser(username, await bcrypt.hash(password, 10));
    res.json({ token: sign(u), username: u.username });
  } catch (e) { console.error(e); res.status(500).json({ error: "Error del servidor" }); }
});

app.post("/api/login", async (req, res) => {
  try {
    const username = norm(req.body.username).toLowerCase();
    const password = String(req.body.password || "");
    const u = await store.getUser(username);
    if (!u || !(await bcrypt.compare(password, u.pass_hash)))
      return res.status(401).json({ error: "Usuario o contraseña incorrectos" });
    res.json({ token: sign(u), username: u.username });
  } catch (e) { console.error(e); res.status(500).json({ error: "Error del servidor" }); }
});

app.get("/api/me", auth, async (req, res) => {
  const u = await store.getUserById(req.userId);
  if (!u) return res.status(401).json({ error: "Sesión no válida" });
  res.json({ username: u.username });
});

app.get("/api/save", auth, async (req, res) => {
  res.json({ data: await store.getSave(req.userId) });
});

app.put("/api/save", auth, async (req, res) => {
  await store.setSave(req.userId, req.body.data || {});
  res.json({ ok: true });
});

app.get("/api/health", (req, res) => res.json({ ok: true, db: process.env.DATABASE_URL ? "postgres" : "file" }));

/* ---------- Estático (el juego) ---------- */
// nunca servir rutas con segmentos ocultos (p.ej. /.data) ni archivos del servidor
const BLOCK = new Set(["server.js", "package.json", "package-lock.json"]);
app.use((req, res, next) => {
  const segs = req.path.split("/").filter(Boolean);
  if (segs.some(s => s.startsWith(".")) || BLOCK.has(segs[segs.length - 1])) return res.status(404).end();
  next();
});
app.use(express.static(__dirname, { dotfiles: "deny" }));

store.init()
  .then(() => app.listen(PORT, () => console.log("DUNK server escuchando en :" + PORT + " (db: " + (process.env.DATABASE_URL ? "postgres" : "file") + ")")))
  .catch(e => { console.error("No se pudo iniciar:", e); process.exit(1); });
