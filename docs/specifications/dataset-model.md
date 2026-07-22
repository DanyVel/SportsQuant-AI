# Dataset Model — Implementation Specification

## Status

Draft

---

## Objective

El objetivo del primer commit es introducir, dentro del código de
SportsQuant-AI, la existencia técnica mínima de los modelos `Dataset` y
`DatasetRow`, tal como fueron conceptualmente definidos en:

- `docs/design/dataset.md`
- `docs/design/dataset-row.md`

Este primer commit busca únicamente establecer ambos modelos como
estructuras de datos válidas dentro del código base, coherentes con los
principios arquitectónicos ya congelados en
`docs/architecture/dataset-generation.md` y
`docs/architecture/machine-learning.md`. No busca implementar ninguna
lógica de construcción, validación, generación de targets, ni ningún
comportamiento asociado a Dataset Generation, Feature Engineering o
Machine Learning.

Este commit es fundacional: establece la existencia de los modelos que
representan una observación y un conjunto de observaciones, sin
implementar todavía cómo se producen, validan o consumen.

---

## Files

### Archivos nuevos

- Un archivo correspondiente a la definición del modelo `DatasetRow`,
  ubicado en el área del código dedicada a Dataset Generation / Machine
  Learning, separado de Feature Engineering, de acuerdo con la
  independencia establecida en `docs/architecture/dataset-generation.md`.
- Un archivo correspondiente a la definición del modelo `Dataset`,
  ubicado en la misma área, separado del archivo de `DatasetRow`, en
  consistencia con la distinción conceptual establecida entre ambos en
  `docs/design/dataset.md`.

### Archivos de pruebas

- Un archivo de pruebas unitarias correspondiente a `DatasetRow`.
- Un archivo de pruebas unitarias correspondiente a `Dataset`.

No se especifican rutas adicionales ni archivos adicionales más allá de
los estrictamente necesarios para la existencia de ambos modelos y sus
pruebas correspondientes.

---

## Models

### Modelos que se implementarán en este commit

- **`DatasetRow`**: la representación técnica de una observación
  individual, según lo definido conceptualmente en
  `docs/design/dataset-row.md`.
- **`Dataset`**: la representación técnica de un conjunto delimitado y
  coherente de observaciones, según lo definido conceptualmente en
  `docs/design/dataset.md`.

### Modelos que NO forman parte de este commit

- Cualquier modelo o componente responsable de construir, ensamblar o
  producir instancias de `DatasetRow` o `Dataset` a partir de
  Analytical Feature Models. Esa responsabilidad pertenece a Dataset
  Generation y no forma parte de este commit.
- Cualquier modelo relacionado con la generación de prediction targets
  como proceso.
- Cualquier modelo relacionado con validación de leakage, consistencia
  estructural, duplicados o columnas requeridas.
- Cualquier modelo relacionado con el Training Pipeline o el Inference
  Pipeline.
- Cualquier variante especializada de `DatasetRow` asociada a otros
  Analytical Feature Models distintos de los ya existentes en Feature
  Engineering.
- Cualquier modelo de exportación, serialización o persistencia de
  `Dataset` o `DatasetRow`.

---

## Responsibilities

Durante este primer commit, las responsabilidades técnicas de cada
modelo se limitan estrictamente a lo siguiente:

### DatasetRow

- Existir como una representación técnica válida de una observación
  individual, capaz de mantener conjuntamente el estado analítico y el
  resultado asociado a esa observación, conforme a lo establecido en
  `docs/design/dataset-row.md`.
- Mantener coherencia interna como una unidad autocontenida.

### Dataset

- Existir como una representación técnica válida de un conjunto
  delimitado de instancias de `DatasetRow`, conforme a lo establecido
  en `docs/design/dataset.md`.
- Actuar como el contenedor coherente de esas observaciones, sin
  imponer sobre ellas ninguna responsabilidad de conjunto.

Ninguno de los dos modelos es responsable, en este commit, de producir,
validar, transformar o interpretar la información que contienen. Esa
responsabilidad pertenece exclusivamente a capas ya definidas fuera de
este alcance.

---

## Implementation Constraints

- **Inmutabilidad**: tanto `DatasetRow` como `Dataset` deben
  comportarse como estructuras inmutables una vez construidas, en
  consistencia con el principio de inmutabilidad conceptual establecido
  en ambos Design RFC.
- **Separación de responsabilidades**: ningún modelo definido en este
  commit debe contener lógica de construcción, validación o
  transformación. Ambos modelos representan resultado, no proceso.
- **Independencia de Persistence**: ninguno de los dos modelos debe
  depender de mecanismos de almacenamiento, acceso a datos ni
  infraestructura de persistencia.
- **Independencia de Dataset Generation**: ninguno de los dos modelos
  debe contener ni depender de lógica propia de la capa de Dataset
  Generation, tal como fue definida en
  `docs/architecture/dataset-generation.md`.
- **Independencia de Machine Learning**: ninguno de los dos modelos
  debe depender de lógica de entrenamiento, evaluación, calibración o
  inferencia, tal como fue definida en
  `docs/architecture/machine-learning.md`.
- **Independencia de Feature Engineering**: la implementación de estos
  modelos no debe introducir dependencias hacia la lógica interna de
  Feature Engineering más allá de lo estrictamente necesario para
  conservar, sin modificar, la información analítica que una
  `DatasetRow` representa.

---

## Testing

Las pruebas unitarias de este commit deben validar exclusivamente:

- Que una instancia de `DatasetRow` puede construirse correctamente
  como una observación individual válida.
- Que una instancia de `DatasetRow` ya construida no puede ser
  modificada.
- Que una instancia de `Dataset` puede construirse correctamente a
  partir de un conjunto de instancias de `DatasetRow`.
- Que una instancia de `Dataset` ya construida no puede ser modificada.
- Que `Dataset` puede construirse a partir de un conjunto vacío de
  observaciones, sin que esto constituya un error a nivel de modelo.

Ninguna prueba de este commit debe validar reglas de negocio propias de
Dataset Generation, tales como ausencia de leakage, ausencia de
duplicados o presencia de columnas requeridas, ya que esas reglas no
son responsabilidad de estos modelos.

---

## Out of Scope

Quedan explícitamente fuera del alcance de este commit:

- Toda lógica de construcción de `DatasetRow` o `Dataset` a partir de
  Analytical Feature Models.
- Toda lógica de generación de prediction targets.
- Toda lógica de validación de leakage, consistencia estructural,
  duplicados o columnas requeridas.
- Toda lógica de exportación, serialización, persistencia o formato
  físico de `Dataset` o `DatasetRow`.
- Todo mecanismo concreto de identidad o versionado de un `Dataset` o
  de una `DatasetRow`.
- Toda integración con el Training Pipeline o el Inference Pipeline.
- Toda variante especializada de `DatasetRow` para Analytical Feature
  Models distintos de los ya existentes.
- Toda decisión sobre partición temporal de train/validation/test.
- Cualquier algoritmo, pipeline o comportamiento de negocio no descrito
  explícitamente en este documento.

---

## Commit Goal

Al finalizar este commit deben existir, y únicamente, los siguientes
elementos:

- El modelo `DatasetRow`, implementado como una estructura inmutable,
  conforme a lo definido en `docs/design/dataset-row.md`.
- El modelo `Dataset`, implementado como una estructura inmutable,
  conforme a lo definido en `docs/design/dataset.md`.
- Las pruebas unitarias correspondientes a ambos modelos, cubriendo
  como mínimo los casos descritos en la sección Testing de este
  documento.

Este commit no debe contener ninguna lógica de construcción,
validación, generación de targets, exportación, ni ningún otro
comportamiento propio de Dataset Generation, Training Pipeline o
Inference Pipeline. El resultado de este commit es, exclusivamente, la
existencia de ambos modelos, listos para ser consumidos por
implementaciones futuras que no forman parte de este alcance.