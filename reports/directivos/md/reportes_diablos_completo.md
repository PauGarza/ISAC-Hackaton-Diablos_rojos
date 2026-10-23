# Stuff+ en el Harp Helú: reportes para la toma de decisiones

**Diablos Rojos del México · Análisis de pitcheo** · Modelo Stuff+ LMB 2024–2026 · Estadio Alfredo Harp Helú, 2,240 m · Octubre 2026 · Paulina Garza Allende, Othoniel Reyes Camacho, Andrea Guerra y Jose Rodrigo Dumas Avalos

Cuatro reportes para la dirección deportiva y el cuerpo técnico, y dos anexos: el simulador y las referencias. Cada reporte abre con un resumen de 30 segundos y cierra con lo que significa para Diablos. Los números salen del modelo Stuff+ entrenado con los 629,616 pitcheos de la LMB 2024–2026.

1. **Stuff+ por pitcheo, pitcher y arsenal.** ¿Qué tan bueno es cada pitcheo, cada pitcher y cada arsenal en el Harp Helú, y cuánto le quita la altura?
2. **Perfil físico ideal para Diablos Rojos.** ¿Qué características físicas y qué arsenal maximizan el Stuff+ en el Harp Helú, y por qué importan más en altura?
3. **Recomendaciones operativas para el Harp Helú.** ¿Qué perfiles ganan y cuáles pierden en casa, qué riesgo de contacto duro y jonrón traen, y cómo perfilar a un prospecto o agente libre?
4. **Cómo funciona el modelo y cuánto confiar en él.** ¿Qué hay detrás del Stuff+ de Diablos, cómo se validó y hasta dónde llega?
- **Anexo A. Simulador Stuff+ Harp Helú: cómo funciona y cómo se usa.** ¿Cómo se usa la herramienta para comparar un pitcheo en el Harp Helú contra nivel del mar y tomar decisiones con ella?
- **Anexo B. Referencias.** Las fuentes, los datos y las herramientas detrás de estos reportes.

**Cómo leer los números.** Se leen como ERA+ u OPS+: 100 es el promedio de la LMB y más alto siempre es mejor para el pitcher; 120 o más es élite. La escala completa, con su equivalente en grados de scout, está al inicio del reporte 1. *Ambiente Harp Helú* quiere decir cómo quedaría cada pitcher en el ranking de la liga si todos lanzaran en el Harp Helú, como ajustar la efectividad por parque. Los pitchers aparecen con su clave anónima de los datos de ISAC; los equipos y estadios los inferimos por récord y ISAC no los ha confirmado.

**Cinco palabras que se repiten.** *Stuff+, Location+, Pitching+*: qué tan buena es la bola, qué tan bien se ubicó y el pitcheo completo. *Bote* (IVB, el "ride"): cuánto se resiste la recta a caer por el backspin; una recta de 18 pulgadas parece que sube, una de 10 se ve "plana". *Corrida* (HB, el "run"): cuánto se mueve la pelota hacia los lados; en el cambio es el desvanecimiento. *Efecto Magnus*: el empuje que da el giro y que produce el bote y la corrida; en el aire delgado es más débil. *Castigo de altura*: cuántas carreras de más permite un pitcheo en el Harp Helú contra el mismo pitcheo a nivel del mar.

---

# 01 · Stuff+ por pitcheo, pitcher y arsenal

*¿Qué tan bueno es cada pitcheo, cada pitcher y cada arsenal en el Harp Helú, y cuánto le quita la altura?*

> **En 30 segundos**
>
> - Calificamos cada uno de los **629,616 pitcheos** de la LMB 2024–2026 con tres números: **Stuff+** (el brazo), **Location+** (la ubicación) y **Pitching+** (todo junto). 100 es el promedio de la liga.
> - **La altura le quita al pitcheo lo que el giro le da.** El mismo pitcheo vale en promedio **6 a 7 puntos menos por cada 1,000 m**. En el Harp Helú la recta pierde **22 puntos** y el slider solo **9**.
> - **El arsenal que más vale en casa es cutter + slider** (Stuff+ 115 en el Harp Helú contra 98 a nivel del mar). El que más sufre es recta + cambio sin rompiente.
> - **En el staff 2026**, los relevistas 01099, 00638 y 00315 son los que mejor rinden en ambiente Harp Helú.

## Cómo leer los tres números

Los tres scores responden la misma pregunta: si este pitcheo se lanzara mil veces, ¿cuántas carreras le quitaría al rival comparado con un pitcheo promedio de la liga? No importa si ese lanzamiento en particular terminó en hit o en out; importa qué tan difícil es de batear.

| Score | Qué mira | En palabras de dugout | Para qué sirve |
|---|---|---|---|
| **Stuff+** | Solo la física al soltar la pelota: velocidad, giro, movimiento, release, extensión y cómo se separa de la recta del mismo pitcher | "¿Qué tan buena es la bola?" Lo que ve el scout con la pistola y el TrackMan | Evaluar el brazo y el arsenal |
| **Location+** | Solo dónde cruzó el plato, en qué cuenta y contra qué mano | "¿La puso donde debía?" El comando | Evaluar la ejecución |
| **Pitching+** | Todo junto, más el cansancio (número de pitcheo y de bateadores enfrentados) | "¿Qué tan bueno fue el pitcheo completo?" | Evaluar el resultado esperado de cada lanzamiento |

**La escala se lee como ERA+ u OPS+:** 100 es el promedio de la LMB y más alto siempre es mejor para el pitcher, sin importar si es una recta o una curva. Cada 10 puntos separan a un pitcheo promedio de uno claramente mejor: un 110 está arriba del 84 % de la liga y un 120 está entre el 3 % mejor. En carreras, 10 puntos de Stuff+ equivalen a unas 1.3 carreras menos por cada 100 pitcheos, más o menos lo que lanza un abridor en una salida larga.

**Truco para el scout:** Stuff+ menos 50 da el grado en la escala 20–80. Un Stuff+ de 110 es un pitcheo de 60; uno de 120, un 70.

| Stuff+ | Lectura | Grado de scout (20–80) | Cuántos pitcheos de la liga llegan ahí |
|---|---|---|---|
| 120 o más | Élite | 70 o más | Más o menos 3 de cada 100 |
| 110 a 119 | Arriba del promedio | 60 | 1 de cada 7 |
| 91 a 109 | Promedio | 45–55 | 2 de cada 3 |
| 81 a 90 | Abajo del promedio | 40 | 1 de cada 7 |
| 80 o menos | Nivel de reemplazo | 30 | Más o menos 3 de cada 100 |

Esta es la escala que pide el reto. El mismo 100 + 10 puntos aplica a Location+ y Pitching+, y al ranking de pitchers en *ambiente Harp Helú*: ahí 120 quiere decir "de los mejores de la liga si todos lanzaran en el Harp Helú".

## Score de cada lanzamiento

Cada pitcheo trae su Stuff+, Location+ y Pitching+ en el ambiente donde se lanzó, y además su Stuff+ si se hubiera lanzado a nivel del mar y en el Harp Helú con la misma mecánica. Así se ve, por ejemplo, el relevista **00315** de Diablos en el Harp Helú en 2026:

| Pitcheo | Velocidad | Cuenta | Resultado | Stuff+ | Location+ | Pitching+ | Stuff+ si fuera a nivel del mar |
|---|---|---|---|---|---|---|---|
| Slider | 84.9 mph | 0-1 | Swing y fallo | 111 | 97 | 102 | 115 |
| Slider | 86.1 mph | 1-2 | En juego | 109 | 102 | 108 | 117 |
| Sinker | 93.5 mph | 0-0 | Strike cantado | 90 | 102 | 103 | 97 |
| Recta | 93.7 mph | 0-0 | Swing y fallo | 94 | 107 | 108 | 113 |

**Qué se lee aquí:** su slider es arriba del promedio aun en casa. Su recta sería un pitcheo de 60 en la costa (113), pero en el Harp Helú baja a promedio (94): la altura le quita casi 20 puntos. Lo que salva a esa recta es la ubicación (Location+ 107).

> **Un aviso para el cuerpo técnico.** Un solo pitcheo dice poco, igual que un solo turno al bat no dice si un bateador es bueno: un batazo de 70 mph puede caer de hit y una línea de 105 puede ser out. El valor del Stuff+ aparece al juntar cientos de pitcheos de un pitcher o de un tipo de pitcheo. Por eso las decisiones de este reporte se toman con promedios, no con lanzamientos sueltos.

## Cuánto le quita la altura a cada tipo de pitcheo

![El mismo pitcheo vale menos en el Harp Helú](../graficas/r1_stuff_por_tipo.png)

Tomamos cada pitcheo de la liga y lo evaluamos dos veces con la misma mecánica: a nivel del mar y a 2,240 m. Todos pierden, pero no lo mismo.

- **Los que más pierden son recta (−22), sinker (−16) y cambio (−15).** Viven del movimiento que da el giro: el bote de la recta y la corrida del sinker y del cambio. En el aire delgado ese movimiento se reduce.
- **Los que menos pierden son slider, sweeper y curva (−9) y cutter (−10).** Engañan sobre todo por la diferencia de velocidad con la recta y por el ángulo con que llegan, y eso la altura no lo cambia.

## El Harp Helú contra los otros estadios de la LMB

![Cada 1,000 m de altura le quitan unos 6 puntos al pitcheo](../graficas/r1_stuff_por_estadio.png)

| Estadio | Altitud | Stuff+ medio | Carreras por 100 pitcheos (real) |
|---|---|---|---|
| **Harp Helú (Diablos)** | **2,240 m** | **94.4** | **+0.87** |
| Hermanos Serdán (Puebla) | 2,135 m | 95.1 | +0.55 |
| Francisco Villa (Durango) | 1,890 m | 95.6 | +0.52 |
| Alberto Romo Chávez (Aguascalientes) | 1,880 m | 93.9 | +1.02 |
| Revolución (Torreón) | 1,120 m | 99.7 | −0.03 |
| Monclova | 600 m | 102.1 | −0.36 |
| Chevron (Tijuana) | 20 m | 108.5 | −1.12 |
| Promedio de los 7 parques de costa | ≤ 170 m | 106.5 | −0.93 |

**Cómo se cuantifica el efecto altitud.** Entre el parque más bajo y el Harp Helú hay **14 puntos de Stuff+ de diferencia**, y la tendencia es de **6.7 puntos por cada 1,000 m**. En carreras, el pitcheo en el Harp Helú permite casi **2 carreras más por cada 100 pitcheos** que en la costa. Dicho en el dugout: el mismo abridor, con la misma salida de 100 pitcheos, sale con casi dos carreras más en la pizarra en casa que en Tijuana. El reporte 4 muestra que el modelo anticipa bien este efecto con pitchers reales.

> **Ojo con los nombres de los estadios.** Los datos de ISAC solo dicen si un juego fue en altura baja, media o extrema. Los equipos y sus estadios los identificamos por el récord y por qué pitchers lanzan juntos; ISAC no los ha confirmado. La altitud de cada parque es la del estadio que identificamos.

> **Qué significa para Diablos.** El efecto no es exclusivo de la Ciudad de México: todos los parques de altura bajan el pitcheo. La diferencia es que Diablos juega ahí la mitad de su temporada, así que para su staff no es un ajuste de una serie sino la condición normal de trabajo.

## Qué arsenal produce el Stuff+ más alto en el Harp Helú

![Cutter + slider: el arsenal que más vale en el Harp Helú](../graficas/r1_arsenales.png)

Agrupamos a los 601 pitchers con al menos 300 pitcheos según su recta principal, su rompiente principal y si usan un cambio de velocidad. Luego calificamos a toda la liga como si todos lanzaran en el Harp Helú.

| Arsenal | Pitchers | Harp Helú | Nivel del mar | Qué pasa |
|---|---|---|---|---|
| **Cutter + slider** | 13 | **115** | 98 | Mediocre en la costa, el mejor en casa |
| Sinker + slider | 71 | 109 | 101 | Sube 8 puntos en el ranking |
| Cutter + slider + cambio | 10 | 102 | 88 | Sube 14 puntos en el ranking |
| Recta + slider | 186 | 103 | 103 | Se mantiene |
| Recta + cambio, sin rompiente | 14 | 96 | **107** | Bueno en la costa, de los peores en casa |
| Recta + curva + cambio | 35 | 92 | 96 | El más bajo en casa |

**La respuesta:** el arsenal que más Stuff+ produce en el Harp Helú es **cutter + slider**, porque ninguno de los dos pitcheos depende del movimiento por giro. La proporción de rompientes lo confirma: los pitchers con más de 50 % de sliders y curvas ganan 13 puntos en el ranking del Harp Helú, y los que lanzan menos de 20 % pierden 6. El cutter + slider se apoya en solo 13 pitchers, así que su 115 es una señal fuerte, pero no una cifra exacta.

## Por pitcher: el staff 2026 de Diablos en casa

![Staff 2026 de Diablos ordenado para jugar en casa](../graficas/r1_staff_2026.png)

La gráfica ordena a los pitchers que lanzaron para Diablos en 2026 por su Pitching+ si toda la liga lanzara en el Harp Helú. Es como ajustar la efectividad por parque: compara a todos en la misma cancha. El número de la derecha dice cuántos puntos sube o baja en el ranking contra nivel del mar.

- **Los mejores en casa son tres relevistas:** 01099 (127, sube 22), 00638 (124) y 00315 (117, sube 12). Los tres tienen una recta, sinker o cutter de poco bote, y un slider o curva de mucho giro.
- **Los que más bajan en casa** son 00503 (−5), 00258 (−4) y 00198 (−3). Viven de rectas y sinkers con mucho bote y corrida.
- **Ningún abridor 2026 está arriba de 106.** La rotación de casa es el punto débil del staff actual, y es donde más rinde fichar el perfil del reporte 2.

> **Una nota sobre el staff.** Los datos van de 2024 a 2026, y varios pitchers que fueron Diablos ya no están. 00619 y 01060 solo lanzaron para Diablos en 2024. 00778 se fue a Tigres en 2025 y 00069 a Saraperos en 2026. Por eso este reporte solo usa el staff 2026 para las decisiones, y a los demás los cita como ejemplos del perfil que conviene buscar.

---

# 02 · Perfil físico ideal para Diablos Rojos

*¿Qué características físicas y qué arsenal maximizan el Stuff+ en el Harp Helú, y por qué importan más en altura?*

> **En 30 segundos**
>
> - **El pitcher ideal para el Harp Helú es el que no necesita el aire para ser bueno:** una recta o cutter de poco bote, un slider o curva de mucho giro, muchos rompientes y batazos al suelo.
> - **El rasgo que más pesa es el bote vertical**, el "ride" que hace que la recta parezca subir. Entre menos depende el arsenal del bote, más sube el pitcher en casa; es la relación más fuerte que encontramos. Los pitchers con bote promedio menor a 6 pulgadas ganan entre 5 y 7 puntos en el ranking del Harp Helú; los de más de 12 pierden 8.
> - **Es casi el opuesto de lo que se busca en Grandes Ligas.** Allá se paga la recta de mucho bote arriba de la zona, y aquí esa es la que más pierde. Por eso Diablos puede encontrar valor en pitchers que el mercado subestima.
> - **En la liga hay candidatos que ya cumplen el perfil**, sobre todo para la rotación, que es lo que más le falta al staff 2026.

## Por qué la altura cambia lo que importa

A 2,240 m el aire es cerca de 20 % menos denso que a nivel del mar. Es lo mismo que pasa en Coors Field, en Denver, pero 600 m más arriba. Eso tiene tres efectos sobre el pitcheo, y los tres apuntan al mismo perfil.

| Qué cambia | Qué le pasa a la pelota | Qué medimos en la LMB |
|---|---|---|
| **Menos fuerza Magnus** (el empuje que da el giro: lo que hace que la recta "suba" y que el sinker corra) | El pitcheo se mueve menos. El bote de la recta y la corrida del sinker y del cambio se encogen | El mismo pitcher pierde 4.8 in de bote y 3.4 in de corrida en la recta, y 5 in de corrida en el cambio |
| **Menos arrastre** | La pelota frena menos en su camino al plato y la bateada viaja más lejos | La recta frena 1.5 mph menos. Un elevado viaja de 10 a 35 pies más |
| **La gravedad no cambia** | La caída que viene de la gravedad, y no del giro, se mantiene | Slider y curva conservan su separación de velocidad y su ángulo de llegada |

La consecuencia es directa: **en altura todos los pitcheos se parecen más a una pelota sin giro.** El que dependía de moverse pierde más, y el que engaña por velocidad, separación y ángulo pierde menos.

![Mapa de movimiento: todo se encoge hacia el centro](../graficas/r2_mapa_movimiento.png)

En el mapa cada punto es una forma de pitcheo de la LMB a nivel del mar, y la flecha marca a dónde llega en el Harp Helú. Las rectas, arriba a la derecha, recorren el camino más largo hacia el centro y pierden de 20 a 25 puntos. Los sliders casi no se mueven y pierden de 7 a 9.

## Qué rasgos ayudan y cuáles estorban

![Qué rasgos ayudan y cuáles estorban en la altura](../graficas/r2_rasgos.png)

Para cada uno de los 601 pitchers con al menos 300 pitcheos calculamos cuánto sube o baja en el ranking de la liga si todos lanzaran en el Harp Helú. Después medimos qué rasgos acompañan a los que suben.

![Entre menos depende del bote, más gana en casa](../graficas/r2_bote_vs_ganancia.png)

| Bote vertical promedio del arsenal | Pitchers | Puntos que gana en el Harp Helú |
|---|---|---|
| Menos de 3 in | 30 | **+6.5** |
| 3 a 6 in | 102 | +5.4 |
| 6 a 9 in | 252 | +1.4 |
| 9 a 12 in | 171 | −2.8 |
| Más de 12 in | 46 | **−8.3** |

| % de rodados en bolas en juego | Pitchers | Puntos que gana en el Harp Helú |
|---|---|---|
| Menos de 40 % | 238 | −2.0 |
| 45 a 50 % | 105 | +1.7 |
| 50 a 55 % | 53 | +5.0 |
| Más de 55 % | 44 | **+5.8** |

**Por qué importa cada rasgo en altura.** Entre paréntesis va la correlación: qué tanto acompaña ese rasgo a los pitchers que suben en casa. Va de −1 a +1. Cerca de 0 quiere decir que no tiene que ver; más allá de ±0.5 es una relación fuerte. Con signo negativo, entre más tiene el pitcher de ese rasgo, más pierde en casa.

- **Poco bote (correlación −0.62, la más fuerte).** El bote es Magnus puro: quien no lo tiene no lo pierde, y su recta se ve igual en casa que de visita. A nivel del mar la recta de 16 a 18 pulgadas de bote vale 118. En el Harp Helú vale 80, por debajo de la recta de menos de 12 pulgadas, que vale 86.
- **Poca corrida lateral (−0.37).** También es Magnus. La corrida grande del sinker y del cambio es lo primero que desaparece.
- **Muchos rodados (+0.39).** Con la misma velocidad de salida y el mismo ángulo, un elevado vale +0.087 carreras más en el Harp Helú y un rodado solo +0.046. Por cada 100 elevados son casi 9 carreras extra; por cada 100 rodados, menos de 5. El rodado pierde la mitad.
- **Mucho giro en cutter, slider y curva (+0.26).** En estos pitcheos el giro no sostiene la pelota, le da forma. La cuarta parte de los sliders con más giro (más de 2,580 rpm) valen 116 en el Harp Helú, contra 111 los de menos giro. En el cutter la diferencia es mayor: 112 contra 102.
- **Velocidad (−0.01).** No distingue quién sube o baja, porque vale lo mismo arriba y abajo. Pero sigue sumando: en la recta y la curva más velocidad es más Stuff+ en cualquier parque. Es un requisito, no un diferenciador.
- **Mano.** Los zurdos suben 1.8 puntos en promedio y los derechos se quedan igual. Es un efecto chico: desempata, no decide.

## Qué pesa más dentro del modelo

Para saber qué variables físicas mueven el Stuff+ usamos valores SHAP. La idea es la misma que repartir el crédito de un rally entre los bateadores que participaron: a cada pitcheo le repartimos su score entre sus ingredientes (velocidad, giro, movimiento…) y vemos cuántos puntos aporta cada uno.

| Variable | Puntos de Stuff+ que mueve en promedio | Lectura |
|---|---|---|
| Altitud del parque | 4.6 | La que más pesa: +5 en la costa, −5 arriba de 1,500 m |
| Separación de velocidad con la recta | 2.5 | Lo que más define a un cambio (4.1) y a un slider (2.8) |
| Desvío entre el eje de giro y el movimiento | 2.4 | El efecto de la costura. En rectas y cutters, más desvío es mejor |
| Velocidad | 1.4 | En la curva pesa 3 puntos |
| Movimiento total | 1.2 | Ayuda en recta y sinker, pero es justo lo que la altura quita |
| Giro por sí solo | 0.7 | Pesa poco: importa qué forma le da a la pelota, no cuánto gira |

**La lectura para el cuerpo técnico:** los rasgos que la altura no toca (separación de velocidad, efecto de la costura, velocidad) pesan más que el giro en sí. Ahí está el margen de un pitcher en casa. Un cambio con 8 a 12 mph de separación con su recta vale unos 10 puntos más que uno con menos de 6, y la altura les quita lo mismo a los dos. El primero llega al Harp Helú con colchón; el segundo queda muy por debajo del promedio.

## La ficha del pitcher ideal para Diablos

| Componente | Qué buscar | Por qué |
|---|---|---|
| **Recta** | Poco bote (menos de 12 in) o, mejor, un cutter de 88 a 91 mph | No pierde lo que no tiene. La recta de mucho bote es la que más sufre |
| **Rompiente principal** | Slider o curva de mucho giro, con buena separación de velocidad con su recta | Pierde 9 puntos, contra 22 de la recta |
| **Mezcla** | Más de 35 % de rompientes; ideal, cerca de 50 % | Con más de 50 % suben 13 puntos en el ranking; con menos de 20 % bajan 6 |
| **Batazo** | Más de 50 % de rodados en bolas en juego | El rodado no vuela; el elevado sí |
| **Cambio** | Si lo usa: firme, de poca corrida y siempre abajo | El cambio de poca corrida pierde 12; el de mucha corrida, 17 |
| **Velocidad** | La más alta posible | No la quita la altura y suma en cualquier parque |
| **Mano** | Zurdo, si todo lo demás empata | Ventaja chica, de 1 a 2 puntos |

**En una frase:** velocidad, un cutter o una recta plana, un slider de mucho giro y un batazo que va al suelo.

**El arsenal que más rinde con este perfil es cutter + slider:** 115 de Stuff+ en el Harp Helú, el más alto de la liga (ver reporte 1).

## Quién cumple el perfil

**Ejemplos que ya pasaron por Diablos.** 00619 fue el mejor pitcher de la liga en ambiente Harp Helú (Pitching+ 137) y 01060 el séptimo (124). Los dos son abridores con recta de poco bote. Solo lanzaron para Diablos en 2024, pero muestran que el perfil funciona en casa.

**En el staff 2026.** Los relevistas 01099 (zurdo: cutter, slider y curva; sube 22 puntos), 00638 (cutter y curva) y 00315 (sinker de poco bote, slider y 57 % de rodados) son el perfil en su versión más pura.

**En otros equipos de la LMB, entre el top 30 de la liga en ambiente Harp Helú:**

| Pitcher | Equipo (inferido) | Rol | Mano | Velocidad media | Bote medio | Rodados | Pitching+ en ambiente Harp Helú | Sube en casa |
|---|---|---|---|---|---|---|---|---|
| 00222 | Tecos | Relevista | Zurdo | 84.6 | 0.7 in | 53 % | 129 | +14 |
| 01075 | Guerreros | Relevista | Zurdo | 87.8 | 3.8 in | 52 % | 125 | +17 |
| 00548 | Toros | Relevista | Zurdo | 83.8 | 1.8 in | 46 % | 127 | +7 |
| 00682 | Pericos | Relevista | Zurdo | 87.8 | 4.6 in | 53 % | 118 | +19 |
| **00019** | **Pericos** | **Abridor** | Derecho | 87.4 | 3.9 in | 47 % | **120** | +6 |
| **00081** | **Algodoneros** | **Abridor** | Derecho | 87.5 | 6.2 in | 46 % | **118** | +6 |
| **00844** | **Tecos** | **Abridor** | Derecho | 89.8 | 6.3 in | 51 % | **115** | +1 |

> **Qué significa para Diablos.** El staff 2026 ya tiene el perfil en el bullpen, pero no en la rotación: ningún abridor 2026 pasa de 106 en ambiente Harp Helú. Los tres abridores de la tabla (00019, 00081 y 00844) serían, con estos datos, la primera lista para buscar por cambio o agencia libre. Velocidad media se refiere a todo el arsenal, no solo a la recta. El equipo de cada pitcher lo inferimos de los datos anónimos; hay que confirmarlo antes de iniciar cualquier plática.

---

# 03 · Recomendaciones operativas para el Harp Helú

*¿Qué perfiles ganan y cuáles pierden en casa, qué riesgo de contacto duro y jonrón traen, y cómo perfilar a un prospecto o agente libre?*

> **En 30 segundos**
>
> - **En casa ganan los rompientes y el cutter; pierden la recta de mucho bote, el sinker de mucha corrida y el cambio de mucho desvanecimiento.** El slider pierde 7 a 9 puntos; la recta de mucho bote, 20 a 25.
> - **El riesgo de jonrón en casa está en el cambio y el splitter, no en la recta.** El cambio permite 1.16 jonrones por 100 pitcheos en el Harp Helú contra 0.70 a nivel del mar. Slider y cutter casi no cambian.
> - **Diablos hace bien con el cutter en casa, pero tira menos sliders en casa que de visita (18 % contra 24 %).** Es al revés de lo que conviene. Corregirlo es la recomendación más barata de este reporte.
> - **Una ficha de cinco preguntas y un procedimiento de cinco pasos** para decidir sobre un prospecto o un agente libre con los datos del TrackMan.

## 1. Qué formas ganan y cuáles pierden en casa

![Qué formas aguantan la altura y cuáles no](../graficas/r3_formas.png)

El modelo no usa la etiqueta del pitcheo, sino su forma: velocidad, bote, corrida y giro. Agrupamos los pitcheos de la liga en 14 formas y medimos cuánto pierde cada una si se lanza en el Harp Helú con la misma mecánica.

| Ganan valor relativo en casa | Pierden valor relativo en casa |
|---|---|
| **Slider de caída hacia el guante** (81 mph): pierde solo 7 | **Recta de mucho bote y corrida** (93 mph, 17 in de bote): pierde 25 |
| **Sliders rectos y cutters** (84 a 88 mph): pierden 8 a 9 | **Cualquier recta de más de 16 in de bote**: pierde 20 |
| **Curvas** de cualquier velocidad: pierden 10 | **Cambio de mucho desvanecimiento** (15 in de corrida): pierde 17 |
| **Cambio firme de poca corrida** (82 mph, 4 in): pierde 12 | **Sinker de mucha corrida** (92 mph, 15 in): pierde 16 |

**La regla general:** dentro de cada tipo de pitcheo, entre más movimiento depende del giro, más se pierde en casa. Un pitcher que vive de la recta con bote o del sinker con corrida es un buen pitcher de visita y uno común en casa.

## 2. Riesgo de contacto duro y jonrón

![Dónde está el riesgo de jonrón en casa](../graficas/r3_riesgo_hr.png)

Datos reales de la liga: lo que pasó con cada tipo de pitcheo en el Harp Helú contra los parques de menos de 700 m.

| Pitcheo | Contacto duro (95+ mph) Harp Helú | Nivel del mar | Jonrones por 100 pitcheos Harp Helú | Nivel del mar | Distancia del elevado (pies) |
|---|---|---|---|---|---|
| **Cambio** | **26.1 %** | 18.2 % | **1.16** | 0.70 | 295 contra 263 |
| **Splitter** | 22.2 % | 16.5 % | **0.98** | 0.45 | 280 contra 265 |
| Recta | 29.1 % | 23.0 % | 0.81 | 0.71 | 294 contra 260 |
| Curva | 20.9 % | 16.8 % | 0.62 | 0.46 | 280 contra 262 |
| Sinker | 28.2 % | 23.2 % | 0.57 | 0.60 | 283 contra 266 |
| Slider | 20.1 % | 18.1 % | 0.65 | 0.62 | 275 contra 257 |
| Cutter | 21.5 % | 19.7 % | 0.66 | 0.77 | 270 contra 260 |

**Qué se lee aquí:**

- **El cambio es el pitcheo más peligroso en casa.** Cuando el cambio pierde su desvanecimiento se convierte en una recta lenta: sube el contacto duro 8 puntos y casi duplica los jonrones. Lo mismo con el splitter (pocos datos, pero misma dirección).
- **La recta recibe más contacto duro** (29 %), pero sus jonrones suben poco. El elevado viaja 34 pies más, que es la diferencia entre la pista de advertencia y la barda.
- **Slider y cutter son los pitcheos más seguros en casa.** Su contacto duro y sus jonrones casi no cambian con la altura.
- **El sinker no sube en jonrones** porque su contacto va al suelo. Pierde Stuff+, pero su batazo es el menos castigado.

> **Ojo.** En el Harp Helú hay pocos cambios y splitters (3,691 y 919 pitcheos). La dirección es clara y coincide con la física, pero los porcentajes exactos tienen margen.

## 3. Dónde lanzar en casa

![Dónde castiga más la altura](../graficas/r3_zona.png)

El mapa muestra cuánto cambia el Pitching+ en cada parte de la zona entre el Harp Helú y nivel del mar, vista desde el catcher.

- **El centro de la zona es donde más se pierde:** −7 para rectas y −8 para cambios. Un error al centro en casa cuesta más que en la costa, porque el contacto viaja más.
- **Abajo y fuera de la zona casi no se pierde nada.** Sin contacto no hay acarreo.
- **Para el cuerpo técnico:** rompientes y cambios abajo; la recta, si se usa, en las esquinas o arriba y afuera, nunca al centro.

## 4. La mezcla de Diablos en casa

![Diablos lanza menos sliders en casa](../graficas/r3_mezcla.png)

| Pitcheo | En el Harp Helú | De visita | Qué conviene en casa |
|---|---|---|---|
| Recta | 33.0 % | 29.9 % | **Bajar.** Es el pitcheo que más pierde, y Diablos lo usa más en casa |
| Sinker | 18.2 % | 18.2 % | Mantener o bajar un poco |
| **Slider** | **17.7 %** | **23.8 %** | **Subir.** El que menos pierde, y Diablos lo usa menos en casa |
| Cutter | 10.8 % | 4.9 % | Bien. Ya lo usan más en casa |
| Curva | 8.5 % | 8.3 % | Subir un poco |
| Cambio | 7.5 % | 12.0 % | Bien que baje, y solo el firme y abajo |

La recomendación es mover **5 a 10 puntos de recta hacia slider y cutter en casa**. En el Harp Helú el slider promedio vale 102 de Stuff+ y la recta 88: cada 100 pitcheos que pasan de recta a slider valen cerca de **1.5 a 2 carreras menos** para el rival. Es lo máximo que se puede esperar, no lo seguro: el slider rinde en parte porque el bateador tiene que respetar la recta, así que no conviene quitarla del todo.

### Pitcher por pitcher (staff 2026)

Para cada pitcher del staff 2026 comparamos cada pitcheo de su arsenal contra su propio promedio en ambiente Harp Helú. Solo incluimos pitcheos con al menos 40 lanzamientos.

| Pitcher | Usar más en casa | Usar menos en casa | El dato que lo dice |
|---|---|---|---|
| **00078** | Slider | — | Su slider vale 120 en casa y lo usa 6 % en casa contra 25 % de visita |
| **00904** | Slider, cutter, sweeper | Recta | Usa el slider 13 % en casa contra 34 % de visita. Su recta vale 94 en casa |
| **00096** | Slider, sweeper, curva | — | Sus rompientes valen 114 a 120, pero el sinker es 72 % de su mezcla |
| **00315** | Slider | Sinker | Su slider vale 126, el mejor pitcheo del staff en casa |
| **01101** | Slider | Sinker, recta | Slider de 120; ya lo usa 30 % y puede subir |
| **00638** | Cutter, curva | Recta, sinker | Ya usa el cutter 36 % en casa. Bien |
| **00258** | Slider | Sinker | Slider de 117 contra sinker de 91 |
| **00503** | Slider | Recta, sinker | Usa el sinker 26 % en casa contra 8 % de visita: al revés |
| **00860** | Slider | Recta | Recta de 97, slider de 117 |
| **01134** | Cutter, slider, splitter | Recta, sinker | Sinker y recta valen 88 a 89 en casa |
| **00710** | Slider, curva | Recta, sinker | Sinker de 83 en casa |
| **00941** | Slider, cambio | Recta, sinker | Recta y sinker de 84 en casa |
| **01099** | Mantener | — | Ya es el perfil ideal: cutter, slider y curva todos arriba de 113 |
| **00198** | Slider | Sinker | Uso bajo del sinker; ajuste menor |

> **Qué significa para Diablos.** Casi todo el staff tiene un slider de 110 a 126 en ambiente Harp Helú, y casi todos lo usan menos en casa que de visita. No hace falta fichar a nadie para mejorar en casa: hace falta usar más lo que ya tienen.

## 5. Cuánta confianza tener en cada pitcher

![Castigo esperado en altura por tipo de pitcheo](../graficas/r3_castigo_bayes.png)

Un bateador que se va de 10-5 en abril no es un bateador de .500; con pocos turnos, lo sensato es suponer que está más cerca del promedio de la liga hasta que acumule más. Hacemos lo mismo con el castigo de altura. Un modelo bayesiano jerárquico (estimado con MCMC) calcula cuánto pierde cada pitcher con cada pitcheo al subir de altura. Si el pitcher tiene pocos lanzamientos en altura, el modelo lo juzga casi como al promedio de su pitcheo; si tiene cientos, lo juzga por lo suyo.

- **El slider es el pitcheo con menos castigo y el más parejo entre pitchers:** 0.9 carreras por 100 pitcheos en promedio, y casi todos los sliders de la liga quedan entre 0.6 y 1.1.
- **Cambio, sinker y recta tienen castigos altos (1.7 a 2.0 carreras por 100) y cambian mucho de un pitcher a otro:** depende de la forma de cada uno. Ahí conviene revisar caso por caso con el simulador (anexo A).
- **Para cada pitcher, el modelo calcula la probabilidad de que su castigo pase de 3 carreras por 100 pitcheos**, que equivale a bajar unos 24 puntos de Stuff+: un pitcheo de 60 en la costa que en casa queda por debajo de 40. Es la columna que conviene ver antes de decidir quién abre en casa.

## 6. Cómo perfilar a un prospecto o agente libre

### Las cinco preguntas

| Pregunta | Dato que se necesita | Señal verde | Señal roja |
|---|---|---|---|
| **1. ¿De qué vive su recta?** | Bote vertical (IVB) y corrida (HB) | Menos de 12 in de bote, o cutter | Más de 16 in de bote: pierde 20 puntos |
| **2. ¿Tiene un rompiente de verdad?** | Giro y separación de velocidad del slider o curva | Slider de más de 2,500 rpm y 8 a 12 mph debajo de su recta | Sin rompiente, o con menos de 20 % de uso |
| **3. ¿A dónde va su contacto?** | % de rodados en bolas en juego | 50 % o más | Menos de 40 % de rodados |
| **4. ¿Cómo es su cambio?** | Corrida y separación de velocidad | Firme, poca corrida, siempre abajo | Mucha corrida y lo deja al centro: riesgo de jonrón |
| **5. ¿Ya lanzó en altura?** | Sus pitcheos en Puebla, Durango, Aguascalientes o CDMX | Su castigo observado es menor al del modelo | Pierde más de 3 carreras por 100 |

### El procedimiento

1. **Con datos de TrackMan del pitcher** (de LMB, MLB, ligas menores o una sesión de bullpen), meter cada pitcheo en el simulador: velocidad, giro, bote, corrida, release y extensión.
2. **Leer su Stuff+ en el Harp Helú y su pérdida contra nivel del mar.** Compararlo con el staff actual y con el promedio de la liga en ambiente Harp Helú.
3. **Pasarlo por las cinco preguntas.** Tres o más señales verdes es un perfil para Diablos.
4. **Si ya lanzó en altura, comparar** lo que predijo el modelo con lo que pasó. El modelo bayesiano de la sección 5 ya lo hace para los pitchers de la LMB.
5. **Ajustar el rol.** Un perfil verde con mucho volumen es abridor de casa. Un pitcher bueno pero de recta con bote se cuida para las series de visita.

> **Un ejemplo con Grandes Ligas.** Jacob Misiorowski y Chad Patrick pierden lo mismo de bote en su recta (unas 4 in), pero a Misiorowski le cuesta 5 puntos y a Patrick 12, porque 100 mph protegen la recta. La velocidad no evita la pérdida, pero deja más colchón. Por eso la pregunta 1 no se responde solo con el bote: una recta de mucho bote con velocidad de élite todavía puede servir en casa.

---

# 04 · Cómo funciona el modelo y cuánto confiar en él

*¿Qué hay detrás del Stuff+ de Diablos, cómo se validó y hasta dónde llega?*

> **En 30 segundos**
>
> - **Este reporte es la lectura ejecutiva del documento técnico** de 10 páginas que acompaña este reporte. Explica qué decisiones se tomaron, cómo se probó el modelo y qué no puede hacer, sin necesidad de saber estadística.
> - **El modelo acierta con pitchers, temporadas y parques que no vio.** Para tener una referencia: la efectividad de un pitcher en un año apenas anticipa la del siguiente (correlación de 0.23 a 0.29). El Stuff+ y el Pitching+, con datos que nunca vieron, llegan a 0.42 a 0.66. La referencia que propone el reto ni siquiera ordena a los pitchers en la dirección correcta.
> - **El Stuff+ se sostiene de un año a otro** (0.61 a 0.68): mide al brazo, no a la suerte. Y el Pitching+ de este año anticipa las carreras del año siguiente mejor que las propias carreras de este año.
> - **El efecto de la altura se comprobó con pitchers reales:** el modelo predijo 1.5 carreras más por 100 pitcheos en altura y en el campo fueron 1.7.

## La idea en una página

**Qué medimos.** Cuántas carreras le quita cada pitcheo al rival comparado con un pitcheo promedio de la LMB. No usamos el resultado del turno, que depende mucho de la suerte y de la defensa: un roletazo débil puede colarse de hit y una línea puede ir directo al guante. Usamos el valor esperado de lo que pasa con el pitcheo: bola, strike, swing y fallo, foul o pelota en juego, y qué tan bien se le pega (velocidad de salida y ángulo).

**Cómo lo medimos.** Con tres modelos de aprendizaje automático (LightGBM). Cada uno ve distinta información, igual que un scout, un coach de pitcheo y un mánager miran cosas distintas del mismo lanzamiento:

| Modelo | Qué ve | Qué no ve, a propósito |
|---|---|---|
| **Stuff+** | La física al soltar la pelota y la altitud del parque | Ubicación, cuenta y etiqueta del pitcheo |
| **Location+** | Dónde cruzó, la cuenta y la mano de pitcher y bateador | La física |
| **Pitching+** | Todo, más el cansancio | — |

**Qué predice cada modelo.** El reto pide estimar varias probabilidades. Así las cubrimos:

| Lo que pide el reto | Cómo sale del modelo |
|---|---|
| Swing y fallo (whiff) y strike cantado | Directo: el modelo predice qué pasa con el pitcheo (bola, strike cantado, swing y fallo, foul, en juego, golpe) |
| Swing fuera de la zona (chase) | De la probabilidad de swing en los pitcheos que cruzan fuera de la zona; necesita la ubicación, así que sale de Pitching+ |
| Rodado | Directo: probabilidad de rodado cuando hay contacto |
| Contacto duro o barril | Directo como contacto de 95 mph o más; no usamos la definición estricta de barril |
| Contacto débil | Dentro del valor esperado del contacto, que se calcula con velocidad de salida y ángulo |
| Out en el turno | Ponche más out en bola en juego |
| Valor esperado en carreras (xRunValue) | Es el número que se convierte en Stuff+ |

**Cómo metimos la altura.** De dos formas que se complementan:

1. **La altitud entra como dato** al modelo, así que aprende cuánto vale el mismo pitcheo en cada parque.
2. **Un traslado físico del movimiento.** Medimos a los mismos pitchers en parques bajos y altos y calculamos cuánto bote y cuánta corrida pierde cada tipo de pitcheo por cada kilómetro de altura. Así podemos llevar cualquier pitcheo al Harp Helú o a nivel del mar y comparar.

**La escala.** 100 es el promedio de la LMB, como en ERA+ u OPS+; la escala completa está en el reporte 1.

## Seis decisiones que vale la pena conocer

| Decisión | Por qué |
|---|---|
| **No usar la etiqueta del pitcheo** | El clasificador llama "slider" a cuatro formas distintas con Stuff+ de 106 a 112. El modelo califica cómo se mueve la pelota, no cómo se llama |
| **Comparar cada pitcheo contra la recta del mismo pitcher** | Un cambio vale por lo que se separa de la recta en velocidad y movimiento; solo no dice mucho |
| **Calcular nuestros propios valores de carrera para la LMB** | La LMB produce más carreras que MLB, así que un out o un sencillo valen distinto, y la altura cambia cuánto vale cada batazo |
| **Quitar el fildeo** | El valor del batazo se calcula con velocidad de salida y ángulo, no con si el fildeador lo atrapó |
| **El 100 se ajusta por temporada, no por estadio** | El reto propone ajustar por temporada y estadio. Ajustamos por temporada (cada año tiene su propio 100), pero no por estadio, a propósito: si cada parque tuviera su propio 100, el efecto de la altura desaparecería del número. Para comparar a todos en la misma cancha usamos el ranking en *ambiente Harp Helú*, que sí pone a todos en el mismo parque |
| **Agregar un modelo bayesiano (MCMC)** | Para que un pitcher con pocos pitcheos en altura no reciba un castigo extremo por pura suerte, igual que no se juzga a un bateador por 20 turnos |

## Cómo sabemos que funciona

![El modelo acierta con datos que no vio](../graficas/r5_validacion.png)

Probamos el modelo de tres formas, siempre con datos que no usó para aprender. La medida es la correlación entre lo que el modelo esperaba de cada pitcher (con 200 pitcheos o más) y las carreras que en realidad permitió: 1 sería acertar siempre, 0 sería tirar una moneda.

- **Pitchers nuevos.** Como calificar a un pitcher que acaba de llegar a la liga: entrenamos con el 85 % de los pitchers y calificamos al 15 % que el modelo nunca vio lanzar. Stuff+: 0.44. Esta prueba se corrió solo para Stuff+.
- **Temporada nueva.** Como hacer las proyecciones en el spring training: entrenamos con 2024 y 2025 y pronosticamos 2026. Stuff+ 0.42 y Pitching+ 0.56.
- **El Harp Helú apartado.** Entrenamos sin ningún pitcheo del Harp Helú y calificamos los que se lanzaron ahí (35 pitchers). Stuff+ 0.66 y Pitching+ 0.62. Es la prueba más importante para Diablos: el modelo funciona en su parque sin haberlo visto.

**La referencia del reto** le pone a cada pitcheo el valor promedio de la cuenta en que se lanzó. Sabe si el pitcher iba 3-0 o 0-2, pero no cómo es la bola. Por eso no separa a un pitcher bueno de uno malo: por pitcher, su correlación con las carreras reales sale negativa (−0.26 en 2026 y −0.20 en el Harp Helú), es decir, ni siquiera los ordena en la dirección correcta.

**Error en carreras.** Por pitcher, la referencia del reto se equivoca en promedio por 1.84 carreras por cada 100 pitcheos al estimar lo que permitió en 2026. El Stuff+ baja ese error a 1.75 y el Pitching+ a 1.59. Pitcheo por pitcheo la diferencia es mínima (el Stuff+ casi empata con la referencia), porque un pitcheo suelto es casi pura suerte.

![El Stuff+ se repite y anticipa las carreras](../graficas/r5_estabilidad.png)

**Estabilidad.** El Stuff+ de un pitcher se repite de un año a otro (0.61 a 0.68), mucho más que sus carreras permitidas (0.23 a 0.29). Y el Pitching+ de este año predice las carreras del año siguiente (0.31 a 0.38) mejor que las propias carreras de este año. **Para firmar o renovar, el Pitching+ dice más que la efectividad.**

**El efecto altitud, comprobado.** Tomamos 150 pitchers que lanzaron tanto arriba de 1,800 m como abajo de 700 m. El modelo predijo que en altura permitirían 1.5 carreras más por 100 pitcheos; en la realidad fueron 1.7.

**Calibración: el modelo no exagera ni se queda corto.** Cuando el Pitching+ dice que un grupo de pitcheos vale 5 carreras, en el campo valió 5: la relación entre lo esperado y lo real es 1.00 en la temporada nueva y 0.99 en el Harp Helú apartado (1.00 es lo ideal). El Stuff+ da 0.95 en la temporada nueva, pero 1.30 en el Harp Helú apartado: ahí las diferencias reales entre pitcheos buenos y malos fueron cerca de 30 % más grandes que lo que esperaba el modelo. Lo leemos como que el Stuff+ ordena bien en casa, pero se queda corto en el tamaño de la diferencia.

## Las cuatro hipótesis del reto

| Hipótesis | Resultado | Evidencia, en términos de béisbol |
|---|---|---|
| **H1.** En altura hay menos movimiento por giro | **Se confirma** | El mismo pitcher pierde 4.8 pulgadas de bote en la recta en el Harp Helú; el giro y la velocidad no cambian. La recta "sube" menos |
| **H2.** El cambio gana valor relativo | **No se cumple** | Pierde menos que la recta (−15 contra −22), pero más que los rompientes, y le batean más fuerte: el contacto duro sube de 18 % a 26 % y los jonrones, de 0.70 a 1.16 por cada 100 cambios |
| **H3.** Los pitchers de rodados valen más | **Se confirma** | En casa, un elevado vale casi el doble de carreras extra que un rodado; los pitchers de rodados son los que suben en el ranking |
| **H4.** El giro solo no basta | **Se confirma** | Con solo velocidad y giro, el modelo acierta la mitad de lo que acierta con la forma completa del pitcheo. Importa cómo se mueve, no cuánto gira |

## Hasta dónde llega el modelo

- **Un pitcheo suelto dice poco.** A nivel de un solo pitcheo el Stuff+ mejora apenas 1.5 % sobre adivinar siempre lo mismo. Es normal: en MLB pasa lo mismo. El valor aparece al juntar cientos de pitcheos, por eso las decisiones de estos reportes usan promedios por pitcher y por tipo de pitcheo.
- **Las pruebas con datos nuevos tienen huecos.** La prueba con pitchers nuevos solo se corrió para Stuff+, no para Location+ ni Pitching+. La prueba por parque solo apartó al Harp Helú, no a cada estadio de la liga.
- **Hay datos que el reto sugiere y no usamos:** el efecto túnel (qué tan parecido sale cada pitcheo del mismo punto que la recta), el porcentaje de uso de cada pitcheo, el pitcheo anterior en la secuencia, la entrada y los corredores en base. El modelo sí compara cada pitcheo contra la recta del pitcher en velocidad, bote, corrida y eje de giro.
- **El Harp Helú y los equipos se identificaron por récord.** Los datos vienen anónimos y solo dicen si el parque es de altura baja, media o extrema. Diablos es el equipo con mejor récord en 2024 y 2025, y su parque de casa coincide con el Harp Helú. La altitud de cada parque es la del estadio que identificamos. Es muy probable, pero ISAC no lo confirmó.
- **El cambio y el slider pierden en altura más movimiento del que explica solo el aire.** Puede haber efectos de costura, de qué pitchers lanzan en altura o de cómo se calibra el TrackMan en cada parque. El modelo usa lo medido, no lo teórico.
- **Pocos datos de splitter.** Sus cifras tienen más margen que las del resto.
- **No hay datos de clima.** Temperatura, humedad y viento cambian la densidad del aire de un día a otro; el modelo usa la altitud del parque como promedio.

## Qué sigue

1. **Agregar el clima del día** para ajustar la densidad del aire por juego.
2. **Agregar el efecto túnel, el uso de cada pitcheo y la secuencia**, y repetir la prueba de pitchers nuevos para Location+ y Pitching+.
3. **Actualizar los scores cada mes** durante la temporada 2027, para seguir al staff y a los candidatos.
4. **Conectar el simulador con los datos de TrackMan del bullpen**, para calificar sesiones de práctica.

---

# Anexo A · Simulador Stuff+ Harp Helú: cómo funciona y cómo se usa

*¿Cómo se usa la herramienta para comparar un pitcheo en el Harp Helú contra nivel del mar y tomar decisiones con ella?*

> **En 30 segundos**
>
> - **El simulador responde una pregunta: ¿cuánto vale este pitcheo en casa?** Se meten los datos de TrackMan de un pitcheo y devuelve su Stuff+ en el Harp Helú y a nivel del mar, cuánto pierde y por qué.
> - **Tres vistas:** el score lado a lado, la vista desde el catcher (dónde cruza el mismo lanzamiento en cada parque) y el mapa de movimiento contra toda la liga.
> - **Usa el mismo modelo de los reportes 1 a 4.** No es una aproximación aparte: es el modelo final del equipo dentro de una página.
> - **Funciona en el navegador, sin instalar nada**, en computadora o celular: <https://claude.ai/artifact/KYU5KNKmTSzew9CFQMMRhd>. También hay una copia en un solo archivo HTML que abre sin internet.

![El simulador completo](../graficas/r4_app_completa.png)

## Para qué sirve

| Quién | Pregunta | Qué mirar en el simulador |
|---|---|---|
| **Dirección deportiva** | ¿Fichamos a este pitcher para casa? | Stuff+ en el Harp Helú de cada pitcheo de su arsenal, y cuánto pierde contra nivel del mar |
| **Coach de pitcheo** | ¿Qué pitcheo usar más en casa? | El pitcheo que menos pierde y el que queda más alto en el Harp Helú |
| **Mánager** | ¿Quién abre en casa y quién de visita? | La diferencia entre los dos scores: el que más pierde, mejor de visita |
| **Scouting** | ¿Este prospecto aguanta la altura? | Su forma contra la liga en el mapa de movimiento |

## Paso 1: meter el pitcheo

![Los datos que pide el simulador](../graficas/r4_formulario.png)

Todos los datos salen directamente de un reporte de TrackMan o Hawk-Eye:

- **Tipo de pitcheo y mano del pitcher.** El tipo solo sirve para comparar contra la media de su tipo; el modelo califica la forma, no la etiqueta.
- **Release:** velocidad, giro, eje de giro, extensión, altura y posición lateral de salida.
- **Movimiento:** bote vertical (IVB) y corrida (HB). Hay que indicar dónde se midió, en el Harp Helú o a nivel del mar, y el simulador traslada el movimiento al otro parque con la física de la altura.
- **Recta primaria del pitcher.** El modelo compara cada pitcheo contra la recta del mismo pitcher (separación de velocidad y de movimiento). Si el pitcheo es la recta, se marca la casilla.

## Paso 2: leer el resultado

![El resultado: el mismo pitcheo en los dos parques](../graficas/r4_resultado.png)

En este ejemplo metimos la recta de Jacob Misiorowski (99.6 mph, 16 in de bote medido a nivel del mar):

- **Las dos tarjetas** dan el Stuff+ en el Harp Helú (99) y a nivel del mar (104), con su etiqueta en la escala del reporte 1 y el movimiento en cada parque. Pierde 4 in de bote y 3.7 de corrida.
- **El texto de abajo** dice cuánto pierde (4.9 puntos) y lo compara con la media de su tipo: las rectas de la liga pierden 22. Esta aguanta mejor por su velocidad.
- **Los tres números chicos** separan la pérdida: cuánto viene del movimiento que quita el aire delgado, cuánto del entorno del parque, y cómo le va contra bateadores del mismo lado y del lado contrario.

## Paso 3: ver dónde cruza el plato

![Vista desde el catcher](../graficas/r4_catcher.png)

Esta es la vista para el cuerpo técnico. El mismo lanzamiento, con la misma mecánica y apuntado al mismo lugar: la bola azul cruza donde la pidió el catcher a nivel del mar y la roja muestra dónde cruza en el Harp Helú.

- **En este ejemplo la recta cruza 4 in más abajo y 3.7 in hacia el guante.** Una recta que arriba de la zona saca swings y fallos en la costa, en casa cae a la altura del bate.
- **Se puede hacer clic en la zona** para cambiar a dónde se apunta, y el botón *Lanzar* repite la animación.
- **Sirve para explicar al pitcher** por qué su recta "no sube" en casa, con una imagen que entiende en segundos.

## Paso 4: compararlo con la liga

![Mapa de movimiento](../graficas/r4_mapa.png)

Cada punto es un pitcher de la LMB con un tipo de pitcheo. Los verdes son el 10 % más efectivo de la liga y los naranjas el 10 % menos efectivo. El punto azul es el pitcheo a nivel del mar y el rojo el mismo pitcheo en el Harp Helú.

**Qué se lee aquí:** en el Harp Helú la recta de Misiorowski se mueve hacia el centro del grupo de rectas, que es la zona naranja. A nivel del mar estaba en una orilla del grupo, que es donde está el valor. El filtro de arriba deja ver solo un tipo de pitcheo.

## Tres casos de uso

**Caso 1. Evaluar a un agente libre.** Meter cada pitcheo de su arsenal con sus datos de TrackMan. Si su mejor pitcheo en el Harp Helú pasa de 107 y su peor pitcheo no baja de 93, es un pitcher que funciona en casa. Pasarlo después por las cinco preguntas del reporte 3.

**Caso 2. Ajustar la mezcla de un pitcher del staff.** Meter su recta y su slider. Si la recta pierde 15 o más y el slider menos de 10, conviene subir el slider en casa. Es el caso de casi todo el staff 2026 (reporte 3).

**Caso 3. Preparar una junta con el pitcher.** Abrir la vista desde el catcher con su propia recta y mostrar dónde cruza en casa. Es la forma más rápida de que acepte un cambio de plan.

## Lo que el simulador no hace

- **No predice el resultado de un turno.** Califica la calidad física del pitcheo. Un solo pitcheo de 110 puede terminar en jonrón; el valor aparece en promedio.
- **No toma en cuenta la ubicación.** Para eso está el Location+ del reporte 1. El simulador mide el brazo, no el comando.
- **Los pitcheos raros tienen más margen.** Si una forma casi no existe en la LMB (por ejemplo, una recta de 100 mph), el modelo tiene pocos ejemplos parecidos y su score es menos preciso.
- **Los datos de Grandes Ligas se traducen, no se copian.** Los TrackMan de MLB miden a la altura de cada parque; hay que marcar *Medido a nivel del mar* para los parques bajos.

## Cómo abrirlo

- **En línea:** <https://claude.ai/artifact/KYU5KNKmTSzew9CFQMMRhd>
- **Sin internet:** el archivo `simulador_standalone.html` que acompaña este reporte. Se abre con doble clic en cualquier navegador.

---

# Anexo B · Referencias

*Las fuentes, los datos y las herramientas detrás de estos reportes.*

## Física de la altitud y béisbol

- Nathan, A. M. (2008). The effect of spin on the flight of a baseball. *American Journal of Physics*, 76(2), 119–124.
- Richardson, E. (2014). High Altitude Offense. *Baseball Research Journal*, SABR.

## Métodos estadísticos

- Deshpande, S. K. y Wyner, A. J. (2017). A hierarchical Bayesian model of pitch framing. arXiv:1704.00823.
- Brill, R. S., Deshpande, S. K. y Wyner, A. J. (2022). A Bayesian analysis of the time through the order penalty in baseball. arXiv:2210.06724.
- Hoffman, M. D. y Gelman, A. (2014). The No-U-Turn Sampler: adaptively setting path lengths in Hamiltonian Monte Carlo. *Journal of Machine Learning Research*, 15, 1593–1623.
- Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q. y Liu, T.-Y. (2017). LightGBM: A highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30.
- Lundberg, S. M. y Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30.

## Software

- LightGBM (modelos Stuff+, Location+ y Pitching+), pandas y scikit-learn, en Python.
- PyMC 5 y ArviZ (modelo bayesiano jerárquico, estimado con MCMC por el muestreador NUTS).

## Datos

- ISAC y Diablos Rojos del México (2026). Datos pitcheo a pitcheo de la Liga Mexicana de Béisbol, temporadas 2024 a 2026 (TrackMan), con identificadores anonimizados. Proporcionados para el 2026 ISAC Hackathon.
- ISAC (2026). *2026 ISAC Hackathon – Diablos Rojos: Stuff Plus Model, Calidad de Pitcheo Ajustada por Entorno*. Bases del reto, de donde salen la escala Stuff+, las hipótesis H1 a H4 y los entregables.
- Datos públicos de Grandes Ligas de Jacob Misiorowski y Chad Patrick, usados solo como ejemplo en el reporte 3 y en el anexo A. Las entradas son aproximadas: el giro, el eje y el movimiento horizontal los estimamos nosotros.

## Herramientas de inteligencia artificial

- Anthropic (2026). *Claude Code* [asistente de inteligencia artificial]. https://claude.com/claude-code. Lo usamos como apoyo para programar el análisis y el simulador, revisar la congruencia entre resultados y reportes, y redactar y editar los reportes.
- El simulador en línea está publicado como artifact de Claude (claude.ai).
