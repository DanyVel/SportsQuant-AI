# Target Generation — Architecture Review

**Proyecto:** SportsQuant-AI
**Capa:** Dataset Generation / Target Generation
**Estado:** Architecture Review — Corrected
**Propósito:** Consolidar las conclusiones arquitectónicas actuales, registrar contradicciones documentales detectadas y establecer con precisión qué decisiones permanecen abiertas antes de continuar con `DatasetBuilder`.

---

# 1. Contexto

Durante el diseño de Dataset Generation se identificó una dependencia conceptual entre `DatasetRow` y la generación del prediction target.

Actualmente, `DatasetRow` requiere dos elementos:

* `feature`
* `target`

Sin embargo, `DatasetBuilder` fue definido explícitamente como un componente que:

* transforma representaciones analíticas;
* no conoce conceptos de Machine Learning;
* no genera labels;
* no genera prediction targets;
* no calcula ni deriva el target de una observación.

Por lo tanto, `DatasetBuilder` no puede construir correctamente un `DatasetRow` completo si no existe previamente un mecanismo independiente responsable de producir el target.

Esto motivó la incorporación de la capa **Target Generation** y la suspensión temporal de la implementación de `DatasetBuilder`.

La revisión arquitectónica posterior identificó además contradicciones documentales que deben resolverse antes de continuar.

---

# 2. Principios arquitectónicos establecidos

## 2.1 Separación entre Feature Engineering y Target Generation

Feature Engineering y Target Generation representan transformaciones conceptualmente distintas.

Feature Engineering produce la representación analítica de una observación.

Target Generation produce el resultado observado que será utilizado como prediction target.

Conceptualmente:

```text
Historical Game
      │
      ├──> Feature Engineering ──> TeamGameFeature
      │
      └──> Target Generation ─────> PredictionTarget
```

Ninguna de estas responsabilidades debe absorber a la otra.

---

## 2.2 DatasetBuilder no genera targets

`DatasetBuilder` no debe:

* calcular resultados;
* determinar ganadores;
* generar labels;
* interpretar resultados deportivos;
* derivar prediction targets;
* contener lógica específica de Machine Learning.

Su responsabilidad permanece limitada a la construcción del Dataset a partir de representaciones que ya contienen la información necesaria.

---

## 2.3 Target Definition ≠ Prediction Target

Debe distinguirse entre:

### Target Definition

Define **qué se desea predecir**.

Ejemplo:

```text
team wins game
```

### Prediction Target

Representa **el resultado observado concreto** de una observación histórica.

Ejemplo:

```text
WIN
```

Esta separación es conceptual y no implica todavía una decisión sobre una representación técnica concreta de `Target Definition`.

---

## 2.4 El target no debe obtenerse conceptualmente desde TeamGameFeature

Aunque una implementación concreta pueda contener información suficiente para calcular el resultado, `TeamGameFeature` representa una salida de Feature Engineering y no debe convertirse en la fuente conceptual del target.

La arquitectura debe permitir mantener separadas:

```text
Historical Game
      │
      ├──> TeamGameFeature
      │
      └──> PredictionTarget
```

Esto reduce el acoplamiento entre Feature Engineering y Target Generation y permite controlar explícitamente los límites relacionados con data leakage.

---

## 2.5 Target Generation permanece independiente de infraestructura

Target Generation debe permanecer independiente de:

* SQLAlchemy;
* ORM;
* Session;
* Repository;
* NBA API;
* proveedores externos;
* DatasetBuilder;
* Dataset;
* DatasetRow;
* Machine Learning.

La responsabilidad de Target Generation es producir el resultado objetivo a partir de la información histórica necesaria, no ensamblar el Dataset.

---

# 3. Terminología de "Observation"

El término **Observation** aparece en este Architecture Review como una herramienta conceptual para razonar sobre la correspondencia entre una representación analítica y su resultado observado.

Sin embargo:

> **Observation NO constituye actualmente una entidad de dominio, Value Object, modelo, interfaz ni contrato técnico del sistema.**

Tampoco se debe crear una clase `Observation` ni introducir una nueva abstracción de código a partir de este documento.

Por ahora debe entenderse simplemente como lenguaje arquitectónico descriptivo.

La identidad técnica de una observación permanece abierta.

En particular, aunque:

```text
(game_id, team_id)
```

sea una forma natural de describir conceptualmente una observación de equipo dentro de un partido, esto **no constituye todavía una decisión técnica congelada**.

---

# 4. OQ1 — Representación de PredictionTarget

## Estado

**ABIERTO**

La implementación actual utiliza provisionalmente:

```python
int
```

con:

```text
1 = win
0 = loss
```

Esta representación funciona para el caso actual, pero no constituye todavía una decisión arquitectónica definitiva.

### Alternativas consideradas

#### A. Mantener `int`

Ventajas:

* simple;
* compatible con ML;
* fácil de serializar.

Desventajas:

* semántica débil;
* permite valores inválidos;
* mezcla representación matemática con significado de dominio.

#### B. Value Object `PredictionTarget`

Ventajas:

* expresa semántica;
* permite proteger invariantes;
* desacopla el dominio de una representación primitiva.

Desventajas:

* mayor abstracción;
* requiere definir correctamente su contrato.

#### C. Enum

Ventajas:

* expresivo para el caso win/loss.

Desventajas:

* puede acoplar el concepto a una clasificación concreta;
* podría resultar insuficiente para futuros tipos de mercados o targets.

### Conclusión

No implementar ni congelar todavía ninguna alternativa.

La representación definitiva debe evaluarse considerando el alcance futuro de Target Generation y los tipos de targets que SportsQuant-AI deberá soportar.

---

# 5. OQ2 — Target Definition

## Estado

**SEMÁNTICAMENTE ESTABLECIDO / REPRESENTACIÓN TÉCNICA ABIERTA**

La arquitectura debe reconocer conceptualmente una diferencia entre:

```text
qué queremos predecir
```

y:

```text
qué ocurrió realmente
```

Por ejemplo:

```text
Target Definition:
    team wins game

Prediction Target:
    WIN
```

La representación técnica de `Target Definition` permanece abierta.

No debe introducirse prematuramente:

* una clase;
* una estrategia;
* una interfaz;
* una configuración;
* una jerarquía de tipos;

sin determinar primero qué responsabilidades debe soportar el concepto.

---

# 6. OQ3 — Fuente de información para Target Generation

## Estado

**DIRECCIÓN SEMÁNTICA ESTABLECIDA / CONTRATO TÉCNICO ABIERTO**

Target Generation necesita información observada del evento deportivo.

Para el caso actual de win/loss, la fuente conceptual es el resultado real del partido, determinado mediante la comparación de los puntos finales.

Conceptualmente:

```text
Historical Game
      │
      └──> Target Generation
                  │
                  └──> PredictionTarget
```

El empate se encuentra fuera del alcance actual y no debe introducirse una categoría adicional sin una decisión arquitectónica explícita.

El contrato técnico exacto de entrada de Target Generation permanece abierto.

No se debe introducir todavía un nuevo Value Object únicamente por anticipación.

---

# 7. OQ4 — Asociación entre representación analítica y PredictionTarget

## Estado

**PRINCIPIO CERRADO / MECANISMO TÉCNICO ABIERTO / BLOQUEANTE**

La asociación entre una representación analítica y su target debe depender de identidad semántica.

No debe depender exclusivamente de la posición dentro de colecciones.

Por ejemplo, no debe asumirse arquitectónicamente:

```python
zip(features, targets)
```

como mecanismo suficiente de identidad.

La correspondencia debe garantizar que el target pertenece a la misma observación representada por el feature.

Sin embargo, el mecanismo técnico exacto mediante el cual esta correspondencia se materializará en `Dataset Generation` permanece abierto.

Esta cuestión es actualmente el **principal bloqueo técnico para `DatasetBuilder`**.

La resolución de OQ4 debe preceder a la implementación de `DatasetBuilder`.

---

# 8. OQ5 — Target indeterminable

## Estado

**REGLA SEMÁNTICA CERRADA / POLÍTICA DE DATASET ABIERTA**

Ya existe:

```python
UndeterminableTargetError
```

para representar la imposibilidad de determinar un target debido a información insuficiente.

Debe mantenerse una distinción estricta:

```text
Undeterminable Target
        ≠
Loss
```

Por lo tanto, valores como:

```text
None
0
-1
UNKNOWN
```

no deben utilizarse arbitrariamente como placeholders para representar un target indeterminable.

En particular:

```text
0 = Loss
```

por lo que utilizar `0` como placeholder produciría información incorrecta.

### Regla arquitectónica

Un target indeterminable **no constituye un PredictionTarget válido**.

Por consecuencia, una observación cuyo target no pueda determinarse no puede convertirse silenciosamente en un `DatasetRow` válido.

### Política pendiente

Todavía debe decidirse qué hará Dataset Generation cuando encuentre una observación cuyo target no pueda determinarse.

Alternativas:

* abortar toda la generación;
* excluir la observación;
* utilizar una política configurable.

Esta decisión permanece abierta.

---

# 9. Contradicciones documentales identificadas

## 9.1 Contradicción A — Orden de operaciones

Existe una discrepancia entre la estrategia descrita en:

```text
docs/architecture/machine-learning.md
```

y la sección de orden de operaciones de:

```text
docs/design/dataset-generation-orchestration.md
```

El primer documento presenta un pipeline donde aparece:

```text
Analytical Feature Models
        ↓
Dataset Row Construction
        ↓
Target Generation
```

Mientras que el segundo documento mantiene abierto si `DatasetBuilder` debe ejecutarse antes o después de Target Generation.

### Problema

No está claro si el orden mostrado en `machine-learning.md` es:

* un pipeline normativo;
* o únicamente una representación conceptual.

### Acción requerida

Debe aclararse explícitamente el carácter vinculante o ilustrativo del orden.

Esta aclaración debe realizarse antes de implementar `DatasetBuilder`.

---

# 10. Contradicción documental B — DatasetBuilder vs DatasetRow

Existe una discrepancia entre:

```text
docs/specifications/dataset-builder.md
```

y el contrato actual de:

```text
DatasetRow
```

`DatasetRow` requiere obligatoriamente:

```text
feature
target
```

Mientras que el Construction Flow de `DatasetBuilder` describe la construcción de un `DatasetRow` a partir de `TeamGameFeature` sin explicar cómo se incorpora el target requerido.

### Problema

El flujo descrito literalmente no puede producir un `DatasetRow` válido bajo el contrato actual sin introducir una responsabilidad no autorizada en `DatasetBuilder`.

### Consecuencia

`dataset-builder.md` no debe considerarse directamente implementable mientras OQ4 y la composición entre feature y target permanezcan sin resolver.

### Acción requerida

Debe añadirse una aclaración documental indicando que el Construction Flow está sujeto a la resolución del mecanismo de asociación y composición.

No se debe modificar `DatasetRow` para solucionar esta contradicción sin una decisión arquitectónica específica.

---

# 11. Contradicción documental C — Estado Propuesto vs Frozen

Se identificó una discrepancia entre:

```text
docs/specifications/dataset-model.md
```

y los estados declarados por:

```text
docs/architecture/dataset-generation.md
docs/architecture/machine-learning.md
```

Los documentos de arquitectura se identifican actualmente como:

```text
Status: Propuesto
```

Por lo tanto, cualquier documento que los describa como arquitecturas "ya congeladas" debe corregirse.

### Acción requerida

La documentación debe utilizar consistentemente:

```text
Propuesto
```

hasta que exista una decisión formal que cambie su estado a:

```text
Frozen
```

---

# 12. Estado de las decisiones

| Tema                                               | Estado                      |
| -------------------------------------------------- | --------------------------- |
| Separación Feature Engineering / Target Generation | **CERRADO**                 |
| DatasetBuilder no genera targets                   | **CERRADO**                 |
| Target Definition ≠ Prediction Target              | **CERRADO conceptualmente** |
| Representación técnica de Target Definition        | **ABIERTO**                 |
| Fuente conceptual del target                       | **CERRADO**                 |
| Input técnico de Target Generation                 | **ABIERTO**                 |
| Asociación por identidad, no por posición          | **CERRADO como principio**  |
| Mecanismo técnico de asociación                    | **ABIERTO — BLOQUEANTE**    |
| Observation como entidad técnica                   | **NO ESTABLECIDO**          |
| Identidad técnica de Observation                   | **ABIERTO**                 |
| Target indeterminable ≠ Loss                       | **CERRADO**                 |
| Política ante target indeterminable                | **ABIERTO**                 |
| Representación técnica de PredictionTarget         | **ABIERTO**                 |
| Orden DatasetBuilder ↔ Target Generation           | **ABIERTO**                 |

---

# 13. Límites de implementación

Hasta resolver las cuestiones anteriores, no deben realizarse los siguientes cambios:

* implementar `DatasetBuilder`;
* modificar `DatasetRow`;
* introducir lógica de target en `DatasetBuilder`;
* utilizar `None` como target válido;
* utilizar `0` como placeholder;
* introducir una entidad `Observation`;
* introducir una entidad independiente de "Dataset Row Assembly";
* introducir infraestructura;
* introducir dependencias con SQLAlchemy;
* introducir dependencias con la NBA API;
* introducir Machine Learning;
* introducir modelos predictivos;
* introducir entrenamiento;
* congelar prematuramente `PredictionTarget`;
* congelar prematuramente la identidad técnica de Observation.

---

# 14. Próximo paso arquitectónico

El siguiente paso debe ser un **Design RFC dedicado exclusivamente a OQ4**:

> **¿Cómo debe asociarse técnicamente la representación analítica de una observación con su `PredictionTarget` para producir un `DatasetRow` válido, sin transferir la responsabilidad de Target Generation a `DatasetBuilder`?**

Ese RFC deberá analizar:

1. posibles mecanismos de asociación;
2. responsabilidad de Dataset Generation Orchestration;
3. responsabilidad de DatasetBuilder;
4. responsabilidad de Target Generation;
5. relación con `DatasetRow`;
6. orden de operaciones;
7. garantías de 1:1;
8. prevención de asociaciones incorrectas;
9. implicaciones para determinismo y reproducibilidad.

No debe resolver otras Open Questions salvo que la resolución de OQ4 las afecte directamente.

Después de aprobar OQ4:

```text
OQ4 Design RFC
      ↓
Architecture Review
      ↓
OQ4 Decision
      ↓
resolver Contradicción A
      ↓
resolver Contradicción B
      ↓
actualizar DatasetBuilder Specification
      ↓
implementar DatasetBuilder
```

Hasta entonces, `DatasetBuilder` permanece suspendido.
