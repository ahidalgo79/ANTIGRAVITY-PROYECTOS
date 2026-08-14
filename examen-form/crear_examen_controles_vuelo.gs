/**
 * EVALUACIÓN COMPLETA: Sistemas de Control de Vuelo — A320 / B737
 * Duración: 2 horas | 60 reactivos | 200 puntos
 * 
 * INSTRUCCIONES:
 * 1. Ve a https://script.google.com
 * 2. Nuevo proyecto → borra código por defecto
 * 3. Pega este código completo
 * 4. Ejecuta: crearEvaluacionCompleta
 * 5. Autoriza permisos
 * 6. El formulario se crea en tu Google Drive
 */

function crearEvaluacionCompleta() {
  var form = FormApp.create('Evaluación: Sistemas de Control de Vuelo — A320 / B737');
  
  form.setDescription(
    'Evaluación técnica integral sobre arquitectura y lógica de controles de vuelo Airbus A320 y Boeing 737.\n\n' +
    'DURACIÓN: 2 horas\n' +
    'SECCIÓN 1: Opción múltiple A320 — 20 preguntas (5 pts c/u = 100 pts)\n' +
    'SECCIÓN 2: Verdadero/Falso B737 — 20 preguntas (2 pts c/u = 40 pts)\n' +
    'SECCIÓN 3: Caso de estudio — 20 preguntas (3 pts c/u = 60 pts)\n' +
    'PUNTAJE TOTAL: 200 puntos\n\n' +
    'Calificación automática.'
  );
  
  form.setIsQuiz(true);
  form.setCollectEmail(true);
  form.setProgressBar(true);
  form.setLimitOneResponsePerUser(true);
  
  // ================================================================
  // SECCIÓN 1: A320 — OPCIÓN MÚLTIPLE (20 preguntas, 5 pts)
  // ================================================================
  
  form.addPageBreakItem().setTitle('SECCIÓN 1: Airbus A320 — Opción Múltiple (100 pts)');
  
  form.addSectionHeaderItem().setTitle('Instrucciones: Seleccione la respuesta correcta. Cada pregunta vale 5 puntos.');
  
  // P1
  var q1 = form.addMultipleChoiceItem();
  q1.setTitle('1. ¿Qué computador es el principal responsable del control de los elevadores y el estabilizador horizontal (THS) en condiciones normales?');
  q1.setPoints(5);
  q1.setChoices([
    q1.createChoice('SEC 1', false),
    q1.createChoice('ELAC 2', true),
    q1.createChoice('FAC 1', false),
    q1.createChoice('ELAC 1', false)
  ]);
  q1.setRequired(true);
  q1.setFeedbackForCorrect(FormApp.createFeedback().setText('ELAC 2 es el computador primario para elevadores y THS en operación normal.').build());
  q1.setFeedbackForIncorrect(FormApp.createFeedback().setText('ELAC 2 controla elevadores y THS. SEC y FAC tienen funciones diferentes.').build());
  
  // P2
  var q2 = form.addMultipleChoiceItem();
  q2.setTitle('2. ¿Qué microprocesadores utiliza el A320 en sus computadores ELAC y SEC para garantizar la redundancia disímil?');
  q2.setPoints(5);
  q2.setChoices([
    q2.createChoice('Ambos usan Intel 80186', false),
    q2.createChoice('ELAC usa Intel y SEC usa Motorola', false),
    q2.createChoice('ELAC usa Motorola y SEC usa Intel', true),
    q2.createChoice('Ambos usan microprocesadores ARM', false)
  ]);
  q2.setRequired(true);
  q2.setFeedbackForCorrect(FormApp.createFeedback().setText('Redundancia disímil: Motorola (ELAC) + Intel (SEC) evita fallos de modo común.').build());
  q2.setFeedbackForIncorrect(FormApp.createFeedback().setText('ELAC usa Motorola, SEC usa Intel. Esta diversidad previene fallos de modo común.').build());
  
  // P3
  var q3 = form.addMultipleChoiceItem();
  q3.setTitle('3. ¿Bajo qué ley de control el A320 cuenta con protecciones de "límite rígido" que el piloto no puede sobrepasar?');
  q3.setPoints(5);
  q3.setChoices([
    q3.createChoice('Alternate Law', false),
    q3.createChoice('Direct Law', false),
    q3.createChoice('Normal Law', true),
    q3.createChoice('Mechanical Backup', false)
  ]);
  q3.setRequired(true);
  q3.setFeedbackForCorrect(FormApp.createFeedback().setText('Normal Law tiene protecciones de envolvente con límites rígidos: pitch, bank, load factor, high speed, alpha.').build());
  q3.setFeedbackForIncorrect(FormApp.createFeedback().setText('Solo Normal Law tiene límites rígidos. Alternate y Direct Law degradan protecciones.').build());
  
  // P4
  var q4 = form.addMultipleChoiceItem();
  q4.setTitle('4. ¿Qué función del autogás ordena automáticamente empuje TOGA si el ángulo de ataque es críticamente elevado?');
  q4.setPoints(5);
  q4.setChoices([
    q4.createChoice('Alpha Lock', false),
    q4.createChoice('Alpha Floor', true),
    q4.createChoice('Speed Baulk', false),
    q4.createChoice('Maneuver Demand', false)
  ]);
  q4.setRequired(true);
  q4.setFeedbackForCorrect(FormApp.createFeedback().setText('Alpha Floor activa TOGA automáticamente cuando AoA supera umbral crítico.').build());
  q4.setFeedbackForIncorrect(FormApp.createFeedback().setText('Alpha Floor ordena TOGA ante AoA crítico. Alpha Lock bloquea retracción de slats.').build());
  
  // P5
  var q5 = form.addMultipleChoiceItem();
  q5.setTitle('5. En degradación a Ley Alternativa, ¿qué sucede con el control del eje lateral (alabeo)?');
  q5.setPoints(5);
  q5.setChoices([
    q5.createChoice('Se mantiene en Ley Normal', false),
    q5.createChoice('Pasa a Respaldo Mecánico', false),
    q5.createChoice('Revierte a Ley Directa', true),
    q5.createChoice('Se pierde totalmente', false)
  ]);
  q5.setRequired(true);
  q5.setFeedbackForCorrect(FormApp.createFeedback().setText('En Alternate Law, el eje lateral siempre opera en Direct Law.').build());
  q5.setFeedbackForIncorrect(FormApp.createFeedback().setText('En Alternate Law, el eje lateral revierte a Direct Law sin protecciones.').build());
  
  // P6
  var q6 = form.addMultipleChoiceItem();
  q6.setTitle('6. ¿Qué sistemas hidráulicos alimentan los elevadores del A320?');
  q6.setPoints(5);
  q6.setChoices([
    q6.createChoice('Solo Verde', false),
    q6.createChoice('Verde y Amarillo', false),
    q6.createChoice('Verde, Azul y Amarillo', true),
    q6.createChoice('Solo Azul', false)
  ]);
  q6.setRequired(true);
  q6.setFeedbackForCorrect(FormApp.createFeedback().setText('Los elevadores reciben los tres sistemas hidráulicos para máxima redundancia.').build());
  q6.setFeedbackForIncorrect(FormApp.createFeedback().setText('Elevadores alimentados por Verde, Azul y Amarillo.').build());
  
  // P7
  var q7 = form.addMultipleChoiceItem();
  q7.setTitle('7. ¿Por qué ELAC 2 es ítem "NO-GO" para despacho?');
  q7.setPoints(5);
  q7.setChoices([
    q7.createChoice('Controla exclusivamente alerones', false),
    q7.createChoice('Detección de cizalladura', false),
    q7.createChoice('Necesidad crítica durante despliegue de RAT (8 seg)', true),
    q7.createChoice('Calcula VLS', false)
  ]);
  q7.setRequired(true);
  q7.setFeedbackForCorrect(FormApp.createFeedback().setText('ELAC 2 es crítico durante despliegue de RAT: único computador activo para pitch.').build());
  q7.setFeedbackForIncorrect(FormApp.createFeedback().setText('ELAC 2 es NO-GO por su rol crítico durante los 8 seg de despliegue de RAT.').build());
  
  // P8
  var q8 = form.addMultipleChoiceItem();
  q8.setTitle('8. ¿Cuál es función principal de los FAC?');
  q8.setPoints(5);
  q8.setChoices([
    q8.createChoice('Control de spoilers', false),
    q8.createChoice('Control de elevadores', false),
    q8.createChoice('Yaw damping y limitación de recorrido del timón', true),
    q8.createChoice('Retracción de flaps', false)
  ]);
  q8.setRequired(true);
  q8.setFeedbackForCorrect(FormApp.createFeedback().setText('FAC gestiona yaw damping, rudder trim y rudder travel limitation.').build());
  q8.setFeedbackForIncorrect(FormApp.createFeedback().setText('FAC = yaw damping + rudder. Spoilers son controlados por SEC.').build());
  
  // P9
  var q9 = form.addMultipleChoiceItem();
  q9.setTitle('9. Si ambos pilotos mueven sidesticks simultáneamente sin prioridad, ¿cómo se procesan las órdenes?');
  q9.setPoints(5);
  q9.setChoices([
    q9.createChoice('Se ignora copiloto', false),
    q9.createChoice('Respuesta al más fuerte', false),
    q9.createChoice('Señales se suman algebraicamente', true),
    q9.createChoice('AP se conecta', false)
  ]);
  q9.setRequired(true);
  q9.setFeedbackForCorrect(FormApp.createFeedback().setText('Señales se suman algebraicamente con límite máximo. Alerta "DUAL INPUT".').build());
  q9.setFeedbackForIncorrect(FormApp.createFeedback().setText('Ambos sidesticks se suman algebraicamente. No se ignora ninguno.').build());
  
  // P10
  var q10 = form.addMultipleChoiceItem();
  q10.setTitle('10. ¿Qué computador controla eléctricamente slats y flaps?');
  q10.setPoints(5);
  q10.setChoices([
    q10.createChoice('ELAC', false),
    q10.createChoice('SEC', false),
    q10.createChoice('SFCC', true),
    q10.createChoice('FCDC', false)
  ]);
  q10.setRequired(true);
  q10.setFeedbackForCorrect(FormApp.createFeedback().setText('Dos SFCC, cada uno con canal slats + flaps, proporcionando redundancia.').build());
  q10.setFeedbackForIncorrect(FormApp.createFeedback().setText('SFCC controla slats/flaps. ELAC y SEC controlan superficies primarias.').build());
  
  // P11
  var q11 = form.addMultipleChoiceItem();
  q11.setTitle('11. ¿Qué componente bloquea físicamente la transmisión de flaps/slats ante asimetría?');
  q11.setPoints(5);
  q11.setChoices([
    q11.createChoice('Solenoide de prioridad', false),
    q11.createChoice('Wing Tip Brakes (WTB)', true),
    q11.createChoice('Pressure-Off Brake', false),
    q11.createChoice('LVDT', false)
  ]);
  q11.setRequired(true);
  q11.setFeedbackForCorrect(FormApp.createFeedback().setText('WTB bloquean mecánicamente ante asimetría, overspeed o movimiento no comandado.').build());
  q11.setFeedbackForIncorrect(FormApp.createFeedback().setText('WTB son frenos mecánicos que bloquean transmisión de flaps/slats.').build());
  
  // P12
  var q12 = form.addMultipleChoiceItem();
  q12.setTitle('12. En E-Rudder, ¿qué unidad proporciona sensación artificial en los pedales?');
  q12.setPoints(5);
  q12.setChoices([
    q12.createChoice('BCM', false),
    q12.createChoice('RBPU', true),
    q12.createChoice('FAC 1', false),
    q12.createChoice('FCDC', false)
  ]);
  q12.setRequired(true);
  q12.setFeedbackForCorrect(FormApp.createFeedback().setText('RBPU reemplaza sensación mecánica por fuerza artificial en pedales.').build());
  q12.setFeedbackForIncorrect(FormApp.createFeedback().setText('RBPU proporciona sensación artificial en arquitectura E-Rudder.').build());
  
  // P13
  var q13 = form.addMultipleChoiceItem();
  q13.setTitle('13. ¿Cuál es el enfoque FBW de Boeing (B777)?');
  q13.setPoints(5);
  q13.setChoices([
    q13.createChoice('Límites rígidos de envolvente', false),
    q13.createChoice('"Command, don\'t constrain" — piloto tiene autoridad final', true),
    q13.createChoice('Sin sensación artificial', false),
    q13.createChoice('Sidesticks sin interconexión', false)
  ]);
  q13.setRequired(true);
  q13.setFeedbackForCorrect(FormApp.createFeedback().setText('Boeing: protecciones existen pero piloto puede sobrepasarlas. Airbus: límites rígidos.').build());
  q13.setFeedbackForIncorrect(FormApp.createFeedback().setText('Boeing usa "command, don\'t constrain". Límites rígidos = Airbus.').build());
  
  // P14
  var q14 = form.addMultipleChoiceItem();
  q14.setTitle('14. En Mechanical Backup, ¿qué controles tiene el piloto?');
  q14.setPoints(5);
  q14.setChoices([
    q14.createChoice('Sidestick + pedales', false),
    q14.createChoice('Solo timón', false),
    q14.createChoice('Rueda de trim THS + pedales', true),
    q14.createChoice('Solo potencia', false)
  ]);
  q14.setRequired(true);
  q14.setFeedbackForCorrect(FormApp.createFeedback().setText('Mechanical Backup: pitch = rueda trim THS, yaw = pedales. Sidestick inoperativo.').build());
  q14.setFeedbackForIncorrect(FormApp.createFeedback().setText('Mechanical Backup = rueda trim manual (THS) + pedales.').build());
  
  // P15
  var q15 = form.addMultipleChoiceItem();
  q15.setTitle('15. ¿Función de los FCDC?');
  q15.setPoints(5);
  q15.setChoices([
    q15.createChoice('Calcular protecciones', false),
    q15.createChoice('Adquirir datos ELAC/SEC para ECAM y mantenimiento', true),
    q15.createChoice('Respaldo FAC', false),
    q15.createChoice('Controlar spoilers', false)
  ]);
  q15.setRequired(true);
  q15.setFeedbackForCorrect(FormApp.createFeedback().setText('FCDC = concentradores de datos para ECAM y CFDS. No controlan actuadores.').build());
  q15.setFeedbackForIncorrect(FormApp.createFeedback().setText('FCDC adquiere señales de ELAC/SEC para pantallas y mantenimiento.').build());
  
  // P16
  var q16 = form.addMultipleChoiceItem();
  q16.setTitle('16. En Normal Law, ¿límite de pitch up en configuración limpia?');
  q16.setPoints(5);
  q16.setChoices([
    q16.createChoice('15°', false),
    q16.createChoice('25°', false),
    q16.createChoice('30°', true),
    q16.createChoice('45°', false)
  ]);
  q16.setRequired(true);
  q16.setFeedbackForCorrect(FormApp.createFeedback().setText('+30° en config 0 (limpia), +25° en configs 1-4.').build());
  q16.setFeedbackForIncorrect(FormApp.createFeedback().setText('Pitch up limit: +30° config limpia, +25° configs 1-4.').build());
  
  // P17
  var q17 = form.addMultipleChoiceItem();
  q17.setTitle('17. ¿Qué función impide retracción de slats si AoA > 8.5° o velocidad < 148 kt?');
  q17.setPoints(5);
  q17.setChoices([
    q17.createChoice('Flap Auto-Retraction', false),
    q17.createChoice('Speed Stability', false),
    q17.createChoice('Alpha Lock', true),
    q17.createChoice('High Speed Protection', false)
  ]);
  q17.setRequired(true);
  q17.setFeedbackForCorrect(FormApp.createFeedback().setText('Alpha Lock bloquea retracción de slats en alto AoA o baja velocidad.').build());
  q17.setFeedbackForIncorrect(FormApp.createFeedback().setText('Alpha Lock impide retraer slats para evitar pérdida de sustentación.').build());
  
  // P18
  var q18 = form.addMultipleChoiceItem();
  q18.setTitle('18. ¿Responsabilidad principal de SEC 3?');
  q18.setPoints(5);
  q18.setChoices([
    q18.createChoice('Backup elevadores/THS', false),
    q18.createChoice('Spoilers 1 y 2 + ground spoilers', true),
    q18.createChoice('Alerones', false),
    q18.createChoice('Yaw damping', false)
  ]);
  q18.setRequired(true);
  q18.setFeedbackForCorrect(FormApp.createFeedback().setText('SEC 3 controla spoilers 1/2 y ground spoilers para frenado aerodinámico.').build());
  q18.setFeedbackForIncorrect(FormApp.createFeedback().setText('SEC 3 = spoilers 1 y 2 + ground spoilers. Elevadores = ELAC.').build());
  
  // P19
  var q19 = form.addMultipleChoiceItem();
  q19.setTitle('19. En arquitectura COM/MON, ¿qué pasa si hay discrepancia entre canales?');
  q19.setPoints(5);
  q19.setChoices([
    q19.createChoice('Se ignora', false),
    q19.createChoice('Alarma pero continúa', false),
    q19.createChoice('Computador se pasiva, siguiente toma mando', true),
    q19.createChoice('Piloto reinicia manualmente', false)
  ]);
  q19.setRequired(true);
  q19.setFeedbackForCorrect(FormApp.createFeedback().setText('COM/MON fail-safe: discrepancia → computador se desconecta, backup asume.').build());
  q19.setFeedbackForIncorrect(FormApp.createFeedback().setText('Arquitectura fail-safe: discrepancia → desconexión automática → backup.').build());
  
  // P20
  var q20 = form.addMultipleChoiceItem();
  q20.setTitle('20. ¿Qué indicación aparece en PFD en Direct Law?');
  q20.setPoints(5);
  q20.setChoices([
    q20.createChoice('"ALTN LAW" verde', false),
    q20.createChoice('"MAN PITCH TRIM ONLY" rojo', false),
    q20.createChoice('"USE MAN PITCH TRIM" ámbar', true),
    q20.createChoice('"STALL" rojo', false)
  ]);
  q20.setRequired(true);
  q20.setFeedbackForCorrect(FormApp.createFeedback().setText('"USE MAN PITCH TRIM" ámbar indica trim manual obligatorio sin protecciones.').build());
  q20.setFeedbackForIncorrect(FormApp.createFeedback().setText('Direct Law = "USE MAN PITCH TRIM" ámbar en PFD.').build());
  
  // ================================================================
  // SECCIÓN 2: B737 — VERDADERO / FALSO (20 preguntas, 2 pts)
  // ================================================================
  
  form.addPageBreakItem().setTitle('SECCIÓN 2: Boeing 737 — Verdadero/Falso (40 pts)');
  
  form.addSectionHeaderItem().setTitle('Instrucciones: Indique si la afirmación es Verdadera o Falsa. Cada pregunta vale 2 puntos.');
  
  // VF1
  var vf1 = form.addMultipleChoiceItem();
  vf1.setTitle('21. Los alerones y elevadores del B737 disponen de reversión manual mediante cables en caso de fallo total de sistemas hidráulicos A y B.');
  vf1.setPoints(2);
  vf1.setChoices([vf1.createChoice('Verdadero', true), vf1.createChoice('Falso', false)]);
  vf1.setRequired(true);
  vf1.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. B737 mantiene cables mecánicos como respaldo para alerones y elevadores.').build());
  vf1.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. El B737 tiene capacidad de reversión manual por cables.').build());
  
  // VF2
  var vf2 = form.addMultipleChoiceItem();
  vf2.setTitle('22. El timón de dirección (rudder) del B737 puede operarse mecánicamente sin asistencia de ningún sistema hidráulico.');
  vf2.setPoints(2);
  vf2.setChoices([vf2.createChoice('Verdadero', false), vf2.createChoice('Falso', true)]);
  vf2.setRequired(true);
  vf2.setFeedbackForCorrect(FormApp.createFeedback().setText('Falso. El rudder requiere presión del sistema A, B o Standby para operar.').build());
  vf2.setFeedbackForIncorrect(FormApp.createFeedback().setText('Falso. El rudder necesita asistencia hidráulica (A, B o Standby).').build());
  
  // VF3
  var vf3 = form.addMultipleChoiceItem();
  vf3.setTitle('23. La presión nominal de los sistemas hidráulicos principal y de reserva del B737 es de 3,000 PSI.');
  vf3.setPoints(2);
  vf3.setChoices([vf3.createChoice('Verdadero', true), vf3.createChoice('Falso', false)]);
  vf3.setRequired(true);
  vf3.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. 3,000 PSI es la presión nominal estándar.').build());
  vf3.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Presión nominal = 3,000 PSI.').build());
  
  // VF4
  var vf4 = form.addMultipleChoiceItem();
  vf4.setTitle('24. El Speed Trim System (STS) del B737 opera únicamente cuando el piloto automático está conectado.');
  vf4.setPoints(2);
  vf4.setChoices([vf4.createChoice('Verdadero', false), vf4.createChoice('Falso', true)]);
  vf4.setRequired(true);
  vf4.setFeedbackForCorrect(FormApp.createFeedback().setText('Falso. STS opera exclusivamente en vuelo manual, no con AP conectado.').build());
  vf4.setFeedbackForIncorrect(FormApp.createFeedback().setText('Falso. STS funciona solo en vuelo manual.').build());
  
  // VF5
  var vf5 = form.addMultipleChoiceItem();
  vf5.setTitle('25. MCAS es una característica de estabilidad longitudinal exclusiva del Boeing 737 MAX.');
  vf5.setPoints(2);
  vf5.setChoices([vf5.createChoice('Verdadero', true), vf5.createChoice('Falso', false)]);
  vf5.setRequired(true);
  vf5.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. MCAS fue introducido específicamente en el 737 MAX.').build());
  vf5.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. MCAS es exclusivo del 737 MAX.').build());
  
  // VF6
  var vf6 = form.addMultipleChoiceItem();
  vf6.setTitle('26. Los ground spoilers del 737 NG son alimentados por los sistemas hidráulicos A y B de forma redundante.');
  vf6.setPoints(2);
  vf6.setChoices([vf6.createChoice('Verdadero', false), vf6.createChoice('Falso', true)]);
  vf6.setRequired(true);
  vf6.setFeedbackForCorrect(FormApp.createFeedback().setText('Falso. Los ground spoilers del 737 NG solo son alimentados por el sistema A.').build());
  vf6.setFeedbackForIncorrect(FormApp.createFeedback().setText('Falso. Solo sistema A alimenta ground spoilers en 737 NG.').build());
  
  // VF7
  var vf7 = form.addMultipleChoiceItem();
  vf7.setTitle('27. El Mach Trim compensa el "Mach Tuck" ajustando elevadores a velocidades superiores a Mach 0.615.');
  vf7.setPoints(2);
  vf7.setChoices([vf7.createChoice('Verdadero', true), vf7.createChoice('Falso', false)]);
  vf7.setRequired(true);
  vf7.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. Mach Trim compensa el desplazamiento del centro de presión a alta velocidad.').build());
  vf7.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Mach Trim actúa por encima de Mach 0.615.').build());
  
  // VF8
  var vf8 = form.addMultipleChoiceItem();
  vf8.setTitle('28. Si la FSEU detecta asimetría en flaps de borde de salida, corta automáticamente la potencia hidráulica a la unidad de accionamiento.');
  vf8.setPoints(2);
  vf8.setChoices([vf8.createChoice('Verdadero', true), vf8.createChoice('Falso', false)]);
  vf8.setRequired(true);
  vf8.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. La FSEU protege contra asimetría cortando potencia hidráulica.').build());
  vf8.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. FSEU corta potencia ante asimetría detectada.').build());
  
  // VF9
  var vf9 = form.addMultipleChoiceItem();
  vf9.setTitle('29. Los Leading Edge Devices del B737 son operados normalmente por el sistema hidráulico A.');
  vf9.setPoints(2);
  vf9.setChoices([vf9.createChoice('Verdadero', false), vf9.createChoice('Falso', true)]);
  vf9.setRequired(true);
  vf9.setFeedbackForCorrect(FormApp.createFeedback().setText('Falso. La fuente normal de los LED es el sistema hidráulico B.').build());
  vf9.setFeedbackForIncorrect(FormApp.createFeedback().setText('Falso. LED operan con sistema B, no A.').build());
  
  // VF10
  var vf10 = form.addMultipleChoiceItem();
  vf10.setTitle('30. La función Autoslat extiende los slats de "Extend" a "Full Extend" automáticamente si el avión se aproxima a una pérdida con flaps 1-25.');
  vf10.setPoints(2);
  vf10.setChoices([vf10.createChoice('Verdadero', true), vf10.createChoice('Falso', false)]);
  vf10.setRequired(true);
  vf10.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. Autoslat extiende automáticamente slats para evitar pérdida.').build());
  vf10.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Autoslat actúa con flaps 1-25 ante aproximación a pérdida.').build());
  
  // VF11
  var vf11 = form.addMultipleChoiceItem();
  vf11.setTitle('31. Para separar las columnas de mando mediante breakout clutch ante bloqueo del elevador, se requiere fuerza de 50-80 libras.');
  vf11.setPoints(2);
  vf11.setChoices([vf11.createChoice('Verdadero', true), vf11.createChoice('Falso', false)]);
  vf11.setRequired(true);
  vf11.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. Breakout clutch requiere 50-80 lbs para separar columnas.').build());
  vf11.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Fuerza requerida: 50-80 libras.').build());
  
  // VF12
  var vf12 = form.addMultipleChoiceItem();
  vf12.setTitle('32. El Force Fight Monitor activa la bomba de reserva si detecta discrepancia de presión en la PCU del timón por más de 5 segundos.');
  vf12.setPoints(2);
  vf12.setChoices([vf12.createChoice('Verdadero', true), vf12.createChoice('Falso', false)]);
  vf12.setRequired(true);
  vf12.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. FFM activa standby pump tras 5 seg de discrepancia en PCU.').build());
  vf12.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. FFM → standby pump tras 5 seg de discrepancia.').build());
  
  // VF13
  var vf13 = form.addMultipleChoiceItem();
  vf13.setTitle('33. Las correcciones del Yaw Damper provocan movimiento proporcional de los pedales del timón en cabina.');
  vf13.setPoints(2);
  vf13.setChoices([vf13.createChoice('Verdadero', false), vf13.createChoice('Falso', true)]);
  vf13.setRequired(true);
  vf13.setFeedbackForCorrect(FormApp.createFeedback().setText('Falso. El Yaw Damper mueve el rudder pero NO mueve los pedales.').build());
  vf13.setFeedbackForIncorrect(FormApp.createFeedback().setText('Falso. Yaw Damper no mueve pedales; solo actúa sobre la superficie.').build());
  
  // VF14
  var vf14 = form.addMultipleChoiceItem();
  vf14.setTitle('34. El B737 MAX utiliza fly-by-wire para el control de todos sus spoilers de vuelo y tierra.');
  vf14.setPoints(2);
  vf14.setChoices([vf14.createChoice('Verdadero', true), vf14.createChoice('Falso', false)]);
  vf14.setRequired(true);
  vf14.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. El MAX introdujo FBW para spoilers mediante SCE.').build());
  vf14.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Spoilers del MAX son controlados por FBW vía SCE.').build());
  
  // VF15
  var vf15 = form.addMultipleChoiceItem();
  vf15.setTitle('35. El módulo Elevator Feel Shift duplica la fuerza de sensación en la columna usando presión del sistema A durante una pérdida.');
  vf15.setPoints(2);
  vf15.setChoices([vf15.createChoice('Verdadero', true), vf15.createChoice('Falso', false)]);
  vf15.setRequired(true);
  vf15.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. EFS duplica fuerza de sensación durante stall usando presión hidráulica A.').build());
  vf15.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. EFS aumenta fuerza en columna durante condición de pérdida.').build());
  
  // VF16
  var vf16 = form.addMultipleChoiceItem();
  vf16.setTitle('36. Los LED pueden ser retraídos usando el sistema Standby a través de los interruptores de Flaps Alternos.');
  vf16.setPoints(2);
  vf16.setChoices([vf16.createChoice('Verdadero', false), vf16.createChoice('Falso', true)]);
  vf16.setRequired(true);
  vf16.setFeedbackForCorrect(FormApp.createFeedback().setText('Falso. Standby solo puede EXTENDER LED, no retraerlos.').build());
  vf16.setFeedbackForIncorrect(FormApp.createFeedback().setText('Falso. Alternate flaps solo extiende LED con Standby; no retrae.').build());
  
  // VF17
  var vf17 = form.addMultipleChoiceItem();
  vf17.setTitle('37. La advertencia de configuración de despegue suena si el estabilizador está fuera de la banda verde con empujes avanzados.');
  vf17.setPoints(2);
  vf17.setChoices([vf17.createChoice('Verdadero', true), vf17.createChoice('Falso', false)]);
  vf17.setRequired(true);
  vf17.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. Takeoff Configuration Warning suena con stab fuera de banda verde + thrust avanzado.').build());
  vf17.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Config warning = stab fuera de green band + thrust.').build());
  
  // VF18
  var vf18 = form.addMultipleChoiceItem();
  vf18.setTitle('38. Las computadoras SMYD activan los stick shakers como alerta de pérdida.');
  vf18.setPoints(2);
  vf18.setChoices([vf18.createChoice('Verdadero', true), vf18.createChoice('Falso', false)]);
  vf18.setRequired(true);
  vf18.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. SMYD gestiona stall warning incluyendo stick shakers.').build());
  vf18.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. SMYD = Stall Management Yaw Damper, activa stick shakers.').build());
  
  // VF19
  var vf19 = form.addMultipleChoiceItem();
  vf19.setTitle('39. Los fusibles hidráulicos en líneas de LED sellan el flujo para prevenir pérdida total de fluido ante ruptura.');
  vf19.setPoints(2);
  vf19.setChoices([vf19.createChoice('Verdadero', true), vf19.createChoice('Falso', false)]);
  vf19.setRequired(true);
  vf19.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. Hydraulic fuses previenen pérdida total de fluido en caso de ruptura de línea.').build());
  vf19.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Fusibles hidráulicos = protección contra pérdida de fluido.').build());
  
  // VF20
  var vf20 = form.addMultipleChoiceItem();
  vf20.setTitle('40. Las ruedas de trim manual del estabilizador pueden anular mecánicamente cualquier entrada eléctrica o automática.');
  vf20.setPoints(2);
  vf20.setChoices([vf20.createChoice('Verdadero', true), vf20.createChoice('Falso', false)]);
  vf20.setRequired(true);
  vf20.setFeedbackForCorrect(FormApp.createFeedback().setText('Verdadero. Stab trim wheels tienen autoridad mecánica sobre cualquier input eléctrico.').build());
  vf20.setFeedbackForIncorrect(FormApp.createFeedback().setText('Verdadero. Trim manual siempre tiene prioridad sobre trim eléctrico/automático.').build());
  
  // ================================================================
  // SECCIÓN 3: CASO DE ESTUDIO (20 preguntas, 3 pts)
  // ================================================================
  
  form.addPageBreakItem().setTitle('SECCIÓN 3: Caso de Estudio — Degradación Sistémica (60 pts)');
  
  form.addSectionHeaderItem().setTitle(
    'CASO DE ESTUDIO: Degradación Sistémica y Transición de Leyes de Vuelo\n\n' +
    'Un Airbus A320 en crucero experimenta falla eléctrica severa con pérdida total de ambos ELAC. ' +
    'Simultáneamente, caída de presión en sistema hidráulico Verde (alimenta elevador izquierdo y motor de trim THS). ' +
    'El sistema transita de Normal Law a Alternate Law, perdiendo protecciones de envolvente. ' +
    'Los SEC asumen control de cabeceo y alabeo.\n\n' +
    'Durante descenso de emergencia, extensión de slats/flaps a velocidad reducida por fallo en un canal del SFCC. ' +
    'En Alternate Law, el piloto debe gestionar trimado manualmente si autotrim se afecta. ' +
    'Ante fallo adicional de SEC, el avión podría degradarse a Direct Law o requerir Mechanical Backup ' +
    '(ruedas de trim THS + cables del timón).\n\n' +
    'Instrucciones: Seleccione la respuesta correcta para cada pregunta derivada del caso. Cada pregunta vale 3 puntos.'
  );
  
  // CS1
  var cs1 = form.addListItem();
  cs1.setTitle('41. ¿Qué computadoras asumen el control de los elevadores tras la pérdida de ambos ELAC?');
  cs1.setPoints(3);
  cs1.setChoices([
    cs1.createChoice('FAC', false),
    cs1.createChoice('SEC', true),
    cs1.createChoice('SFCC', false),
    cs1.createChoice('FCDC', false)
  ]);
  cs1.setRequired(true);
  cs1.setFeedbackForCorrect(FormApp.createFeedback().setText('SEC asumen elevadores cuando ELAC fallan.').build());
  cs1.setFeedbackForIncorrect(FormApp.createFeedback().setText('SEC (Spoilers Elevator Computers) asumen el control.').build());
  
  // CS2
  var cs2 = form.addListItem();
  cs2.setTitle('42. ¿Cuáles son los tres sistemas hidráulicos del A320?');
  cs2.setPoints(3);
  cs2.setChoices([
    cs2.createChoice('Verde, Azul, Amarillo', true),
    cs2.createChoice('A, B, Standby', false),
    cs2.createChoice('Izquierdo, Derecho, Central', false),
    cs2.createChoice('Principal, Reserva, Emergencia', false)
  ]);
  cs2.setRequired(true);
  cs2.setFeedbackForCorrect(FormApp.createFeedback().setText('Green, Blue, Yellow = nomenclatura Airbus.').build());
  cs2.setFeedbackForIncorrect(FormApp.createFeedback().setText('Airbus usa Verde, Azul, Amarillo. A/B/Standby es nomenclatura Boeing.').build());
  
  // CS3
  var cs3 = form.addListItem();
  cs3.setTitle('43. ¿Qué sucede con las protecciones de envolvente al transitar a Alternate Law?');
  cs3.setPoints(3);
  cs3.setChoices([
    cs3.createChoice('Se mantienen intactas', false),
    cs3.createChoice('Se pierden o degradan', true),
    cs3.createChoice('Se refuerzan', false),
    cs3.createChoice('Solo se pierde high speed protection', false)
  ]);
  cs3.setRequired(true);
  cs3.setFeedbackForCorrect(FormApp.createFeedback().setText('Alternate Law degrada protecciones: AoA protection se pierde, lateral pasa a Direct Law.').build());
  cs3.setFeedbackForIncorrect(FormApp.createFeedback().setText('En Alternate Law se pierden o degradan protecciones de envolvente.').build());
  
  // CS4
  var cs4 = form.addListItem();
  cs4.setTitle('44. ¿Cómo se realiza el respaldo mecánico de cabeceo si fallan todos los computadores FBW?');
  cs4.setPoints(3);
  cs4.setChoices([
    cs4.createChoice('Sidestick directo a actuadores', false),
    cs4.createChoice('Ruedas de trim THS por cables', true),
    cs4.createChoice('Pedales del timón', false),
    cs4.createChoice('No hay respaldo de cabeceo', false)
  ]);
  cs4.setRequired(true);
  cs4.setFeedbackForCorrect(FormApp.createFeedback().setText('Mechanical Backup pitch = ruedas de trim THS operadas por cables mecánicos.').build());
  cs4.setFeedbackForIncorrect(FormApp.createFeedback().setText('Pitch mecánico = ruedas de trim THS. No hay control directo de elevadores sin computadores.').build());
  
  // CS5
  var cs5 = form.addListItem();
  cs5.setTitle('45. ¿Cuál es la función del motor eléctrico del THS controlado por ELAC2 en operación normal?');
  cs5.setPoints(3);
  cs5.setChoices([
    cs5.createChoice('Control de alerones', false),
    cs5.createChoice('Autotrim longitudinal', true),
    cs5.createChoice('Yaw damping', false),
    cs5.createChoice('Ground spoiler', false)
  ]);
  cs5.setRequired(true);
  cs5.setFeedbackForCorrect(FormApp.createFeedback().setText('ELAC2 ejecuta Autotrim para mantener equilibrio longitudinal sin intervención del piloto.').build());
  cs5.setFeedbackForIncorrect(FormApp.createFeedback().setText('Motor THS de ELAC2 = Autotrim longitudinal automático.').build());
  
  // CS6
  var cs6 = form.addListItem();
  cs6.setTitle('46. ¿Qué unidad controla y monitorea flaps y slats en el A320?');
  cs6.setPoints(3);
  cs6.setChoices([
    cs6.createChoice('ELAC', false),
    cs6.createChoice('SEC', false),
    cs6.createChoice('SFCC', true),
    cs6.createChoice('FSEU', false)
  ]);
  cs6.setRequired(true);
  cs6.setFeedbackForCorrect(FormApp.createFeedback().setText('SFCC = Slat Flap Control Computer, controla y monitorea dispositivos hipersustentadores.').build());
  cs6.setFeedbackForIncorrect(FormApp.createFeedback().setText('SFCC controla flaps/slats. FSEU es el equivalente en Boeing.').build());
  
  // CS7
  var cs7 = form.addListItem();
  cs7.setTitle('47. ¿Por qué el A320 no requiere stick shaker en Normal Law?');
  cs7.setPoints(3);
  cs7.setChoices([
    cs7.createChoice('Porque tiene alertas sonoras', false),
    cs7.createChoice('Porque hard limits impiden la pérdida por AoA', true),
    cs7.createChoice('Porque tiene MCAS', false),
    cs7.createChoice('Porque usa Alpha Floor exclusivamente', false)
  ]);
  cs7.setRequired(true);
  cs7.setFeedbackForCorrect(FormApp.createFeedback().setText('Normal Law impide físicamente la pérdida mediante limitación de AoA (alpha prot, alpha floor).').build());
  cs7.setFeedbackForIncorrect(FormApp.createFeedback().setText('Hard limits de Normal Law impiden entrar en pérdida. No se necesita stick shaker.').build());
  
  // CS8
  var cs8 = form.addListItem();
  cs8.setTitle('48. ¿Qué componente del B737 NG/MAX equivale funcionalmente al SFCC para monitoreo de asimetrías?');
  cs8.setPoints(3);
  cs8.setChoices([
    cs8.createChoice('SMYD', false),
    cs8.createChoice('FSEU', true),
    cs8.createChoice('FCC', false),
    cs8.createChoice('SCE', false)
  ]);
  cs8.setRequired(true);
  cs8.setFeedbackForCorrect(FormApp.createFeedback().setText('FSEU = Flaps/Slats Electronics Unit, equivalente Boeing al SFCC de Airbus.').build());
  cs8.setFeedbackForIncorrect(FormApp.createFeedback().setText('FSEU es el equivalente Boeing al SFCC de Airbus.').build());
  
  // CS9
  var cs9 = form.addListItem();
  cs9.setTitle('49. En Direct Law, ¿cuál es la relación entre sidestick y deflexión de superficie?');
  cs9.setPoints(3);
  cs9.setChoices([
    cs9.createChoice('Logarítmica', false),
    cs9.createChoice('Proporcional directa', true),
    cs9.createChoice('Inversa', false),
    cs9.createChoice('No hay relación', false)
  ]);
  cs9.setRequired(true);
  cs9.setFeedbackForCorrect(FormApp.createFeedback().setText('Direct Law = relación proporcional directa, sin protecciones ni autotrim.').build());
  cs9.setFeedbackForIncorrect(FormApp.createFeedback().setText('Direct Law: sidestick → superficie proporcionalmente, como sistema mecánico.').build());
  
  // CS10
  var cs10 = form.addListItem();
  cs10.setTitle('50. ¿Qué computador gestiona yaw damping en el A320?');
  cs10.setPoints(3);
  cs10.setChoices([
    cs10.createChoice('ELAC', false),
    cs10.createChoice('SEC', false),
    cs10.createChoice('FAC', true),
    cs10.createChoice('SFCC', false)
  ]);
  cs10.setRequired(true);
  cs10.setFeedbackForCorrect(FormApp.createFeedback().setText('FAC = Flight Augmentation Computer, gestiona yaw damping y rudder.').build());
  cs10.setFeedbackForIncorrect(FormApp.createFeedback().setText('FAC gestiona yaw damping. ELAC = pitch/roll, SEC = spoilers/elevators.').build());
  
  // CS11
  var cs11 = form.addListItem();
  cs11.setTitle('51. ¿Qué sensor proporciona retroalimentación de posición de superficie a los computadores?');
  cs11.setPoints(3);
  cs11.setChoices([
    cs11.createChoice('Pitot tube', false),
    cs11.createChoice('LVDT', true),
    cs11.createChoice('RVDT', false),
    cs11.createChoice('Strain gauge', false)
  ]);
  cs11.setRequired(true);
  cs11.setFeedbackForCorrect(FormApp.createFeedback().setText('LVDT = Linear Variable Differential Transformer, sensor de posición lineal.').build());
  cs11.setFeedbackForIncorrect(FormApp.createFeedback().setText('LVDT proporciona feedback de posición de superficies a los computadores.').build());
  
  // CS12
  var cs12 = form.addListItem();
  cs12.setTitle('52. ¿Principal diferencia FBW entre A320 y B777?');
  cs12.setPoints(3);
  cs12.setChoices([
    cs12.createChoice('A320 hard limits vs B777 soft limits', true),
    cs12.createChoice('A320 usa cables, B777 es 100% FBW', false),
    cs12.createChoice('B777 no tiene protecciones', false),
    cs12.createChoice('A320 no tiene respaldo mecánico', false)
  ]);
  cs12.setRequired(true);
  cs12.setFeedbackForCorrect(FormApp.createFeedback().setText('A320: límites rígidos (no sobrepasables). B777: límites blandos (piloto puede superar con fuerza).').build());
  cs12.setFeedbackForIncorrect(FormApp.createFeedback().setText('A320 = hard limits, B777 = soft limits. Filosofía de autoridad del piloto.').build());
  
  // CS13
  var cs13 = form.addListItem();
  cs13.setTitle('53. ¿Qué sistema hidráulico respalda el rudder del B737 si fallan A y B?');
  cs13.setPoints(3);
  cs13.setChoices([
    cs13.createChoice('Sistema Azul', false),
    cs13.createChoice('Sistema Standby', true),
    cs13.createChoice('Sistema Amarillo', false),
    cs13.createChoice('No hay respaldo', false)
  ]);
  cs13.setRequired(true);
  cs13.setFeedbackForCorrect(FormApp.createFeedback().setText('Standby Hydraulic System respalda rudder cuando A y B fallan.').build());
  cs13.setFeedbackForIncorrect(FormApp.createFeedback().setText('Standby es el respaldo hidráulico del rudder en B737.').build());
  
  // CS14
  var cs14 = form.addListItem();
  cs14.setTitle('54. ¿Cómo afecta la falla de un canal del SFCC a la operación de flaps?');
  cs14.setPoints(3);
  cs14.setChoices([
    cs14.createChoice('Flaps inoperativos', false),
    cs14.createChoice('Media velocidad', true),
    cs14.createChoice('Velocidad normal', false),
    cs14.createChoice('Solo se extienden, no retraen', false)
  ]);
  cs14.setRequired(true);
  cs14.setFeedbackForCorrect(FormApp.createFeedback().setText('Un canal SFCC fallido = flaps operan a media velocidad. Redundancia mantenida.').build());
  cs14.setFeedbackForIncorrect(FormApp.createFeedback().setText('Fallo de 1 canal SFCC = media velocidad. Ambos canales = velocidad normal.').build());
  
  // CS15
  var cs15 = form.addListItem();
  cs15.setTitle('55. ¿Qué componente mecánico del B737 permite separar columnas ante bloqueo?');
  cs15.setPoints(3);
  cs15.setChoices([
    cs15.createChoice('Shear pin', false),
    cs15.createChoice('Breakout clutch', true),
    cs15.createChoice('Torque limiter', false),
    cs15.createChoice('Override spring', false)
  ]);
  cs15.setRequired(true);
  cs15.setFeedbackForCorrect(FormApp.createFeedback().setText('Breakout clutch separa columnas con 50-80 lbs de fuerza ante bloqueo.').build());
  cs15.setFeedbackForIncorrect(FormApp.createFeedback().setText('Breakout clutch permite separar columnas de mando ante bloqueo del elevador.').build());
  
  // CS16
  var cs16 = form.addListItem();
  cs16.setTitle('56. ¿Presión nominal de los sistemas hidráulicos descritos?');
  cs16.setPoints(3);
  cs16.setChoices([
    cs16.createChoice('1,500 PSI', false),
    cs16.createChoice('2,500 PSI', false),
    cs16.createChoice('3,000 PSI', true),
    cs16.createChoice('5,000 PSI', false)
  ]);
  cs16.setRequired(true);
  cs16.setFeedbackForCorrect(FormApp.createFeedback().setText('3,000 PSI es la presión nominal estándar en aviación comercial.').build());
  cs16.setFeedbackForIncorrect(FormApp.createFeedback().setText('Presión nominal = 3,000 PSI.').build());
  
  // CS17
  var cs17 = form.addListItem();
  cs17.setTitle('57. ¿Qué aviso en ECAM/PFD indicaría discrepancia entre sensores de AoA?');
  cs17.setPoints(3);
  cs17.setChoices([
    cs17.createChoice('STALL WARNING', false),
    cs17.createChoice('AOA DISAGREE', true),
    cs17.createChoice('SENSOR FAULT', false),
    cs17.createChoice('PROBE HEAT', false)
  ]);
  cs17.setRequired(true);
  cs17.setFeedbackForCorrect(FormApp.createFeedback().setText('"AOA DISAGREE" alerta discrepancia entre sensores de ángulo de ataque.').build());
  cs17.setFeedbackForIncorrect(FormApp.createFeedback().setText('"AOA DISAGREE" es el mensaje de discrepancia de sensores de AoA.').build());
  
  // CS18
  var cs18 = form.addListItem();
  cs18.setTitle('58. ¿Qué superficie se usa en A320 para respaldo lateral en Mechanical Backup?');
  cs18.setPoints(3);
  cs18.setChoices([
    cs18.createChoice('Alerones', false),
    cs18.createChoice('Spoilers', false),
    cs18.createChoice('Rudder (pedales mecánicos)', true),
    cs18.createChoice('THS', false)
  ]);
  cs18.setRequired(true);
  cs18.setFeedbackForCorrect(FormApp.createFeedback().setText('En Mechanical Backup, solo rudder (pedales) proporciona control lateral inducido.').build());
  cs18.setFeedbackForIncorrect(FormApp.createFeedback().setText('Mechanical Backup lateral = rudder por pedales mecánicos. Alerones/spoilers inoperativos.').build());
  
  // CS19
  var cs19 = form.addListItem();
  cs19.setTitle('59. ¿Bajo qué FAR se certifica aterrizaje seguro tras fallos combinados?');
  cs19.setPoints(3);
  cs19.setChoices([
    cs19.createChoice('FAR 25.1309', false),
    cs19.createChoice('FAR 25.671', true),
    cs19.createChoice('FAR 25.143', false),
    cs19.createChoice('FAR 25.341', false)
  ]);
  cs19.setRequired(true);
  cs19.setFeedbackForCorrect(FormApp.createFeedback().setText('FAR 25.671 requiere capacidad de aterrizaje seguro tras fallos en controles de vuelo.').build());
  cs19.setFeedbackForIncorrect(FormApp.createFeedback().setText('FAR 25.671 = certificación de controles de vuelo y aterrizaje seguro tras fallos.').build());
  
  // CS20
  var cs20 = form.addListItem();
  cs20.setTitle('60. En el 737 MAX, ¿qué unidad reemplazó al mezclador mecánico para spoilers?');
  cs20.setPoints(3);
  cs20.setChoices([
    cs20.createChoice('FSEU', false),
    cs20.createChoice('SCE (Spoiler Control Electronics)', true),
    cs20.createChoice('SMYD', false),
    cs20.createChoice('FCC', false)
  ]);
  cs20.setRequired(true);
  cs20.setFeedbackForCorrect(FormApp.createFeedback().setText('SCE reemplazó el mezclador mecánico de spoilers en el MAX con control FBW.').build());
  cs20.setFeedbackForIncorrect(FormApp.createFeedback().setText('SCE = Spoiler Control Electronics, reemplazo FBW del mezclador mecánico en MAX.').build());
  
  // ================================================================
  // LOG
  // ================================================================
  
  Logger.log('========================================');
  Logger.log('EVALUACIÓN CREADA EXITOSAMENTE');
  Logger.log('========================================');
  Logger.log('URL del formulario: ' + form.getPublishedUrl());
  Logger.log('URL de edición: ' + form.getEditUrl());
  Logger.log('Total de preguntas: 60');
  Logger.log('Puntaje total: 200 puntos');
  Logger.log('Sección 1 (MC): 20 preguntas × 5 pts = 100 pts');
  Logger.log('Sección 2 (V/F): 20 preguntas × 2 pts = 40 pts');
  Logger.log('Sección 3 (Caso): 20 preguntas × 3 pts = 60 pts');
  Logger.log('========================================');
  
  return form;
}
