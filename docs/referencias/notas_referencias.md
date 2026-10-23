# Notas de referencias — Stuff+ ajustado por altitud

Resumen de lo que dice cada fuente del reto (y algunas extra) y **qué implica para nuestro modelo y nuestro EDA**.

---

## 1. Física: qué le hace la altitud a un pitch

### Idea central (Alan Nathan, física del béisbol)
- Sobre una pelota en vuelo actúan tres fuerzas: **gravedad**, **arrastre** (resistencia del aire, la frena) y **Magnus** (el spin "empuja" la pelota y genera el movimiento: el ride del four-seam, la caída de la curva, el run del sinker).
- El arrastre y Magnus son **proporcionales a la densidad del aire (ρ)**. La gravedad no cambia.
- Con menos densidad, **todos los pitches se parecen más a una pelota sin spin** (trayectoria de "solo gravedad"):
  - Four-seam: pierde ride (cae más).
  - Sinker / changeup: pierden run y caída inducida.
  - Curva: cae **menos** (pierde su ventaja).
  - Slider: según un análisis de FanGraphs en Coors, es el que menos cambia.
- **Coors Field (1,609 m):** ρ ≈ 82% de nivel del mar. La curva pierde ~18–25% de movimiento (≈4 pulgadas menos de caída). La pelota pierde ~8% de velocidad en su camino a home vs ~10% al nivel del mar, así que llega ~1 mph más rápida.
- **Harp Helú (2,240 m):** esperamos ρ ≈ 0.76–0.80 de nivel del mar (depende de la temperatura), o sea, **un efecto mayor que en Coors**.

### Lo que ya se ve en nuestros datos (primer vistazo)
| | No Altitude | Medium | Extreme |
|---|---|---|---|
| % de velocidad perdida (four-seam) | 8.4% | 7.4% | 6.9% |
| IVB sinker (pulg.) | 10.0 | 8.8 | 8.0 |
| IVB changeup | 7.3 | 5.9 | 5.2 |
| IVB curva | −8.0 | −7.1 | −6.4 |

La razón 6.9 / 8.4 ≈ 0.82 encaja con la física. Pero **ojo**: estas son comparaciones crudas; falta controlar quién lanza en cada parque (lo hacemos en el EDA comparando al mismo pitcher en distintos ambientes).

### SABR — *High Altitude Offense* (Eliza Richardson)
- Datos: ligas menores (Rookie / Short Season A), 2008–2012, 26 estadios de 13 a 5,150 pies.
- Por cada pie de altitud: +5.6×10⁻⁴ carreras/juego y +1.2×10⁻⁴ HR/juego. A 5,000 pies eso es ≈ **+2.8 carreras/juego** y +0.6 HR/juego.
- **La fracción de carreras que viene de HR no cambia con la altitud (~21%).** La mayoría de las carreras extra vienen de **más hits y errores**, no de jonrones.
- Modelos numéricos citados: 10% menos densidad ⇒ hasta 9% menos quiebre de curva. El cambio es **sobre todo vertical**.
- Coors antes del humidor: +66% HR vs los Rockies como visitantes.
- **Limitaciones:** no controla viento, temperatura ni humedad; es correlacional; ligas menores. **CDMX (≈7,350 pies) está fuera del rango estudiado**: usar estas pendientes para CDMX es extrapolar.
- **Implicación para H3:** no basta con ver HR; hay que revisar BABIP / hits en rolling vs elevado.

---

## 2. Sabermetría: cómo se construye un Stuff+

### Tango, Lichtman & Dolphin — *The Book* (2007)
- Base de **run expectancy** (carreras esperadas según el estado del juego), **linear weights** (cuánto vale cada evento) y el **valor de cada cuenta** (un 3-0 vale más para el bateador que un 0-2).
- Regresión a la media: con muestras chicas, los números de un pitcher están muy influidos por el azar ⇒ hay que fijar **umbrales mínimos de pitches**.
- **Implicación:** nuestro target principal (xRunValue) se construye como cambio en run expectancy por pitch. Como no tenemos corredores en base, usamos la versión RE(outs, cuenta).

### FanGraphs — primer de Stuff+ / Location+ / Pitching+
- **Stuff+**: solo características físicas (velo, movimiento, spin, release, extensión). Se entrena contra run value.
- **Location+**: solo dónde cruzó el pitch el plato (no la intención del catcher).
- **Pitching+**: combina ambos con el contexto.
- Los pitches secundarios se evalúan **en relación con el fastball principal** del pitcher (diferenciales de velocidad y movimiento).
- Estabilidad: Stuff+ se vuelve confiable con ~80 pitches; Location+ con ~400.
- **Implicación:** separar estrictamente las features de Stuff+ (físicas) de las de Location+ (ubicación, cuenta). El diccionario de datos ya marca cuáles son cuáles.

---

## 3. Papers académicos del reto

### Brill, Deshpande & Wyner (2022) — penalidad por veces en el orden (TTOP)
- Modelo bayesiano multinomial que ajusta por calidad del bateador y del pitcher, mano y localía.
- Hallazgo: el pitcher empeora **gradualmente** durante el juego; no hay un "salto" especial al empezar la tercera vuelta.
- **Implicación:** (a) ajustar los resultados por la calidad del bateador; (b) tratar la fatiga y el número de pitch como algo continuo; (c) es un buen ejemplo de cómo aislar un efecto de sus confusores.

### Deshpande & Wyner (2017) — modelo jerárquico de framing
- Modelo bayesiano jerárquico de P(strike cantado) que ajusta por catcher, pitcher, bateador, umpire, ubicación y cuenta; convierte el efecto del catcher a carreras.
- **Implicación:** `P(called_strike)` no depende solo del pitch: el catcher (tenemos `catcher_anon_id`) y el umpire influyen. Los modelos jerárquicos (*partial pooling*) ayudan con pitchers de LMB con poca muestra.

### Ahn et al. (2026) — *Neural sabermetrics*
- Un LLM entrenado como "modelo del mundo" sobre más de 7 millones de secuencias de pitches de MLB (~3 mil millones de tokens).
- Predice el siguiente pitch dentro de un turno con ~64% de acierto y la decisión de swing con ~78%.
- **Implicación:** la secuencia (`prev_pitch_type`) y la decisión de swing tienen señal real. Nuestras filas vienen en orden, así que podemos reconstruirla.

### McBride (2026) — descomposición Shapley del rendimiento de pitcheo
- **No pude leerlo (el sitio bloquea la descarga automática; pendiente de leer a mano).**
- La idea general: repartir el rendimiento entre componentes usando valores de Shapley. Es el mismo principio que **SHAP**, que usaremos para explicarle al pitching coach qué empuja cada score.

### Huang & Hsu (2021) — SAGE Open
- ⚠️ El PDF del reto lo cita para H4 ("el spin solo no basta"), pero el artículo parece ser *"A Multidisciplinary Perspective on Publicly Available Sports Data in the Era of Big Data: A Scoping Review of the Literature on MLB"*: una revisión de 48 papers que usan datos públicos de MLB (PITCHf/x, Lahman, Baseball-Reference). **El resumen no menciona spin.**
- **Acción:** antes de citarlo en el documento técnico, verificar el texto completo. Para respaldar H4 es más sólido usar la física de Nathan y la idea de "shape over spin" de FanGraphs/Driveline.

---

## 4. Cosas a tener en cuenta (resumen)
1. **Comparar al mismo pitcher entre ambientes**: 665 pitchers lanzaron en las tres categorías de altitud. Es nuestra mejor forma de aislar el efecto de la altitud.
2. **SpinAxis / Tilt de Trackman** suelen calcularse a partir del movimiento observado ⇒ ya traen "metido" el efecto de la altitud. Lo preguntamos a ISAC.
3. Sin corredores en base ⇒ run expectancy aproximado por (outs, cuenta).
4. Sin estadio ⇒ inferimos la densidad del aire por juego con la pérdida de velocidad del four-seam.
5. **Los datos no se pueden publicar** (solo los resultados); por eso `data/` está en `.gitignore`.

## Fuentes
- PDF del reto: https://www.isac-app.com/competition-details/hackathon-diablos-rojos.html
- SABR, High Altitude Offense: https://sabr.org/journal/article/high-altitude-offense/
- Brill et al. 2022: https://arxiv.org/abs/2210.06724
- Deshpande & Wyner 2017: https://arxiv.org/abs/1704.00823
- Ahn et al. 2026: https://arxiv.org/abs/2602.07030
- McBride 2026: https://doi.org/10.3390/g17020015
- Huang & Hsu 2021: https://journals.sagepub.com/doi/10.1177/21582440211061566 (ficha: https://ideas.repec.org/a/sae/sagope/v11y2021i4p21582440211061566.html)
- FanGraphs, Stuff+/Location+/Pitching+ primer: https://library.fangraphs.com/pitching/stuff-location-and-pitching-primer
- FanGraphs Community, An Analysis of Pitch Movement at Coors Field: https://community.fangraphs.com/an-analysis-of-pitch-movement-at-coors-field/
- Kagan & Nathan, arrastre: https://physics.csuchico.edu/kagan/professional/papers/drag.pdf
- Colorado Sun (Nathan sobre Coors): https://coloradosun.com/?p=343242
