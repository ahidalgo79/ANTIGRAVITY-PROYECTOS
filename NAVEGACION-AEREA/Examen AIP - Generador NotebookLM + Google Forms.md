---
tags: [clase, navegacion-aerea]
curso: Navegación Aérea
semana:
fecha: 12-08-2026
---

# Examen AIP/PIA — Generador NotebookLM + Google Forms

Flujo para generar un examen de 100 puntos sobre la **AIP/PIA (Publicación de
Información Aeronáutica / Aeronautical Information Publication)** usando
NotebookLM como generador de preguntas y un Apps Script para construir el
Formulario de Google con calificación automática.

## 📐 Distribución de puntos (total 100)

| Sección | Cantidad | Puntos c/u | Total |
|---|---|---|---|
| Opción múltiple | 10 | 5 | 50 |
| Verdadero/Falso | 10 | 3 | 30 |
| Caso de estudio | 1 (≈5 sub-preguntas) | 4 | 20 |
| **Total** | | | **100** |

## 🔁 Workflow

1. Subir el material de la AIP/PIA a **NotebookLM** (PDF/doc del manual AIP).
2. Pegar el **prompt de generación** (abajo) en la nota *Audio Overview / Notas*.
3. NotebookLM devuelve un **JSON** con las 21 preguntas (10 OM + 10 F/V + caso).
4. Copiar el JSON en `NAVEGACION-AEREA/crear_formulario_aip.gs` (constante `PREGUNTAS`).
5. Ejecutar `crearFormulario()` en apps-script.google.com.
6. El script crea el formulario, lo configura como *quiz* con clave de respuestas
   y loguea la URL.

## 📋 Prompt para NotebookLM

> Eres un evaluador de navegación aérea. A partir del material adjunto sobre la
> AIP/PIA (Publicación de Información Aeronáutica), genera un examen de 100
> puntos en **JSON válido** (sin comentarios, sin markdown alrededor, solo el
> bloque JSON). Estructura exacta:
>
> ```json
> {
>   "titulo": "Examen AIP/PIA — Publicación de Información Aeronáutica",
>   "descripcion": "Instrucciones: 10 opción múltiple (5 pts), 10 V/F (3 pts), 1 caso de estudio (20 pts). Total 100 pts.",
>   "opcion_multiple": [
>     {
>       "texto": "¿Qué significa AIP?",
>       "opciones": ["Publicación de Información Aeronáutica", "Aeronautical Information Publication", "Ambas son correctas", "Ninguna de las anteriores"],
>       "correcta": 2,
>       "puntos": 5
>     }
>   ],
>   "verdadero_falso": [
>     {
>       "texto": "La AIP es el manual básico de información aeronáutica para la navegación aérea.",
>       "correcta": true,
>       "puntos": 3
>     }
>   ],
>   "caso_estudio": {
>     "escenario": "Texto del escenario operativo que plantee el caso.",
>     "preguntas": [
>       {
>         "texto": "Pregunta derivada del escenario.",
>         "opciones": ["A", "B", "C", "D"],
>         "correcta": 0,
>         "puntos": 4
>       }
>     ]
>   }
> }
> ```
>
> Reglas:
> - Exactamente **10** elementos en `opcion_multiple`, **10** en `verdadero_falso`
>   y un caso de estudio con **5** sub-preguntas de opción múltiple.
> - `correcta` es el **índice** (0-based) de la opción correcta en `opciones`.
> - Las preguntas deben basarse SOLO en el material adjunto. Si un dato no está
>   en el material, no lo inventes: omítelo.
> - Usa lenguaje técnico aeronáutico correcto (español, salvo siglas oficiales).

## 📄 Apps Script

- Script: `NAVEGACION-AEREA/crear_formulario_aip.gs`
- Pegar el JSON de NotebookLM en la constante `PREGUNTAS`.
- Ejecutar la función `crearFormulario()` → loguea la URL del formulario.
- La clave de respuestas se configura automáticamente (quiz con calificación).

## 📚 Bibliografía recomendada

- Manual AIP/PIA OACI (Anexo 15 — Servicios de Información Aeronáutica)
- Doc 8126 — Manual de servicios de información aeronáutica

## ❓ Dudas recurrentes de alumnos

- Formato de exámenes en Formularios de Google vs DOCX
