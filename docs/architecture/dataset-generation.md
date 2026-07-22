# Arquitectura de Dataset Generation

## Status

Propuesto

---

## Purpose

Dataset Generation es la capa responsable de transformar Analytical
Feature Models, producidos por Feature Engineering, en datasets
reproducibles listos para ser consumidos por Machine Learning.

Esta capa existe de forma independiente porque la construcción de un
dataset de entrenamiento no es una responsabilidad de Feature
Engineering ni de Machine Learning.

Feature Engineering se limita a derivar features analíticas a partir de
agregados de dominio, sin conocimiento de targets, particiones
temporales ni de los requisitos de un dataset de entrenamiento.

Machine Learning se limita a consumir datasets ya construidos y
validados, sin conocimiento de cómo se originan las features ni de cómo
se ensamblan las filas del dataset.

Dataset Generation cierra esa brecha. Es la única capa responsable de
transformar features analíticas en observaciones de entrenamiento,
garantizando que el resultado sea consistente, reproducible y libre de
fuga de información.

Sin esta capa, la lógica de construcción de datasets tendería a
dispersarse entre Feature Engineering y Machine Learning, violando el
principio de responsabilidad única y acoplando ambas capas entre sí.

---

## Architectural Position

Dataset Generation se ubica estrictamente entre Feature Engineering y
Machine Learning.

```
Historical Data
        │
        ▼
Feature Engineering
        │
        ▼
Analytical Feature Models
        │
        ▼
Dataset Generation
        │
        ▼
Datasets
        │
        ▼
Machine Learning
```

- Feature Engineering produce Analytical Feature Models.
- Dataset Generation consume esos Analytical Feature Models.
- Machine Learning consume únicamente los datasets producidos por
  Dataset Generation.

Ninguna capa puede saltarse en este flujo. Machine Learning no accede
directamente a Analytical Feature Models, y Feature Engineering no
produce datasets directamente.

---

## Responsibilities

Dataset Generation es responsable de:

- Construir las filas del dataset a partir de Analytical Feature Models.
- Generar los prediction targets asociados a cada fila.
- Validar la consistencia estructural del dataset.
- Detectar y prevenir data leakage.
- Validar la presencia de las columnas requeridas.
- Garantizar la reproducibilidad del dataset generado.
- Preparar el dataset final para ser consumido por el Training Pipeline.

Dataset Generation **no** es responsable de:

- Producir o derivar Analytical Feature Models. Esa responsabilidad
  pertenece exclusivamente a Feature Engineering.
- Entrenar modelos.
- Evaluar modelos.
- Realizar inferencia.
- Calibrar probabilidades.
- Definir estrategias de partición temporal de entrenamiento.
- Persistir datos históricos ni acceder a la capa de Persistence.
- Ejecutar lógica de negocio no relacionada con la construcción del
  dataset.

Dataset Generation es una capa de transformación y validación, no una
capa de modelado ni de acceso a datos crudos.

---

## Inputs

Dataset Generation consume exclusivamente Analytical Feature Models
producidos por Feature Engineering.

No consume:

- Agregados de dominio directamente.
- Datos crudos de proveedores externos.
- Registros de Persistence directamente.

Cualquier información necesaria para construir el dataset debe llegar a
Dataset Generation ya transformada en un Analytical Feature Model. Esto
garantiza que Dataset Generation permanezca desacoplado de la fuente
original de los datos y del dominio.

---

## Outputs

Dataset Generation produce datasets reproducibles, listos para ser
consumidos por el Training Pipeline de Machine Learning.

La arquitectura permanece deliberadamente agnóstica respecto al formato
físico de salida. El formato final del dataset es una decisión de
implementación posterior y no forma parte de este documento.

Lo que sí es arquitectónicamente obligatorio es que la salida:

- Represente un conjunto completo de observaciones válidas para
  entrenamiento.
- Sea reproducible a partir de los mismos Analytical Feature Models de
  entrada.
- Haya sido validada de acuerdo con los criterios definidos en la
  sección Validation.

---

## Dataset Rows

Conceptualmente, una fila del dataset representa una observación
individual utilizable para entrenamiento o evaluación.

Cada fila se deriva de uno o más Analytical Feature Models y encapsula:

- El estado analítico relevante para esa observación.
- El prediction target correspondiente a esa observación.

Una fila del dataset no introduce información nueva respecto a los
Analytical Feature Models de entrada; únicamente organiza y valida esa
información en la forma requerida por Machine Learning.

La definición exacta de qué constituye una fila puede variar según el
tipo de problema (por ejemplo, una fila por equipo por partido), pero el
principio arquitectónico se mantiene constante: cada fila es una
observación trazable hasta su Analytical Feature Model de origen.

---

## Prediction Targets

Dataset Generation es responsable de construir los prediction targets
utilizados durante el entrenamiento.

Esta responsabilidad no pertenece a Machine Learning por las siguientes
razones:

- El target se deriva de información histórica ya conocida (por ejemplo,
  el resultado final de un partido), la cual debe procesarse con el
  mismo rigor aplicado a las features, incluyendo validación de
  consistencia y prevención de leakage.
- Machine Learning debe recibir el target ya resuelto, como parte de una
  observación completa y validada, sin necesidad de conocer cómo se
  deriva.
- Mantener la generación del target fuera de Machine Learning refuerza
  la separación de responsabilidades: Machine Learning se concentra en
  aprender de los datos, no en definir qué constituye un resultado
  correcto.

La lógica de qué representa un target válido es una decisión
arquitectónica de Dataset Generation, no una decisión del Training
Pipeline.

---

## Validation

Dataset Generation aplica un conjunto de validaciones arquitectónicas
obligatorias antes de que un dataset pueda considerarse apto para
Machine Learning.

Como mínimo, Dataset Generation valida:

- **Data leakage**: ninguna fila puede contener información que no
  estuviera disponible en el momento real de la predicción, de acuerdo
  con las reglas de Forbidden Features definidas en la arquitectura de
  Machine Learning.
- **Consistencia estructural**: todas las filas deben respetar el mismo
  esquema, los mismos tipos de datos y las mismas convenciones.
- **Duplicados**: no se permite la existencia de filas duplicadas dentro
  del mismo dataset.
- **Columnas requeridas**: toda columna necesaria para el entrenamiento
  debe estar presente y correctamente poblada.
- **Integridad del dataset**: el dataset debe representar de forma
  completa y coherente el conjunto de observaciones esperado, sin
  omisiones ni inconsistencias entre filas relacionadas.

Un dataset que no supere estas validaciones no puede ser exportado ni
entregado al Training Pipeline.

---

## Reproducibility

Un dataset es reproducible cuando, dado el mismo conjunto de Analytical
Feature Models de entrada y los mismos parámetros de generación (por
ejemplo, una fecha de corte), Dataset Generation produce siempre el
mismo resultado.

La reproducibilidad es un requisito arquitectónico, no una característica
opcional, por las siguientes razones:

- Permite auditar cualquier predicción hasta el dataset exacto que la
  originó.
- Permite comparar modelos entrenados en condiciones equivalentes.
- Permite reconstruir un dataset histórico ante fallos, migraciones o
  auditorías.
- Es una precondición para la trazabilidad exigida por la arquitectura
  de Machine Learning, que establece que toda predicción debe ser
  trazable hasta el dataset y el modelo que la produjeron.

Sin reproducibilidad, ningún resultado de Machine Learning puede
considerarse confiable ni auditable.

---

## Architectural Principles

Los siguientes principios son de cumplimiento obligatorio para Dataset
Generation:

- **Separación de responsabilidades**: Dataset Generation no produce
  features ni entrena modelos; únicamente transforma features en
  datasets.
- **Determinismo**: dado el mismo input, Dataset Generation siempre
  produce el mismo output.
- **Reproducibilidad**: todo dataset generado debe poder reconstruirse
  de forma idéntica.
- **Independencia de Machine Learning**: Dataset Generation no conoce
  detalles de entrenamiento, evaluación ni inferencia.
- **Independencia del almacenamiento**: Dataset Generation no depende de
  ningún mecanismo de persistencia específico.
- **Independencia del formato del dataset**: la arquitectura no asume ni
  impone un formato físico particular para el dataset resultante.

Estos principios garantizan que Dataset Generation permanezca estable
incluso cuando cambien los modelos, los proveedores de datos o las
tecnologías de almacenamiento.

---

## Future Evolution

Dataset Generation está diseñado para evolucionar sin comprometer sus
principios arquitectónicos. Extensiones futuras posibles incluyen:

- Soporte para múltiples tipos de datasets, derivados de distintos
  Analytical Feature Models (por ejemplo, datasets a nivel de equipo, de
  jugador o de lineup).
- Soporte para múltiples prediction targets dentro del mismo dominio de
  datos (por ejemplo, resultado del partido, margen de victoria, totales).
- Extensión hacia distintos deportes, reutilizando la misma arquitectura
  sin modificar sus principios.
- Soporte para distintos modelos que consuman variaciones del mismo
  dataset base.
- Incorporación de validaciones adicionales a medida que surjan nuevos
  requisitos de calidad de datos.
- Versionado explícito de datasets, permitiendo asociar cada dataset
  generado con una versión específica de Feature Engineering y con un
  conjunto específico de Analytical Feature Models.

Cada una de estas extensiones debe respetar los principios definidos en
este documento y debe documentarse formalmente antes de su
implementación.

---

## Summary

Dataset Generation es la capa arquitectónica responsable de transformar
Analytical Feature Models en datasets reproducibles, validados y listos
para el entrenamiento de modelos de Machine Learning.

Se ubica de forma estricta entre Feature Engineering y Machine Learning,
consumiendo exclusivamente Analytical Feature Models y produciendo
datasets que Machine Learning consume sin necesidad de conocer su
origen.

Su existencia como capa independiente garantiza que la construcción de
targets, la validación de leakage, la consistencia estructural y la
reproducibilidad de los datos de entrenamiento sean tratadas como una
responsabilidad arquitectónica propia, y no como una extensión implícita
de Feature Engineering o de Machine Learning.