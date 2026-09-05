# Dataset Generation Orchestration — Design RFC

## Status

Propuesto

---

## 1. Purpose

Este documento especifica conceptualmente la responsabilidad de
orquestación que pertenece a la capa de **Dataset Generation** dentro de
SportsQuant-AI.

Su propósito es describir cómo la responsabilidad ya asignada a Dataset
Generation coordina las piezas necesarias para producir observaciones
completas destinadas a Machine Learning, particularmente la relación
entre:

- `DatasetBuilder`;
- Target Generation;
- `DatasetRow`;
- `Dataset`.

Este documento no introduce un nuevo componente arquitectónico de
primera clase.

La orquestación descrita aquí debe entenderse como una responsabilidad
interna de la capa de Dataset Generation y no como una nueva entidad
independiente comparable a `DatasetBuilder`, Target Generation,
`DatasetRow` o `Dataset`.

Este documento tampoco implementa código ni determina todavía la forma
técnica concreta mediante la cual esta responsabilidad será
implementada.

---

## 2. Problem Statement

Existe una tensión textual en la specification actualmente definida para
`DatasetBuilder`.

`docs/specifications/dataset-builder.md` establece que, para cada
`TeamGameFeature`, se construye una instancia de `DatasetRow` que
conserva el estado analítico representado por dicho `TeamGameFeature`.

Al mismo tiempo, `DatasetRow` actualmente requiere dos elementos:

- una `feature`;
- un `target`.

Por otro lado, la specification de `DatasetBuilder` establece
explícitamente que `DatasetBuilder`:

- no conoce conceptos de Machine Learning;
- no genera labels;
- no genera prediction targets;
- no asocia, calcula ni deriva el prediction target de una observación.

Por lo tanto, existe una tensión textual real entre el paso de
construcción de `DatasetRow` descrito en `dataset-builder.md` y el
contrato actual de `DatasetRow`.

Este documento no resuelve unilateralmente esa tensión.

La finalidad de este RFC es describir cómo la responsabilidad de
orquestación de Dataset Generation deberá coordinar las piezas
existentes, manteniendo abiertas las decisiones que todavía requieren
formalización.

---

## 3. Architectural Context

La arquitectura existente asigna a **Dataset Generation** la
responsabilidad general de transformar información analítica en datasets
destinados posteriormente a Machine Learning.

El documento:

`docs/architecture/dataset-generation.md`

tiene actualmente estado **Propuesto**.

Por lo tanto, este RFC utiliza dicho documento como contexto
arquitectónico vigente, pero no lo trata como una decisión arquitectónica
Frozen.

De manera equivalente, `docs/architecture/machine-learning.md` tiene
actualmente estado **Propuesto**.

Este RFC utiliza sus definiciones como contexto para describir la
coordinación actualmente prevista, pero no convierte sus elementos
todavía no congelados en decisiones definitivas.

En particular, `docs/architecture/machine-learning.md` proporciona el
antecedente conceptual de que un dataset puede organizar sus
observaciones alrededor de una correspondencia:

`(game_id, team_id)`

Esta referencia no define por sí misma un mecanismo técnico de
identidad dentro de `DatasetRow`, ni introduce campos nuevos en los
modelos existentes.

---

## 4. Architectural Position

La coordinación descrita en este documento pertenece a la capa de
Dataset Generation.

No se introduce un componente independiente llamado
"Dataset Row Assembly".

Tampoco se establece un componente independiente denominado
"Dataset Generation Orchestrator".

Cuando este documento utiliza expresiones como "orquestación de Dataset
Generation", se refiere a la responsabilidad de coordinación de la
propia capa de Dataset Generation.

La responsabilidad de orquestación:

- coordina componentes ya existentes;
- no reemplaza a `DatasetBuilder`;
- no reemplaza a Target Generation;
- no modifica el contrato de `DatasetRow`;
- no modifica el contrato de `Dataset`;
- no decide nuevas Target Definitions;
- no crea una nueva capa arquitectónica.

La forma concreta de implementar esta responsabilidad permanece abierta.

---

## 5. Responsibilities of Dataset Generation Orchestration

La responsabilidad de orquestación dentro de Dataset Generation
consiste conceptualmente en coordinar las etapas necesarias para obtener
observaciones completas destinadas al dataset.

Esta coordinación incluye, como mínimo:

1. recibir o trabajar sobre las unidades de información necesarias para
   generar observaciones;
2. coordinar la construcción de la representación analítica mediante
   `DatasetBuilder`;
3. coordinar la generación del Prediction Target mediante Target
   Generation;
4. permitir que el Prediction Target correspondiente quede asociado con
   la observación que corresponda;
5. producir, una vez definido formalmente el mecanismo de asociación, las
   observaciones completas representables mediante `DatasetRow`;
6. organizar las observaciones completas en un `Dataset`.

Estas responsabilidades son conceptuales.

Este RFC no define todavía la forma técnica concreta de ejecutar cada
operación.

---

## 6. Non-Responsibilities

La responsabilidad de orquestación de Dataset Generation no absorbe las
responsabilidades de los componentes que coordina.

### 6.1 No reemplaza a DatasetBuilder

Dataset Generation no debe convertir a `DatasetBuilder` en un
componente de Machine Learning.

`DatasetBuilder` mantiene su responsabilidad de construir la
representación definida por su specification a partir del estado
analítico según su specification vigente.

DatasetBuilder no debe generar Prediction Targets.

### 6.2 No reemplaza a Target Generation

Dataset Generation no debe convertir la orquestación en la responsable
de calcular el resultado del partido.

Target Generation mantiene la responsabilidad de producir el Prediction
Target correspondiente a una observación, según su specification.

### 6.3 No redefine DatasetRow

La orquestación no modifica la definición de `DatasetRow`.

No introduce campos adicionales.

No cambia su mutabilidad.

No modifica su genericidad.

No redefine el significado de `feature` ni de `target`.

### 6.4 No redefine Dataset

La orquestación no modifica el modelo `Dataset`.

`Dataset` continúa representando una colección coherente y delimitada de
`DatasetRow`.

### 6.5 No define nuevas Target Definitions

La orquestación no puede introducir una nueva definición del problema
predictivo.

La Target Definition vigente para el primer problema predictivo continúa
siendo la definida por la documentación existente de Machine Learning y
Target Generation.

### 6.6 No resuelve las Open Questions pendientes

La orquestación no debe resolver implícitamente ninguna de las
decisiones que todavía permanecen abiertas en Target Generation ni las
decisiones abiertas de este documento.

---

## 7. Conceptual Flow

El flujo conceptual de Dataset Generation puede representarse de la
siguiente manera:

```text
Información necesaria para Dataset Generation
                    |
                    v
          +---------------------+
          | Dataset Generation   |
          | orchestration        |
          +---------------------+
             /             \
            /               \
           v                 v
+-------------------+   +----------------------+
| DatasetBuilder    |   | Target Generation    |
+-------------------+   +----------------------+
           |                     |
           |                     |
           v                     v
  Representación          Prediction Target
  analítica de la              asociado a
  observación                 observación
           \                     /
            \                   /
             \                 /
              v               v
             Asociación pendiente
                    |
                    v
              DatasetRow
                    |
                    v
                 Dataset
                    |
                    v
        Validaciones posteriores
```

Este diagrama es exclusivamente conceptual.

No define:

- una API;
- una secuencia concreta de llamadas;
- una clase denominada "Dataset Generation Orchestrator";
- una clase o función de asociación;
- el orden de invocación entre `DatasetBuilder` y Target Generation;
- una representación intermedia adicional;
- una modificación de `DatasetRow`.

El diagrama tampoco establece que `TeamGameFeature` sea el input directo
de Target Generation.

Target Generation recibe la información necesaria para determinar el
resultado real de la observación de acuerdo con su propia specification.

La forma concreta mediante la cual esa información llega a Target
Generation permanece abierta.

---

## 8. Coordination with DatasetBuilder

`DatasetBuilder` y la orquestación de Dataset Generation tienen
responsabilidades diferentes.

`DatasetBuilder` es responsable de la construcción de la representación
definida por su specification a partir de `TeamGameFeature`.

La orquestación de Dataset Generation es responsable de coordinar esa
operación con las demás etapas necesarias para obtener una observación
completa.

El presente RFC no modifica la specification de `DatasetBuilder`.

En particular, no se establece aquí que `DatasetBuilder` deba:

- conocer Prediction Targets;
- generar labels;
- generar targets;
- calcular resultados;
- consultar Target Generation;
- modificar `DatasetRow`;
- realizar operaciones propias de Machine Learning.

La tensión textual identificada en la Sección 2 permanece documentada
pero no resuelta.

---

## 9. Coordination with Target Generation

Target Generation constituye la responsabilidad encargada de producir
el Prediction Target.

La orquestación de Dataset Generation debe coordinar la salida de Target
Generation con la observación correspondiente.

Esta coordinación no convierte a Target Generation en responsable de
construir `DatasetRow`.

Target Generation:

- produce el Prediction Target;
- no construye `DatasetRow`;
- no construye `Dataset`;
- no decide qué observaciones pertenecen al Dataset;
- no depende de `DatasetBuilder` como dependencia de implementación.

El origen exacto de la información de resultado utilizada por Target
Generation permanece definido por la specification de Target Generation
y sus Open Questions.

---

## 10. Relationship with DatasetRow

`DatasetRow` representa una observación completa que contiene:

- una representación analítica mediante `feature`;
- el Prediction Target correspondiente mediante `target`.

La responsabilidad de orquestación debe permitir que ambos elementos
correspondientes a una misma observación puedan terminar asociados en una
`DatasetRow`.

Sin embargo, este RFC no define todavía el mecanismo técnico concreto
para realizar dicha asociación.

En particular, este documento no introduce:

- un modelo intermedio;
- una nueva clase;
- un nuevo tipo de identidad;
- una nueva estructura de datos;
- un nuevo campo dentro de `DatasetRow`.

La asociación concreta permanece como decisión pendiente.

---

## 11. Relationship with Dataset

Una vez que las observaciones completas puedan representarse mediante
`DatasetRow`, Dataset Generation podrá organizar dichas filas dentro de
un `Dataset`.

`Dataset` permanece como el modelo que contiene una colección coherente
y delimitada de `DatasetRow`.

Este RFC no redefine:

- cómo se almacena `Dataset`;
- cómo se serializa;
- cómo se exporta;
- cómo se versiona;
- cómo se entrena un modelo a partir de él.

Esas responsabilidades pertenecen a etapas posteriores o a otros
componentes de la arquitectura.

---

## 12. Observation Identity

La arquitectura de Machine Learning proporciona un antecedente
conceptual para la identidad de las observaciones del dataset:

`(game_id, team_id)`

Esta correspondencia expresa conceptualmente que una fila representa el
estado de un equipo determinado dentro de un partido determinado.

Este antecedente no resuelve por sí mismo cómo debe representarse la
identidad técnicamente durante la orquestación.

En particular, este RFC no establece que:

- `DatasetRow` deba incorporar nuevos campos de identidad;
- `PredictionTarget` deba contener `game_id`;
- `PredictionTarget` deba contener `team_id`;
- `DatasetBuilder` deba modificarse para producir una nueva estructura;
- deba introducirse un objeto de identidad independiente.

El mecanismo concreto para verificar que un Prediction Target corresponde
a la observación correcta permanece abierto.

---

## 13. One-to-One Correspondence

Conceptualmente, cada observación requiere un Prediction Target
correspondiente al mismo caso observado.

La relación esperada es:

```text
Una observación
      |
      +----> Feature analítica
      |
      +----> Prediction Target correspondiente
      |
      v
   DatasetRow
```

Esta correspondencia debe preservar la identidad de la observación.

No debe producirse una asociación entre:

- una feature de un partido y el resultado de otro partido;
- una feature de un equipo y el resultado de otro equipo;
- una observación y un Prediction Target que corresponda a una
  observación diferente.

Sin embargo, este RFC no define todavía el mecanismo técnico mediante
el cual esta correspondencia será garantizada.

La identidad conceptual `(game_id, team_id)` constituye un antecedente
relevante, pero no se convierte aquí en un contrato técnico nuevo.

---

## 14. Ordering of Operations

Los documentos actuales no determinan de manera suficientemente precisa
si DatasetBuilder debe ejecutarse antes o después de Target Generation
durante la implementación concreta.

Por lo tanto, este RFC no establece un orden obligatorio.

Conceptualmente, ambas operaciones forman parte del mismo proceso de
Dataset Generation:

```text
                 Dataset Generation
                        |
             +----------+----------+
             |                     |
             v                     v
      DatasetBuilder       Target Generation
             |                     |
             +----------+----------+
                        |
                        v
              Asociación pendiente
                        |
                        v
                   DatasetRow
```

La representación anterior no debe interpretarse como ejecución
paralela obligatoria.

Tampoco debe interpretarse como una secuencia concreta de invocaciones.

El orden de operaciones queda como decisión pendiente.

---

## 15. Undeterminable Targets During Orchestration

Target Generation define conceptualmente la existencia de casos en los
que un Prediction Target no puede determinarse debido a información
insuficiente o ausente.

La orquestación de Dataset Generation no debe resolver por sí misma esta
situación.

En particular, no debe introducir silenciosamente:

- `None`;
- `0`;
- `-1`;
- u otro valor artificial

para representar un target no determinable.

El valor `0` continúa siendo semánticamente válido cuando representa una
derrota real.

Lo que permanece prohibido es utilizar `0` como sustituto silencioso de
un resultado desconocido.

El comportamiento concreto ante un target no determinable permanece
ligado a la Open Question 5 de Target Generation.

Por lo tanto, este RFC no decide si una observación con target no
determinable debe:

- excluirse;
- producir un error explícito;
- propagarse como un estado determinado;
- tratarse mediante otro mecanismo.

Cualquier decisión futura deberá documentarse formalmente antes de ser
implementada.

---

## 16. Relationship with Existing Documents

Este RFC debe interpretarse junto con los siguientes documentos:

- `docs/architecture/dataset-generation.md`
- `docs/architecture/machine-learning.md`
- `docs/design/dataset.md`
- `docs/design/dataset-row.md`
- `docs/design/target-generation.md`
- `docs/specifications/dataset-builder.md`
- `docs/specifications/target-generation.md`

La relación documental debe entenderse considerando el estado actual de
cada documento.

En particular:

- `docs/architecture/dataset-generation.md` está en estado **Propuesto**;
- `docs/architecture/machine-learning.md` está en estado **Propuesto**;
- `docs/design/dataset.md` contiene la definición conceptual de
  `Dataset`;
- `docs/design/dataset-row.md` contiene la definición conceptual de
  `DatasetRow`;
- `docs/design/target-generation.md` contiene el RFC de Target
  Generation;
- `docs/specifications/dataset-builder.md` contiene la specification
  de DatasetBuilder;
- `docs/specifications/target-generation.md` contiene la specification
  de Target Generation.

Este RFC no modifica ninguno de esos documentos.

Si una futura decisión arquitectónica modifica el contenido o estado de
alguno de ellos, este RFC deberá revisarse para mantener coherencia
documental.

---

## 17. Architectural Constraints

La orquestación de Dataset Generation debe respetar las restricciones
arquitectónicas de los componentes que coordina.

No debe utilizar la orquestación como mecanismo para introducir
dependencias indebidas entre capas.

En particular, la orquestación no debe convertir:

- Target Generation en una capa de persistence;
- DatasetBuilder en una capa de Machine Learning;
- DatasetRow en un componente de proceso;
- Dataset en un componente de entrenamiento.

La orquestación debe permanecer conceptualmente separada de:

- persistence;
- repositories;
- providers;
- NBA API;
- training;
- inference;
- odds;
- Expected Value;
- Kelly Criterion;
- bankroll.

---

## 18. Preservation of Existing Contracts

La futura implementación de esta responsabilidad deberá preservar los
contratos existentes mientras las decisiones abiertas permanezcan sin
resolver.

En particular:

### DatasetBuilder

No debe modificarse para generar targets mientras su specification
actual continúe estableciendo que no genera Prediction Targets.

### Target Generation

No debe modificarse para construir `DatasetRow` o `Dataset`.

### DatasetRow

No debe modificarse únicamente para hacer ejecutable la orquestación.

### Dataset

No debe modificarse únicamente para introducir la asociación entre
features y targets.

### Target Generation Open Questions

Las cinco Open Questions de Target Generation permanecen intactas.

No pueden resolverse implícitamente mediante la implementación de esta
orquestación.

---

## 19. Architectural Principles

La responsabilidad descrita en este RFC debe seguir los siguientes
principios:

### 19.1 Separation of Responsibilities

Cada responsabilidad debe permanecer en el componente que la define.

DatasetBuilder construye la representación analítica según su contrato.

Target Generation produce el Prediction Target según su contrato.

Dataset Generation coordina las etapas.

DatasetRow representa la observación completa.

Dataset contiene las filas.

### 19.2 No Premature Abstraction

No debe introducirse una abstracción de código únicamente para
representar la orquestación mientras los documentos fuente no hayan
determinado que dicha abstracción sea necesaria.

### 19.3 No Hidden Semantics

Ninguna decisión pendiente debe resolverse mediante valores
placeholder, convenciones implícitas o comportamiento accidental.

### 19.4 Deterministic Coordination

La futura coordinación debe preservar el determinismo exigido por
Dataset Generation, DatasetBuilder y Target Generation.

### 19.5 Temporal Integrity

La orquestación no debe convertir información posterior al partido en
una feature.

El resultado final del partido puede utilizarse para producir el
Prediction Target, de acuerdo con Target Generation.

### 19.6 Traceability

La asociación entre una observación y su Prediction Target debe ser
verificable cuando el mecanismo concreto sea definido.

### 19.7 Minimal Architecture

No debe introducirse un componente independiente cuando una
responsabilidad ya existente dentro de Dataset Generation sea suficiente
para coordinar el proceso.

---

## 20. Data Leakage Boundary

La orquestación debe preservar la separación entre:

- información utilizada como feature;
- información utilizada como Prediction Target.

Las features analíticas deben representar información permitida para el
problema predictivo.

El resultado final del partido pertenece al Prediction Target y no debe
reintroducirse como feature.

Por lo tanto, la coordinación no debe modificar el contenido semántico
de una feature para incorporar información posterior al inicio del
partido.

La validación formal de ausencia de leakage corresponde a las etapas de
validación de Dataset Generation y no se resuelve en este RFC.

---

## 21. Consistency Boundary

La responsabilidad de orquestación no sustituye las validaciones
posteriores de Dataset Generation.

No corresponde a este documento definir:

- validación completa de columnas;
- detección de duplicados;
- validación estadística;
- validación de leakage;
- validación de consistencia del Dataset;
- exportación;
- versionado.

Estas responsabilidades pertenecen a etapas posteriores del flujo de
Dataset Generation.

---

## 22. Future Implementation Boundary

La implementación futura de la orquestación deberá esperar a que las
decisiones necesarias hayan sido formalizadas.

En particular, no debe asumirse durante implementación:

- una representación definitiva de `PredictionTarget`;
- una representación definitiva de `Target Definition`;
- un origen concreto de los puntos finales distinto del que se formalice;
- un mecanismo concreto de asociación entre target y `DatasetRow`;
- un comportamiento definitivo ante targets no determinables;
- un orden obligatorio entre DatasetBuilder y Target Generation.

La ausencia de una decisión explícita no debe convertirse en una
decisión accidental mediante código.

---

## 23. Open Questions

Las siguientes decisiones permanecen abiertas.

### 23.1 Mecanismo de asociación

¿Cuál será el mecanismo técnico concreto mediante el cual una
observación y su Prediction Target correspondiente se asociarán para
producir una `DatasetRow` válida?

### 23.2 Orden de operaciones

¿Debe ejecutarse primero DatasetBuilder, primero Target Generation, o
debe existir otra estrategia de coordinación?

### 23.3 Revisión de DatasetBuilder

¿La tensión textual identificada en
`docs/specifications/dataset-builder.md` requiere una revisión formal de
dicha specification, o puede resolverse mediante coordinación sin
modificarla?

Esta decisión no se toma en este RFC.

### 23.4 Targets no determinables

¿Cómo debe comportarse la orquestación cuando Target Generation no puede
determinar un target?

Esta pregunta permanece ligada a la Open Question 5 de Target Generation.

### 23.5 Forma técnica de la orquestación

¿La responsabilidad de orquestación se implementará mediante una función,
una clase, un pipeline u otra estructura?

No se decide aquí.

### 23.6 Open Questions de Target Generation

Las cinco Open Questions de Target Generation permanecen intactas:

1. Representación concreta de `PredictionTarget`.
2. Representación concreta de `Target Definition` como componente de
   código.
3. Origen exacto de la información del resultado.
4. Mecanismo de asociación entre Prediction Target y `DatasetRow`.
5. Comportamiento ante targets no determinables.

Ninguna de estas preguntas queda resuelta por este RFC.

---

## 24. Future Evolution

La responsabilidad de orquestación podrá evolucionar cuando las
decisiones abiertas sean formalizadas.

Una evolución futura podrá:

- definir el mecanismo concreto de asociación;
- establecer el orden de las operaciones;
- determinar la representación definitiva de `PredictionTarget`;
- formalizar el comportamiento ante targets no determinables;
- revisar `DatasetBuilder` si resulta necesario;
- definir la implementación concreta de la coordinación.

Cualquier evolución deberá mantener la separación de responsabilidades y
evitar introducir componentes adicionales sin una necesidad
arquitectónica demostrada.

La extensión hacia otros problemas predictivos, como:

- spread;
- totals;
- player props;

queda fuera del alcance actual y requerirá decisiones arquitectónicas y
documentación propias.

---

## 25. Acceptance Criteria

Este RFC será considerado coherente con la arquitectura cuando:

- describa la orquestación como una responsabilidad interna de Dataset
  Generation;
- no introduzca Dataset Row Assembly como componente independiente;
- no introduzca un componente arquitectónico obligatorio llamado
  "Dataset Generation Orchestrator";
- reconozca explícitamente la tensión textual existente en
  `dataset-builder.md`;
- no resuelva unilateralmente dicha tensión;
- no modifique `DatasetBuilder`;
- no modifique `DatasetRow`;
- no modifique `Dataset`;
- no modifique Target Generation;
- mantenga intactas las cinco Open Questions de Target Generation;
- reconozca que `dataset-generation.md` está actualmente en estado
  Propuesto;
- reconozca que `machine-learning.md` está actualmente en estado
  Propuesto;
- reconozca `(game_id, team_id)` como antecedente conceptual de
  identidad sin convertirlo en un mecanismo técnico nuevo;
- no muestre a `TeamGameFeature` como origen directo obligatorio de
  Target Generation;
- no muestre a `DatasetBuilder` produciendo de forma independiente una
  `DatasetRow` completa;
- no presente dos `DatasetRow` diferentes con significados distintos;
- no introduzca un modelo intermedio no documentado;
- mantenga abierto el mecanismo de asociación;
- mantenga abierto el orden de invocación;
- mantenga abierto el comportamiento ante targets no determinables;
- mantenga abierta la forma técnica de implementación;
- preserve la separación entre features y Prediction Targets;
- preserve la integridad temporal;
- no introduzca lógica de Machine Learning adicional;
- no introduzca persistence, repositories, providers, odds, EV, Kelly o
  bankroll;
- no resuelva decisiones pendientes mediante placeholders o
  comportamiento implícito.

---

## 26. Files Affected by This RFC

Este RFC describe conceptualmente la responsabilidad de orquestación de
Dataset Generation.

No requiere modificaciones a otros documentos para existir como
documento Propuesto.

Los siguientes documentos permanecen sin modificación como consecuencia
de este RFC:

- `docs/architecture/dataset-generation.md`
- `docs/architecture/machine-learning.md`
- `docs/design/dataset.md`
- `docs/design/dataset-row.md`
- `docs/design/target-generation.md`
- `docs/specifications/dataset-builder.md`
- `docs/specifications/target-generation.md`

Los modelos existentes tampoco se modifican:

- `src/sportsquant/datasets/dataset.py`
- `src/sportsquant/datasets/dataset_row.py`
- `src/sportsquant/targets/target_generation.py`

Este RFC tampoco requiere código ni tests.

---

## 27. Implementation Status

No existe todavía una implementación de esta responsabilidad.

Este documento no autoriza por sí mismo la creación de:

- una clase;
- una función;
- un pipeline;
- un servicio;
- un repository;
- un nuevo modelo;
- una nueva estructura de datos.

La implementación deberá comenzar únicamente después de que las
decisiones necesarias hayan sido formalizadas y el contrato técnico
correspondiente haya sido aprobado.

---

## 28. Summary

Dataset Generation ya posee conceptualmente la responsabilidad de
coordinar el proceso de generación de datasets.

Este RFC no crea una nueva responsabilidad arquitectónica independiente.

Su finalidad es documentar con mayor precisión cómo esa responsabilidad
debe coordinar las piezas existentes, especialmente:

```text
DatasetBuilder
      +
Target Generation
      |
      v
Asociación de la observación con su target
      |
      v
DatasetRow
      |
      v
Dataset
```

La tensión textual existente en `dataset-builder.md` queda reconocida
explícitamente y no se resuelve mediante este documento.

El mecanismo técnico de asociación permanece abierto.

El orden de operaciones permanece abierto.

El comportamiento ante targets no determinables permanece abierto.

La forma técnica de implementar la orquestación permanece abierta.

Las cinco Open Questions de Target Generation permanecen intactas.

`docs/architecture/dataset-generation.md` y
`docs/architecture/machine-learning.md` son actualmente documentos
Propuestos, por lo que este RFC los utiliza como contexto arquitectónico
vigente sin tratarlos como decisiones Frozen.

Este documento, por tanto, formaliza el detalle pendiente de una
responsabilidad de orquestación ya perteneciente a Dataset Generation,
sin introducir un nuevo componente arquitectónico ni resolver
prematuramente decisiones que todavía requieren diseño.