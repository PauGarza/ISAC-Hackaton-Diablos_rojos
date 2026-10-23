# Identificación de Harp Helú y de Diablos (datos indirectos)

Fecha: 2026-10-17. Archivo resultante: `juegos_equipo_local.csv` (una fila por `game_anon_id`: `year`, `home_team`, `away_team`, `diablos_home`, `diablos_away`, `harp_helu`, `altitude_category`). Los IDs de equipo (`2024_T8`, etc.) son por temporada y no se conservan entre años.

## Método
1. **Equipos anónimos.** En `Top` lanza el equipo local y en `Bottom` el visitante. Se armó un grafo de pitchers que lanzan en el mismo lado del mismo juego y se detectaron comunidades (Louvain, resolución 2.0), lo que da 20 equipos por temporada. Cada juego queda con equipo local y visitante. El 99.5 % de los juegos de cada equipo local cae en una sola `altitude_category`. Scripts: `t1.py`.
2. **Densidad del aire por estadio.** Para rectas y sinkers, se proyectó la aceleración sin gravedad (`ax0, ay0, az0+32.174`) sobre la velocidad, se dividió entre v² (∝ ρ·Cd) y se ajustaron efectos fijos de pitcher×tipo + parque. Scripts: `t3.py`.
3. **Récord por equipo.** Carreras por media entrada (`RunsScored`) → ganador de cada juego → G-P, CA y CE. Se unieron los equipos entre temporadas por traslape de pitchers. Script: `t5.py`.

## Resultado: Diablos = 2024_T8 → 2025_T11 → 2026_T1

| Temporada | Equipo | Local | G-P (datos) | CA-CE | Altitud | Liga a temporada siguiente |
|---|---|---|---|---|---|---|
| 2024 | T8 | 51 | **72-20** | 682-409 | Extreme | 2025_T11 (32 % de pitchers compartidos) |
| 2025 | T11 | 50 | **68-21** | 728-498 | Extreme | 2026_T1 (46 %) |
| 2026 | T1 | 27 | 33-22 | 421-343 | Extreme | — |

En 2024 y 2025 es el mejor récord de la liga por mucho (el segundo apenas pasa de .58), y juega de local en un parque Extreme. Esto coincide con lo público: Diablos fue primer lugar general en 2024 y ganó la Serie del Rey en 2024 (vs. Sultanes) y en 2025 (barrida a Charros). Los juegos incluyen postemporada, por eso suman ~95 juegos.

**Harp Helú = juegos de local de ese equipo:** 128 juegos (51 / 50 / 27) y 39,321 pitcheos, todos en `Extreme Altitude`.

## Advertencias
- **La física sola no lo distingue.** Por arrastre, el parque de Diablos queda segundo en "menos densidad" entre los Extreme. Otro equipo (2024_T4 → 2025_T13 → 2026_T8) sale ~1–2 % menos denso, aunque CDMX es el más alto. La diferencia es chica y la confunden la temperatura y la pelota; probablemente ese otro parque es Puebla u otro de altura similar. La identificación descansa en el récord, no en la física.
- 2026 es parcial y Diablos no domina tan claramente (es 2.º-3.º); la identificación ahí se apoya en la continuidad de pitchers (46 %).
- Hay ~57 juegos con empate en carreras, que en realidad son juegos con pitcheos faltantes. Eso mueve los récords unos pocos juegos, no la conclusión.
- Para confirmarlo al 100 %, cruzar con las posiciones oficiales (G-P, CA, CE) de cada temporada. Esa misma tabla permitiría nombrar a los 20 equipos y sus estadios.

## Actualización: los 20 equipos con nombre (con las tablas de posiciones 2024 y 2025 que pasó Otho)
Archivo: `equipos_identificados.csv` (team_id por temporada → equipo, zona, ciudad, estadio, altitud, confianza). `juegos_equipo_local.csv` ahora trae `home_equipo`, `away_equipo`, `estadio`, `altitud_m` y `confianza_estadio`.

Método (`m2.py`–`m4.py`):
1. **Zona**: se partió el grafo de enfrentamientos en dos. 721 juegos quedan dentro de zona y 112 cruzados, y la mitad con Diablos es la Sur.
2. **Celda zona × altitud**: con la altitud de cada ciudad (≥1,800 m = Extreme, 1,000–1,800 = Medium, <1,000 = No), el número de equipos anónimos en cada celda coincide exactamente con la liga real (Sur: 4 Extreme, 1 Medium, 5 No; Norte: 2, 4, 4).
3. **Linajes**: se unió cada equipo 2024 → 2025 → 2026 por pitchers compartidos. Los 20 linajes caen en la misma celda en las tres temporadas, lo que sirve como validación independiente.
4. **Nombre**: dentro de cada celda se asignaron nombres minimizando la diferencia de PCT (datos vs. tabla) sumada 2024 + 2025.

Confianza:
- **Alta**: Diablos, Guerreros (único Sur-Medium), Caliente y Rieleros (PCT muy distintos), Toros (además es el parque más denso de toda la liga, consistente con Tijuana fresco y al nivel del mar).
- **Media**: Pericos, Bravos, Conspiradores, Algodoneros, Saraperos, Sultanes, Tecos, Acereros, Piratas, Tigres. Pericos (Puebla, 2,135 m) sale con menos arrastre que Bravos (León, 1,815 m), lo que es físicamente consistente. Conspiradores es el que casi no tiene juegos de local con Trackman (3 en 2024, 14 en 2025).
- **Baja**: Charros vs. Dorados y Leones / Águila / Olmecas. Sus PCT son casi iguales; podrían estar intercambiados entre sí. Para Harp Helú y la comparación por altitud no importa, porque los intercambios posibles ocurren dentro de la misma celda de altitud.

Nota: el PCT de los datos incluye postemporada y le faltan algunos juegos, por eso no cuadra exacto con la tabla.
