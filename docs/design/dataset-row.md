# DatasetRow — Design RFC

## Status

Frozen

---

## Purpose

Una DatasetRow representa, dentro de SportsQuant-AI, una observación
individual perteneciente a un Dataset: la unidad mínima de información
que Machine Learning consume como un caso concreto de entrenamiento,
validación o evaluación.

Una DatasetRow existe como concepto propio porque un Dataset, tal como
fue definido en `docs/design/dataset.md`, es un conjunto delimitado y
coherente de observaciones, pero ese documento deliberadamente no
definió qué constituye una observación individual. Ese vacío conceptual
es precisamente lo que este documento resuelve.

Una DatasetRow no es simplemente un fragmento arbitrario de datos
dentro de un Dataset, por las siguientes razones:

- Un fragmento arbitrario de datos no tiene por qué representar una
  observación completa y autocontenida. Una DatasetRow sí: encapsula
  todo lo necesario para que esa observación tenga sentido por sí
  misma.
- Un fragmento arbitrario de datos no necesita mantener correspondencia
  con un origen analítico específico. Una DatasetRow sí, porque debe
  poder trazarse hasta la información que la originó.
- Un fragmento arbitrario de datos no tiene por qué ser coherente con
  el resto de las observaciones de un conjunto. Una DatasetRow sí,
  porque su razón de ser es integrarse dentro de un Dataset con
  propósito y estructura propia.

Por estas razones, una DatasetRow merece ser tratada como un concepto
de primera clase, y no como un detalle incidental de cómo se organiza
internamente un Dataset.

---

## Conceptual Model

Una DatasetRow es, conceptualmente, una observación individual y
autocontenida: la representación de un caso concreto, delimitado en el
tiempo y en el dominio, que combina información analítica relevante con
el resultado asociado a esa observación.

Una DatasetRow no es un proceso. No es una transformación. No es una
acción de construcción. Es el resultado, ya estabilizado, de haber
organizado información analítica en la forma que una observación
requiere.

Dentro de un Dataset, una DatasetRow es la parte que compone el todo.
Un Dataset es el conjunto coherente de observaciones; una DatasetRow es
cada una de esas observaciones consideradas individualmente. Ninguna
DatasetRow tiene sentido pleno fuera del Dataset al que pertenece, pero
tampoco el Dataset existe sin las DatasetRow que lo componen.

---

## Responsibilities

Una DatasetRow es responsable de:

- Representar una observación individual, completa y autocontenida.
- Mantener correspondencia conceptual con la información analítica de
  la que se origina.
- Conservar la asociación entre esa observación y su resultado
  correspondiente.
- Preservar coherencia interna, de modo que la observación sea
  internamente consistente consigo misma.

Una DatasetRow **no** es responsable de:

- Derivar o calcular información analítica a partir de agregados de
  dominio. Esa responsabilidad pertenece exclusivamente a Feature
  Engineering.
- Construir, ensamblar o validar su propia existencia dentro de un
  Dataset. Esa responsabilidad pertenece a Dataset Generation.
- Determinar qué constituye un Dataset válido en su conjunto. Esa
  responsabilidad pertenece al concepto de Dataset.
- Entrenar, evaluar o utilizar modelos. Esa responsabilidad pertenece
  exclusivamente a Machine Learning.
- Decidir cómo se almacena, transporta o serializa. Esa responsabilidad
  pertenece a capas de infraestructura, no al concepto de DatasetRow en
  sí.

---

## Relationship with Dataset

Una DatasetRow se relaciona con un Dataset como la parte se relaciona
con el todo: cada DatasetRow pertenece a un único Dataset, y un Dataset
se compone de un conjunto delimitado de DatasetRow.

Ambos son conceptos distintos porque representan niveles diferentes de
significado:

- Un Dataset aporta el contexto colectivo: el propósito, la
  delimitación y la coherencia que convierten a un conjunto de
  observaciones en una unidad con sentido propio.
- Una DatasetRow aporta el contenido individual: el caso concreto que,
  junto con otros, compone ese conjunto.

Confundir ambos conceptos llevaría a que la observación individual
cargue con responsabilidades de conjunto (como la coherencia colectiva
o la delimitación general), lo cual violaría la separación de
responsabilidades ya establecida en `docs/design/dataset.md`.

---

## Relationship with Analytical Feature Models

Una DatasetRow se relaciona con los Analytical Feature Models como su
fuente conceptual de origen, de la misma manera en que un Dataset se
relaciona con ellos, pero a nivel de una única observación.

- Lo que **conserva**: una DatasetRow conserva el significado analítico
  de la información contenida en el Analytical Feature Model del que
  proviene. No reinterpreta ni redefine lo que una feature representa.
- Lo que **no modifica**: una DatasetRow no altera la naturaleza ni el
  origen de la información analítica que contiene. No es su
  responsabilidad recalcular ni reinterpretar esa información; esa
  responsabilidad pertenece exclusivamente a Feature Engineering.

Una DatasetRow es, en este sentido, la expresión de una observación ya
producida, no una nueva fuente de conocimiento analítico.

---

## Relationship with Prediction Target

Una DatasetRow mantiene una relación conceptual directa con el
Prediction Target: cada observación individual lleva asociado el
resultado correspondiente a esa observación.

Esta relación es inherente a lo que hace de una DatasetRow una
observación completa: sin su Prediction Target asociado, una DatasetRow
representaría únicamente estado analítico, pero no una observación
utilizable para entrenamiento o evaluación en el sentido definido por la
arquitectura de Machine Learning.

Este documento no decide todavía cómo se representa concretamente esa
asociación; únicamente establece que una DatasetRow y su Prediction
Target están conceptualmente unidos como parte de una misma
observación.

---

## Identity

Una DatasetRow tiene identidad propia.

Una DatasetRow debe ser trazable: debe ser posible identificar, sin
ambigüedad, de qué información analítica se originó una observación
determinada, y a qué Dataset pertenece.

Una DatasetRow se relaciona con el Dataset al que pertenece como una
parte identificable dentro de un todo delimitado: su pertenencia a ese
Dataset es parte de su identidad, de la misma manera en que su origen
analítico también lo es.

Este documento no decide todavía cómo se expresa esa identidad ni qué
mecanismo concreto garantiza esa trazabilidad; únicamente establece que
ambas propiedades son inherentes al concepto de DatasetRow.

---

## Architectural Principles

- **Inmutabilidad conceptual**: una DatasetRow, una vez definida,
  representa una observación fija. No es un concepto que cambie
  progresivamente en el tiempo.
- **Trazabilidad**: toda DatasetRow debe poder vincularse con claridad
  a su origen analítico y al Dataset al que pertenece.
- **Reproducibilidad**: una DatasetRow debe poder reconstruirse de
  forma equivalente a partir de la misma información analítica de
  origen.
- **Independencia del almacenamiento**: el concepto de DatasetRow no
  depende de dónde ni cómo se guarde la información.
- **Independencia del algoritmo de Machine Learning**: una DatasetRow
  no está diseñada en función de un algoritmo específico; representa
  una observación con sentido propio, independientemente del modelo que
  eventualmente la consuma.

---

## Future Evolution

Sin diseñar todavía cómo, una DatasetRow podría evolucionar en el
futuro hacia conceptos relacionados, tales como:

- Distintos tipos de DatasetRow según el Analytical Feature Model del
  que se originan (por ejemplo, a nivel de equipo, de jugador o de
  lineup).
- Relación con múltiples Prediction Targets asociados a una misma
  observación.
- Relación con distintos deportes o dominios analíticos.
- Mecanismos de comparación o agrupación entre distintas DatasetRow.
- Versionado de una DatasetRow en relación con versiones futuras de su
  Analytical Feature Model de origen.

Estas posibles evoluciones no se diseñan en este documento; únicamente
se reconocen como direcciones futuras razonables.

---

## Open Questions

Las siguientes preguntas quedan abiertas y no se resuelven en este
documento, ya que requieren decisiones de diseño o implementación
posteriores:

- ¿Cómo se expresa concretamente la identidad de una DatasetRow?
- ¿Qué mecanismo garantiza, en la práctica, la trazabilidad de una
  DatasetRow hasta su Analytical Feature Model de origen?
- ¿Puede una DatasetRow originarse de más de un Analytical Feature
  Model simultáneamente, o debe corresponder siempre a uno solo?
- ¿Cómo se relaciona la identidad de una DatasetRow con la identidad
  del Dataset al que pertenece, más allá del principio general de
  trazabilidad ya establecido?
- ¿Cómo se documenta o comunica la correspondencia entre una DatasetRow
  y su Prediction Target asociado?

Estas preguntas deberán resolverse en documentos de diseño o
especificaciones técnicas posteriores.

---

## Summary

Una DatasetRow, dentro de SportsQuant-AI, es la observación individual,
completa y autocontenida que compone un Dataset: la unidad mínima de
información analítica y resultado asociado que Machine Learning
considera un caso concreto de entrenamiento, validación o evaluación.

Una DatasetRow es el resultado conceptual de organizar la información
producida por un Analytical Feature Model, junto con su Prediction
Target correspondiente, en una forma trazable, reproducible y coherente
con el Dataset al que pertenece.

Una DatasetRow no es un proceso, no es responsable de su propia
construcción ni validación, y no está atada a ningún formato,
almacenamiento o algoritmo específico. Es, ante todo, una unidad
conceptual con identidad, propósito y significado propio dentro de la
arquitectura de SportsQuant-AI.