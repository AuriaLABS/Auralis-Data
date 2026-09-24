# Política de datos

Reglas para aceptar, describir y versionar fuentes en Auralis-Data.
No sustituyen asesoramiento legal. Si una fuente es dudosa, no entra.

## Principios

1. **Procedencia antes que volumen.** Una frase con origen y licencia vale más que un dump anónimo.
2. **Castellano primero.** El corpus de preentrenamiento prioriza español. Inglés y código se añaden con peso explícito en la mezcla.
3. **Licencia por fuente.** Mezclar no unifica licencias. Cada ficha declara qué se puede entrenar, publicar o citar.
4. **Git no es almacenamiento masivo.** Aquí viven metadatos y muestras. Los shards viven fuera, referenciados por checksum.
5. **Nada se acepta por intuición.** Igual que en Auralis: una fuente entra cuando la ficha está completa y el manifiesto la nombra.

## Criterios de rechazo rápido

Rechazar (o dejar en cuarentena) una fuente si ocurre cualquiera de esto:

- no hay licencia ni términos de uso identificables;
- la licencia prohíbe entrenamiento de modelos o uso comercial y no hay excepción documentada;
- el material es claramente PII (correos, teléfonos, documentos de identidad, historiales médicos);
- hay menor de edad en contexto sexual o explotación;
- el texto es sobre todo boilerplate web, captchas, carritos, cookies o basura OCR ilegible;
- no se puede reconstruir de dónde salió (URL, snapshot, hash, fecha).

## PII y seguridad

- No commitear secretos, cookies, credenciales ni dumps de correo real.
- Si una muestra de evaluación necesita un dato personal, se redacta o se sintetiza.
- Los logs de limpieza que citen documentos crudos no se suben.

## Splits

Toda mezcla versionada declara `train`, `validation` y `test` (aunque el test sea pequeño al principio). El fixture de Auralis no cuenta como split de evaluación.

Un documento no debe aparecer en dos splits de la misma mezcla. Si se detecta fuga, se versiona un manifiesto nuevo; no se «arregla en silencio» el anterior.

## Versionado

- Un manifiesto tiene nombre estable y versión (`mezcla-genesis-v0.1.0`).
- Cambiar pesos, fuentes o filtros **sube la versión**.
- El checksum del artefacto publicado se guarda en `checksums/`.
- Auralis debe apuntar a esa terna (nombre, versión, hash), no a «último archivo en el disco».

## Relación con el modelo

El repo [Auralis](https://github.com/AuriaLABS/Auralis) consume datos; no los define. Cuando el pipeline de 0.2 exista, este repositorio será la fuente de verdad de *qué* se entrenó, no de *cómo* multiplican los tensores.
