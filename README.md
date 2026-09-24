# Auralis-Data

Repositorio de **datos** del proyecto [Auralis](https://github.com/AuriaLABS/Auralis) (AuriaLABS).

Auralis es el modelo: tokenizador, transformer, entrenamiento e inferencia en Rust.
Auralis-Data es la fábrica de corpora: procedencia, limpieza, mezclas, licencias y manifiestos versionados.

> El código no guarda el corpus real. El corpus no entrena el modelo por sí solo.
> Cada fuente entra con licencia, checksum y una ficha que se pueda auditar.

## Estado

Fase de arranque. Este repositorio acaba de inicializarse. Todavía no hay shards de preentrenamiento ni mezclas cerradas.

El archivo `data/corpus.txt` que vive en el repo de Auralis es un **fixture de desarrollo**: unas pocas frases en castellano para cerrar el ciclo Genesis (entrenar, guardar checkpoint, generar texto). No es el dataset de entrenamiento.

Idioma de trabajo de la documentación y de los metadatos: **español**. El corpus objetivo es castellano en primer término, con inglés y código cuando una mezcla lo justifique.

## Qué sí entra aquí

- Fichas de dataset (origen, idioma, licencia, fecha de corte, sesgos conocidos).
- Manifiestos de mezcla: qué fuentes, qué peso, qué split.
- Recetas de limpieza y criterios de rechazo.
- Checksums (`SHA-256`) de artefactos versionados.
- Textos de licencia por fuente.
- Muestras pequeñas y conjuntos de evaluación que quepan en git.
- Scripts o notas que documenten cómo se construyó un artefacto.

## Qué no entra en git

- Dumps de crawl, `.parquet` / `.arrow` / `.jsonl` masivos, tarballs, shards tokenizados (`.bin`, `.idx`).
- Checkpoints del modelo (`auralis.bin` y equivalentes).
- Secretos, cookies, credenciales o texto con PII sin redactar.

Esos artefactos viven fuera (almacenamiento de objetos o disco de entrenamiento). Aquí solo queda el puntero: URI, tamaño, checksum y ficha.

Esto no es un capricho de repo limpio. GitHub no es un datalake; un push de decenas de gigas rompe clones, CI y el histórico. Auralis 0.2 pide «datasets mayores y pipeline de datos»; ese pipeline debe ser reproducible sin clonar terabytes.

## Estructura

```text
Auralis-Data/
  README.md                 este archivo
  LICENSE                   licencia del andamiaje del repo (no de cada corpus)
  docs/
    politica.md             reglas de aceptación, PII, atribución
    ficha.plantilla.md      plantilla de ficha de dataset
  manifests/                mezclas y listados versionados (JSON/YAML)
  licenses/                 textos o extractos de licencia por fuente
  checksums/                SHA-256 de artefactos publicados
  samples/                  recortes mínimos para pruebas y CI
  raw/                      notas de procedencia; no el dump
  processed/                notas del corpus limpio; no los shards
  mixes/                    recetas de mezcla train/val/test
```

Las carpetas `raw/`, `processed/` y `mixes/` guardan **descripciones y punteros**, no el binario. Si un archivo supera unos pocos megabytes, no pertenece a git.

## Relación con Auralis

| Pieza | Dónde | Rol |
| --- | --- | --- |
| Motor, tokenizador, train/eval/chat | [AuriaLABS/Auralis](https://github.com/AuriaLABS/Auralis) | código |
| Fixture `data/corpus.txt` | repo Auralis | humo / Genesis |
| Corpora, mixes, fichas | este repo | datos |
| Checkpoints | fuera de ambos repos | artefactos de entrenamiento |

Cuando exista la primera mezcla usable, Auralis deberá referenciarla por **nombre + versión + checksum**, no por «un archivo que alguien dejó en disco».

Encaja con la hoja de ruta de Auralis:

- **0.1 Genesis** — ciclo sobre un corpus mínimo (ya cubierto por el fixture).
- **0.2 Foundation** — datasets mayores, splits train/val/test, perplexity.
- **0.7 Multimodal** — datasets multimodales versionados, más adelante.

## Cómo añadir una fuente

1. Copiar `docs/ficha.plantilla.md` a `docs/fuentes/<id>.md`.
2. Dejar constancia de URL o identificador estable, fecha de descarga, licencia y restricciones.
3. Si el artefacto es grande, publicar checksum en `checksums/` y la URI en el manifiesto. No subir el blob.
4. Si forma parte de una mezcla, editar `manifests/` y `mixes/` en el mismo cambio.
5. Toda fuente sin licencia clara o con PII evidente se queda fuera hasta resolverlo.

Detalle normativo: [docs/politica.md](docs/politica.md).

## Licencia de este repositorio

El andamiaje (documentación, plantillas, manifiestos vacíos, scripts que se añadan) se publica bajo [MIT](LICENSE), igual que Auralis.

**Eso no cubre los datasets.** Cada fuente conserva su licencia original. Entrenar o redistribuir un corpus exige leer `licenses/` y la ficha correspondiente. Mezclar fuentes no crea una licencia nueva ni borra las anteriores.
