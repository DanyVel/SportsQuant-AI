# Dataset — Design RFC

## Status

Frozen

---

## Purpose

Un Dataset representa, dentro de SportsQuant-AI, el conjunto completo de
observaciones que Machine Learning utiliza para entrenar, evaluar o
validar un modelo en un momento determinado.

Un Dataset existe como concepto propio porque no es simplemente
información disponible; es información que ha sido deliberadamente
delimitada, organizada y preparada con un propósito específico: servir
como base de aprendizaje o evaluación para un modelo.

Un Dataset no es una colección cualquiera de datos por las siguientes
razones:

- Una colección cualquiera de datos no tiene un propósito predictivo
  definido. Un Dataset sí lo tiene: existe en función de un problema de
  Machine Learning concreto.
- Una colección cualquiera de datos puede cambiar, crecer o mezclarse
  libremente. Un Dataset representa un corte específico, delimitado y
  con sentido propio.
- Una colección cualquiera de datos no necesita ser reproducible ni
  trazable. Un Dataset sí, porque de él dependen decisiones de
  entrenamiento, evaluación y, eventualmente, decisiones de negocio.

Por estas razones, un Dataset merece ser tratado como un concepto de
primera clase dentro de la arquitectura de SportsQuant-AI, y no como un
subproducto incidental de otras capas.

---

## Conceptual Model

Un Dataset es, conceptualmente, un conjunto delimitado y coherente de
observaciones, cada una compuesta por información analítica y un
resultado asociado, reunidas con el propósito de ser utilizadas por
Machine Learning.

Un Dataset no es un proceso. No es una acción. No es una transformación.
Es el resultado, ya estabilizado, de haber aplicado un criterio
consistente sobre un conjunto de observaciones.

Un Dataset representa una porción de la realidad del dominio,
seleccionada y organizada bajo un criterio explícito, en un momento
determinado.

---

## Responsibilities

Un Dataset es responsable de:

- Representar un conjunto delimitado de observaciones válidas para
  Machine Learning.
- Mantener coherencia interna entre todas sus observaciones.
- Actuar como el punto de referencia único que Machine Learning consume
  para entrenar o evaluar un modelo.
- Ser identificable como una unidad concreta, distinguible de otros
  conjuntos de observaciones.

Un Dataset **no** es responsable de:

- Producir información analítica a partir de agregados de dominio. Esa
  responsabilidad pertenece a Feature Engineering.
- Construir, validar o ensamblar sus propias observaciones. Esa
  responsabilidad pertenece a Dataset Generation.
- Entrenar, evaluar o utilizar modelos. Esa responsabilidad pertenece a
  Machine Learning.
- Decidir cómo se almacena, transporta o serializa la información. Esa
  responsabilidad pertenece a capas de infraestructura, no al concepto
  de Dataset en sí.

---

## Relationship with Dataset Rows

Un Dataset se relaciona con sus observaciones individuales como un todo
se relaciona con sus partes: el Dataset es el conjunto coherente, y cada
observación es un elemento que pertenece a ese conjunto.

Un Dataset no tiene sentido sin sus observaciones, pero tampoco es
simplemente la suma mecánica de ellas: el Dataset aporta el contexto que
convierte a un conjunto de observaciones individuales en una unidad con
propósito, delimitación y coherencia propia.

Este documento no define todavía qué es una observación individual en
detalle; únicamente establece que un Dataset la contiene y le da sentido
colectivo.

---

## Relationship with Analytical Feature Models

Un Dataset se relaciona con los Analytical Feature Models como su fuente
conceptual de origen.

- Lo que **transforma**: un Dataset transforma información analítica
  dispersa, producida por Feature Engineering, en un conjunto delimitado
  y con propósito, listo para ser consumido por Machine Learning.
- Lo que **conserva**: un Dataset conserva el significado analítico de la
  información original. No reinterpreta ni redefine lo que una feature
  representa.
- Lo que **no modifica**: un Dataset no altera la naturaleza ni el
  origen de los Analytical Feature Models. No es su responsabilidad
  recalcular ni reinterpretar información analítica; esa responsabilidad
  pertenece exclusivamente a Feature Engineering.

Un Dataset es, en este sentido, una organización con propósito de
información ya producida, no una nueva fuente de conocimiento analítico.

---

## Relationship with Machine Learning

Machine Learning conoce de un Dataset únicamente lo siguiente:

- Que representa un conjunto coherente y delimitado de observaciones.
- Que puede ser utilizado como base para entrenar, evaluar o validar un
  modelo.
- Que es reproducible y trazable.

Machine Learning **no** conoce:

- Cómo se originó cada observación.
- De qué Analytical Feature Models proviene la información.
- Cómo fue validado o ensamblado el Dataset.
- Ningún detalle acerca del proceso que produjo el Dataset.

Esta separación garantiza que Machine Learning permanezca desacoplado de
la lógica de construcción de datos, consumiendo únicamente el resultado
final.

---

## Relationship with Dataset Generation

La distinción entre Dataset y Dataset Generation es conceptual y debe
mantenerse estricta:

- **Dataset** es el resultado: el conjunto delimitado, coherente y
  reproducible de observaciones.
- **Dataset Generation** es el proceso: la capa responsable de producir
  ese resultado a partir de Analytical Feature Models.

Un Dataset no sabe cómo fue construido. Dataset Generation sabe cómo
construir un Dataset, pero no es en sí mismo un Dataset.

Mezclar ambos conceptos llevaría a que el resultado (Dataset) cargue con
responsabilidades de proceso, lo cual violaría la separación de
responsabilidades ya establecida en `docs/architecture/dataset-generation.md`.

---

## Identity

Un Dataset tiene identidad propia.

Un Dataset debe ser trazable: debe ser posible identificar, sin
ambigüedad, qué Dataset específico fue utilizado para entrenar,
evaluar o producir una predicción determinada.

Un Dataset debe representar un snapshot reproducible: dado el mismo
criterio de generación y las mismas condiciones de origen, debe ser
posible reconstruir un Dataset equivalente en contenido y significado.

Este documento no decide todavía cómo se expresa esa identidad ni cómo
se garantiza esa reproducibilidad en términos concretos; únicamente
establece que ambas propiedades son inherentes al concepto de Dataset.

---

## Architectural Principles

- **Inmutabilidad conceptual**: un Dataset, una vez definido, representa
  un conjunto fijo de observaciones. No es un concepto que cambie
  progresivamente en el tiempo.
- **Reproducibilidad**: un Dataset debe poder reconstruirse de forma
  equivalente a partir de las mismas condiciones de origen.
- **Trazabilidad**: todo Dataset debe poder vincularse con claridad a su
  origen y a su uso posterior.
- **Independencia del almacenamiento**: el concepto de Dataset no
  depende de dónde ni cómo se guarde la información.
- **Independencia del formato**: el concepto de Dataset no depende de
  ninguna representación física particular.
- **Independencia del algoritmo de Machine Learning**: un Dataset no
  está diseñado en función de un algoritmo específico; es el algoritmo
  el que se adapta al Dataset, no al revés.

---

## Future Evolution

Sin diseñar todavía cómo, un Dataset podría evolucionar en el futuro
hacia conceptos relacionados, tales como:

- Distintos tipos de Dataset según el problema de Machine Learning que
  respaldan.
- Distintas versiones de un mismo Dataset a lo largo del tiempo.
- Relación con múltiples prediction targets dentro de un mismo dominio.
- Relación con distintos deportes o dominios analíticos.
- Mecanismos de comparación entre distintos Datasets.
- Políticas de vigencia o expiración conceptual de un Dataset.

Estas posibles evoluciones no se diseñan en este documento; únicamente
se reconocen como direcciones futuras razonables.

---

## Open Questions

Las siguientes preguntas quedan abiertas y no se resuelven en este
documento, ya que requieren decisiones de diseño o implementación
posteriores:

- ¿Cómo se expresa concretamente la identidad de un Dataset?
- ¿Qué mecanismo garantiza, en la práctica, que un Dataset sea
  reproducible?
- ¿Cómo se relaciona la identidad de un Dataset con la identidad de un
  Trained Model, más allá del principio general de trazabilidad ya
  establecido en la arquitectura de Machine Learning?
- ¿Un Dataset puede contener observaciones de distintos tipos de
  Analytical Feature Models simultáneamente, o debe ser homogéneo?
- ¿Cómo se documenta o comunica el criterio de delimitación de un
  Dataset determinado?

Estas preguntas deberán resolverse en documentos de diseño o
especificaciones técnicas posteriores.

---

## Summary

Un Dataset, dentro de SportsQuant-AI, es el conjunto delimitado,
coherente, reproducible y trazable de observaciones que Machine Learning
utiliza como base para entrenar, evaluar o validar un modelo.

Un Dataset es el resultado conceptual de organizar información analítica
producida por Feature Engineering, bajo un criterio explícito definido
por Dataset Generation, sin que el Dataset mismo conozca ni dependa de
cómo fue construido.

Un Dataset no es un proceso, no es una colección arbitraria de datos, y
no está atado a ningún formato, almacenamiento o algoritmo específico.
Es, ante todo, una unidad conceptual con propósito, identidad y
significado propio dentro de la arquitectura de SportsQuant-AI.