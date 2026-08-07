import type { Plugin } from "@opencode-ai/plugin"
import { readFile, writeFile, mkdir, access } from "node:fs/promises"
import path from "node:path"

const MEMORY_FILE = "Proyectos/memoria-opencode.md"
const VAULT_MARKER = ".obsidian"
const MAX_ENTRIES = 15
const MAX_PROMPT_CHARS = 400
const MAX_RESPONSE_CHARS = 900

const HEADER = `---
tags: [memoria, opencode]
---

# Memoria de sesiones — opencode

Resumen de las últimas sesiones, inyectado automáticamente al inicio de cada sesión por el plugin MemoriaPlugin.
\n`

const lastWritten = new Map<string, string>()

function truncate(s: string, n: number): string {
  const clean = s.replace(/\s+/g, " ").trim()
  return clean.length <= n ? clean : clean.slice(0, n) + "…"
}

function textOfParts(parts: Array<{ type?: string; text?: string }> | undefined): string {
  return (parts || [])
    .filter((p) => p.type === "text" && typeof p.text === "string")
    .map((p) => p.text as string)
    .join("\n")
}

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms))

async function isDir(p: string): Promise<boolean> {
  try {
    await access(p)
    return true
  } catch {
    return false
  }
}

async function findVaultRoot(start: string): Promise<string | null> {
  let current = path.resolve(start)
  const stop = path.parse(current).root
  while (true) {
    if (await isDir(path.join(current, VAULT_MARKER))) return current
    if (current === stop) return null
    current = path.dirname(current)
  }
}

export const MemoriaPlugin: Plugin = async ({ directory, client }) => {
  const root = (await findVaultRoot(directory)) ?? directory
  const memoriaPath = path.join(root, MEMORY_FILE)

  const readEntries = async (): Promise<string[]> => {
    try {
      const raw = await readFile(memoriaPath, "utf8")
      const body = raw.split(/^## /m).slice(1)
      return body.map((b) => "## " + b.trim()).filter(Boolean)
    } catch {
      return []
    }
  }

  const writeEntries = async (entries: string[]): Promise<void> => {
    await mkdir(path.dirname(memoriaPath), { recursive: true })
    const body = entries.slice(0, MAX_ENTRIES).join("\n\n---\n\n")
    await writeFile(memoriaPath, HEADER + body + "\n")
  }

  const saveSession = async (sessionID: string): Promise<void> => {
    await delay(500)
    const msgs = await client.session.messages({ path: { id: sessionID } })
    const list = msgs?.data
    if (!list || list.length === 0) return

    const last = list[list.length - 1]
    const lastId = last?.info?.id
    if (lastId && lastWritten.get(sessionID) === lastId) return
    if (lastId) lastWritten.set(sessionID, lastId)

    const lastUser = [...list].reverse().find((m) => m.info?.role === "user")
    const lastAssistant = [...list].reverse().find((m) => m.info?.role === "assistant")
    const prompt = textOfParts(lastUser?.parts)
    const response = textOfParts(lastAssistant?.parts)

    let title = sessionID.slice(0, 8)
    try {
      const s = await client.session.get({ path: { id: sessionID } })
      if (s?.data?.title) title = s.data.title
    } catch {
      /* sin título */
    }

    const now = new Date().toISOString().replace("T", " ").slice(0, 16)
    const marker = `session:${sessionID}`
    const entry =
      `## ${now} — ${title}\n\n` +
      `- **Última petición:** ${truncate(prompt, MAX_PROMPT_CHARS) || "(sin texto)"}\n` +
      `- **Fin de sesión:** ${truncate(response, MAX_RESPONSE_CHARS) || "(sin respuesta)"}\n\n` +
      `<!-- ${marker} -->`

    const entries = await readEntries()
    const filtered = entries.filter((e) => !e.includes(marker))
    filtered.unshift(entry)
    await writeEntries(filtered)
  }

  try {
    await mkdir(path.dirname(memoriaPath), { recursive: true })
    const exists = await readFile(memoriaPath, "utf8").catch(() => null)
    if (exists === null) await writeFile(memoriaPath, HEADER)
  } catch {
    /* el archivo se creará al primer guardado */
  }

  return {
    config: async (cfg) => {
      const inst = Array.isArray(cfg.instructions) ? [...cfg.instructions] : []
      if (!inst.includes(memoriaPath)) inst.push(memoriaPath)
      cfg.instructions = inst
    },
    event: async ({ event }) => {
      if (event.type !== "session.idle") return
      const sid = event.properties?.sessionID
      if (!sid) return
      try {
        await saveSession(sid)
      } catch (e) {
        await client.app.log({
          body: {
            service: "memoria",
            level: "warn",
            message: `No se pudo guardar memoria de la sesión: ${e}`,
          },
        })
      }
    },
  }
}
