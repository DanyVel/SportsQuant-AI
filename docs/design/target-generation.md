# Target Generation — Design RFC

## Status

Frozen

---

## Purpose

Target Generation define, dentro de SportsQuant-AI, la responsabilidad
conceptual de producir el Prediction Target asociado a una observación
analítica.

Esta responsabilidad existe porque una DatasetRow representa una
observación completa compuesta por información analítica y un resultado
asociado, pero la producción de dicho resultado no pertenece ni al
Analytical Feature Model, ni a DatasetRow, ni al Dataset.

Target Generation existe como una responsabilidad propia para mantener
separadas dos cuestiones conceptualmente diferentes:

- la producción de información analítica que describe el estado de una
  observación;
- la determinación del resultado que corresponde a esa observación.

Esta separación permite que Dataset Generation pueda ensamblar una
observación completa sin asumir responsabilidades que pertenecen a
otras partes de la arquitectura.

---

## Conceptual Model

Un Prediction Target representa el resultado asociado a una observación
que puede ser utilizado posteriormente por Machine Learning como
variable objetivo.

El Prediction Target no representa una feature adicional.

Una feature describe información disponible acerca de una observación.

El Prediction Target representa el resultado que corresponde a esa
observación bajo un problema predictivo determinado.

La definición de qué resultado constituye el Prediction Target pertenece
conceptualmente a una Target Definition.

Una Target Definition expresa el problema predictivo y determina qué
resultado debe representar el Prediction Target.

Target Generation no decide arbitrariamente qué constituye un target.
Su responsabilidad es aplicar una Target Definition explícita sobre la
información necesaria para producir el resultado correspondiente.

Por lo tanto:

- Target Definition define qué resultado representa el target.
- Target Generation produce el Prediction Target de acuerdo con esa
  definición.
- Analytical Feature Models representan información analítica.
- Dataset Generation ensambla la información analítica y el Prediction
  Target en una DatasetRow.
- Dataset organiza las DatasetRow en un conjunto delimitado y coherente.

Target Generation no constituye Machine Learning.

No entrena modelos.

No realiza predicciones.

No evalúa modelos.

No calcula probabilidades.

No decide qué modelo debe utilizarse.

Su responsabilidad termina en producir el resultado que corresponde a
una observación de acuerdo con una Target Definition explícita.

---

## Responsibilities

Target Generation es responsable de:

- Recibir la información necesaria para determinar un Prediction Target.
- Aplicar una Target Definition explícita.
- Producir el Prediction Target correspondiente a una observación.
- Aplicar un criterio determinista para obtener dicho resultado cuando
  las condiciones de origen lo permitan.
- Mantener una separación clara entre la información analítica y el
  resultado objetivo.
- Permitir que el Prediction Target producido pueda asociarse de forma
  inequívoca con la observación correspondiente.
- Permitir que la generación del target sea reproducible bajo las mismas
  condiciones de origen y reglas de generación.

Target Generation no es responsable de:

- Definir arbitrariamente el problema predictivo.
- Producir Analytical Features.
- Transformar agregados de dominio en Analytical Feature Models.
- Entrenar modelos de Machine Learning.
- Generar predicciones de modelos.
- Evaluar modelos.
- Calcular probabilidades predichas.
- Decidir qué observaciones pertenecen a un Dataset determinado.
- Construir un Dataset.
- Construir una DatasetRow completa.
- Almacenar o serializar Prediction Targets.
- Definir infraestructura de persistencia.
- Decidir cómo un algoritmo específico de Machine Learning utilizará el
  target.

---

## Relationship with Target Definition

Una Target Definition representa la definición explícita del resultado
que un problema predictivo requiere como Prediction Target.

Target Definition y Target Generation son conceptos relacionados pero
distintos:

- Target Definition establece qué resultado debe representar el target.
- Target Generation determina ese resultado para una observación
  concreta.

Target Generation no debe contener de forma implícita la definición del
problema predictivo.

La separación conceptual es:

```text
Target Definition
        +
Required Domain Information
        │
        ▼
Target Generation
        │
        ▼
Prediction Target