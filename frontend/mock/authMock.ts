/**
 * Fake authentication server, used to work on the front-end until the backend implements /auth.
 *
 * Enabled only with `VITE_MOCK_AUTH=true` and `VITE_API_URL=/api` in frontend/.env.local.
 * It answers /api/auth/* in `vite` (dev) and `vite preview`, the way the backend should:
 *
 *   POST /auth/register  {firstName, lastName, email, password}  -> 201 User + session cookie
 *   POST /auth/login     {email, password}                       -> 200 User + session cookie
 *   GET  /auth/me                                                -> 200 User, or 401
 *   POST /auth/logout                                            -> 204, clears the cookie
 *
 * User = {id, email, firstName, lastName, avatarUrl, provider} (see src/types/auth.ts).
 * Errors are returned as {"detail": "..."}, like FastAPI.
 * Accounts live in memory and are lost when the server restarts.
 * Demo account: alice@example.com / password123
 */
import { randomUUID } from "node:crypto"
import type { IncomingMessage, ServerResponse } from "node:http"
import type { Plugin } from "vite"

const PREFIX = "/api/auth/"
const COOKIE_NAME = "signy_session"
const LATENCY_MS = 300

interface MockUser {
  id: number
  email: string
  firstName: string
  lastName: string
  password: string
}

export function authMock(): Plugin {
  let enabled = false
  const usersByEmail = new Map<string, MockUser>()
  const sessions = new Map<string, MockUser>() // session token -> user
  let nextId = 1

  function createUser(data: Omit<MockUser, "id">): MockUser {
    const user = { id: nextId++, ...data }
    usersByEmail.set(user.email, user)
    return user
  }

  createUser({
    email: "alice@example.com",
    password: "password123",
    firstName: "Alice",
    lastName: "Dupont",
  })

  function startSession(res: ServerResponse, user: MockUser, status: number) {
    const token = randomUUID()
    sessions.set(token, user)
    res.setHeader("Set-Cookie", `${COOKIE_NAME}=${token}; Path=/; HttpOnly; SameSite=Lax`)
    send(res, status, toPublicUser(user))
  }

  async function handle(req: IncomingMessage, res: ServerResponse, next: () => void) {
    if (!enabled || !req.url?.startsWith(PREFIX)) {
      next()
      return
    }
    // Simulated network latency, so that loading states are visible
    await new Promise((resolve) => setTimeout(resolve, LATENCY_MS))

    const path = req.url.slice(PREFIX.length).split("?")[0]
    const token = readCookie(req, COOKIE_NAME)
    const currentUser = token ? sessions.get(token) : undefined

    switch (`${req.method} ${path}`) {
      case "POST register": {
        const body = await readJson(req)
        const firstName = asText(body.firstName)
        const lastName = asText(body.lastName)
        const email = asText(body.email).toLowerCase()
        const password = typeof body.password === "string" ? body.password : ""
        if (!firstName || !lastName || !email || !password) {
          send(res, 400, { detail: "Tous les champs sont obligatoires." })
        } else if (password.length < 8) {
          send(res, 400, { detail: "Le mot de passe doit contenir au moins 8 caractères." })
        } else if (usersByEmail.has(email)) {
          send(res, 409, { detail: "Un compte existe déjà avec cet email." })
        } else {
          startSession(res, createUser({ firstName, lastName, email, password }), 201)
        }
        return
      }
      case "POST login": {
        const body = await readJson(req)
        const user = usersByEmail.get(asText(body.email).toLowerCase())
        if (!user || user.password !== body.password) {
          send(res, 401, { detail: "Email ou mot de passe incorrect." })
        } else {
          startSession(res, user, 200)
        }
        return
      }
      case "GET me":
        if (currentUser) {
          send(res, 200, toPublicUser(currentUser))
        } else {
          send(res, 401, { detail: "Non connecté." })
        }
        return
      case "POST logout":
        if (token) sessions.delete(token)
        res.setHeader("Set-Cookie", `${COOKIE_NAME}=; Path=/; HttpOnly; SameSite=Lax; Max-Age=0`)
        res.statusCode = 204
        res.end()
        return
      default:
        send(res, 404, { detail: "Route d'authentification inconnue." })
    }
  }

  function middleware(req: IncomingMessage, res: ServerResponse, next: () => void) {
    handle(req, res, next).catch((error: unknown) => {
      send(res, 500, { detail: `Erreur du faux serveur : ${String(error)}` })
    })
  }

  return {
    name: "signy-auth-mock",
    configResolved(config) {
      enabled = config.env.VITE_MOCK_AUTH === "true"
      if (enabled && config.env.VITE_API_URL !== "/api") {
        config.logger.warn(
          "[auth-mock] VITE_MOCK_AUTH=true needs VITE_API_URL=/api in .env.local to be reached",
        )
      }
    },
    configureServer(server) {
      if (!enabled) return
      server.middlewares.use(middleware)
      server.config.logger.info("[auth-mock] fake /api/auth enabled (alice@example.com / password123)")
    },
    configurePreviewServer(server) {
      if (!enabled) return
      server.middlewares.use(middleware)
      server.config.logger.info("[auth-mock] fake /api/auth enabled (alice@example.com / password123)")
    },
  }
}

function toPublicUser(user: MockUser) {
  return {
    id: user.id,
    email: user.email,
    firstName: user.firstName,
    lastName: user.lastName,
    avatarUrl: null,
    provider: "email",
  }
}

function send(res: ServerResponse, status: number, data: unknown) {
  res.statusCode = status
  res.setHeader("Content-Type", "application/json; charset=utf-8")
  res.end(JSON.stringify(data))
}

function asText(value: unknown): string {
  return typeof value === "string" ? value.trim() : ""
}

function readCookie(req: IncomingMessage, name: string): string | undefined {
  const cookies = req.headers.cookie?.split(";") ?? []
  for (const cookie of cookies) {
    const [key, ...rest] = cookie.trim().split("=")
    if (key === name) return rest.join("=")
  }
  return undefined
}

async function readJson(req: IncomingMessage): Promise<Record<string, unknown>> {
  const chunks: Buffer[] = []
  for await (const chunk of req) chunks.push(chunk as Buffer)
  try {
    const data: unknown = JSON.parse(Buffer.concat(chunks).toString("utf-8"))
    return data && typeof data === "object" ? (data as Record<string, unknown>) : {}
  } catch {
    return {}
  }
}
