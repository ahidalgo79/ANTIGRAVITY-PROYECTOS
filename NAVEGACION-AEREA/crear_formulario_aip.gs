/**
 * Examen AIP/PIA — Generador de Formulario de Google con calificación automática.
 *
 * PEGA AQUÍ EL JSON GENERADO POR NOTEBOOKLM (constante PREGUNTAS) y ejecuta
 * la función crearFormulario(). El log mostrará la URL del formulario.
 *
 * Estructura esperada:
 * {
 *   "titulo": "...",
 *   "descripcion": "...",
 *   "opcion_multiple": [{ "texto": "...", "opciones": ["A","B","C","D"], "correcta": 0, "puntos": 5 }],
 *   "verdadero_falso": [{ "texto": "...", "correcta": true, "puntos": 3 }],
 *   "caso_estudio": {
 *     "escenario": "...",
 *     "preguntas": [{ "texto": "...", "opciones": ["A","B","C","D"], "correcta": 0, "puntos": 4 }]
 *   }
 * }
 */

const PREGUNTAS = {
  "titulo": "Examen AIP/PIA — Publicación de Información Aeronáutica",
  "descripcion": "Instrucciones: 10 opción múltiple (5 pts), 10 V/F (3 pts), 1 caso de estudio (20 pts). Total 100 pts.",
  "opcion_multiple": [
    {
      "texto": "Ejemplo: ¿Qué significa AIP?",
      "opciones": ["Publicación de Información Aeronáutica", "Aeronautical Information Publication", "Ambas son correctas", "Ninguna de las anteriores"],
      "correcta": 2,
      "puntos": 5
    }
  ],
  "verdadero_falso": [
    {
      "texto": "Ejemplo: La AIP es el manual básico de información aeronáutica.",
      "correcta": true,
      "puntos": 3
    }
  ],
  "caso_estudio": {
    "escenario": "Ejemplo: texto del escenario operativo.",
    "preguntas": [
      {
        "texto": "Ejemplo: pregunta derivada del escenario.",
        "opciones": ["A", "B", "C", "D"],
        "correcta": 0,
        "puntos": 4
      }
    ]
  }
};

function crearFormulario() {
  const form = FormApp.create(PREGUNTAS.titulo);
  form.setDescription(PREGUNTAS.descripcion)
      .setIsQuiz(true)
      .setCollectEmail(true)
      .setLimitOneResponsePerUser(true)
      .setShowLinkToRespondAgain(false);

  let total = 0;

  form.addSectionHeaderItem()
      .setTitle("Parte I — Opción múltiple (50 pts)");

  PREGUNTAS.opcion_multiple.forEach(p => {
    const item = form.addMultipleChoiceItem();
    item.setTitle(p.texto).setPoints(p.puntos).setRequired(true);
    item.setChoices(p.opciones.map((op, i) =>
      item.createChoice(op, i === p.correcta)));
    total += p.puntos;
  });

  form.addSectionHeaderItem()
      .setTitle("Parte II — Verdadero/Falso (30 pts)");

  PREGUNTAS.verdadero_falso.forEach(p => {
    const item = form.addMultipleChoiceItem();
    item.setTitle(p.texto).setPoints(p.puntos).setRequired(true);
    item.setChoices([
      item.createChoice("Verdadero", p.correcta === true),
      item.createChoice("Falso", p.correcta === false)
    ]);
    total += p.puntos;
  });

  form.addSectionHeaderItem()
      .setTitle("Parte III — Caso de estudio (20 pts)");
  form.addParagraphTextItem()
      .setTitle(PREGUNTAS.caso_estudio.escenario)
      .setHelpText("Lee el escenario y responde las preguntas.");

  PREGUNTAS.caso_estudio.preguntas.forEach(p => {
    const item = form.addMultipleChoiceItem();
    item.setTitle(p.texto).setPoints(p.puntos).setRequired(true);
    item.setChoices(p.opciones.map((op, i) =>
      item.createChoice(op, i === p.correcta)));
    total += p.puntos;
  });

  form.setConfirmationMessage("Examen enviado. Tu calificación se registrará automáticamente.");
  form.setAllowResponseEdits(false);
  form.setAcceptingResponses(true);

  Logger.log("URL del formulario: " + form.getPublishedUrl());
  Logger.log("Puntos totales configurados: " + total);
  return form.getId();
}

function borrarFormularioPrueba(id) {
  if (id) DriveApp.getFileById(id).setTrashed(true);
}
