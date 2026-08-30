# Target Generation — Implementation Specification

## Status

Frozen

---

## 1. Objective

Definir formalmente la responsabilidad de **Target Generation** dentro de SportsQuant-AI: el componente encargado de producir el **Prediction Target** correspondiente a una observación, a partir de la información del resultado real de un partido.

Esta specification documenta el contrato, las reglas y las restricciones arquitectónicas aprobadas para Target Generation, sin introducir decisiones de implementación que aún no han sido formalizadas.

---

## 2. Scope

Esta specification cubre exclusivamente:

- La responsabilidad conceptual de Target Generation.
- Su relación con Target Definition, Analytical Feature Model, Dataset Generation y DatasetRow.
- Las reglas de generación del target para el primer problema predictivo (victoria/derrota).
- Las restricciones de dependencias y de responsabilidades prohibidas.
- Los criterios de determinismo, reproducibilidad e integridad temporal.
- El tratamiento de targets no determinables a nivel conceptual.

Esta specification **no** cubre:

- La implementación concreta en código de Target Generation.
- La representación concreta de `PredictionTarget`.
- La representación concreta de `Target Definition` como componente de código.
- La integración concreta entre Target Generation y DatasetBuilder.
- Cualquier decisión sobre empates más allá de excluirlos del alcance actual.

---

## 3. Relationship with Target Definition

Target Definition y Target Generation son responsabilidades distintas:

- **Target Definition** expresa el problema predictivo y determina qué resultado representa el Prediction Target.
- **Target Generation** aplica esa definición a la información necesaria y produce el Prediction Target correspondiente.

Target Generation depende conceptualmente de una Target Definition, pero esta specification no determina si Target Definition será representada como una clase, interfaz, función, enum u otra abstracción de código. Esa decisión permanece como Open Question (ver Sección 15).

---

## 4. Relationship with Analytical Feature Model

Los Analytical Feature Models, tal como se definen en `docs/architecture/feature-engineering.md`, representan información disponible **antes** del partido.

Target Generation es conceptualmente independiente de la generación de Analytical Feature Models:

- No calcula features.
- No depende de `TeamGameFeature`, calculators, `TeamGameFeatureBuilder` ni `TeamGameFeatureEnricher` como dependencias de implementación.
- No transforma el Prediction Target en una feature.

El origen exacto de dónde provienen los puntos finales del partido dentro de los Analytical Feature Models existentes **no está determinado** por esta specification (ver Open Question 3).

---

## 5. Relationship with Dataset Generation and DatasetRow

Target Generation produce el Prediction Target. No participa en el ensamblaje de observaciones ni en la construcción de conjuntos:

- Target Generation **no** construye `DatasetRow`.
- Target Generation **no** construye `Dataset`.
- Target Generation **no** modifica `DatasetRow`.
- Target Generation **no** decide qué observaciones pertenecen a un Dataset.

`DatasetRow` es un dataclass genérico (`DatasetRow(Generic[AnalyticalFeatureT, TargetT])`) que requiere un target para representar una observación completa. El mecanismo concreto mediante el cual el Prediction Target producido por Target Generation se asocia con una `DatasetRow` **no está definido** por esta specification (ver Open Question 4).

Adicionalmente, se reafirma que:

- **DatasetBuilder no genera Prediction Targets.**
- DatasetBuilder debe permanecer libre de conceptos de Machine Learning.
- La integración concreta entre Target Generation, DatasetBuilder y DatasetRow queda para trabajo posterior y no se resuelve en esta specification (ver Sección 16).

---

## 6. Contract

### 6.1 Responsabilidad concreta

Target Generation es responsable únicamente de:

- Recibir la información necesaria para determinar el resultado de una observación.
- Aplicar la Target Definition correspondiente al primer problema predictivo.
- Producir el Prediction Target resultante.

Target Generation **no** es responsable de obtener, persistir, transformar o validar la información de origen más allá de lo estrictamente necesario para producir el target.

### 6.2 Inputs

Target Generation recibe la información necesaria para determinar el resultado de la observación (por ejemplo, los puntos anotados por el equipo representado y por el oponente al finalizar el partido), ya provista por quien lo invoca.

Target Generation **no** accede directamente a persistence ni a proveedores externos para obtener esta información.

### 6.3 Outputs

Target Generation produce un Prediction Target correspondiente al problema predictivo definido.

Para el primer problema predictivo:

- `1` representa victoria.
- `0` representa derrota.

La representación concreta del Prediction Target (tipo dedicado, entero, booleano u otra) **no está decidida** por esta specification (ver Open Question 1).

---

## 7. Generation Rules

Para el primer problema predictivo — estimar la probabilidad de que un equipo gane un partido dado su estado antes del mismo — el target se determina comparando los puntos anotados por el equipo representado por la observación contra los puntos anotados por el oponente, ambos al finalizar el partido:

- Si `team_points > opponent_points` → victoria (`1`).
- Si `team_points < opponent_points` → derrota (`0`).

Los documentos fuente no contemplan explícitamente el caso de empate. Por lo tanto, esta specification no introduce un tercer resultado; el tratamiento de empates queda fuera del alcance actual. Cualquier extensión futura sobre este punto requiere una decisión y documentación formal independientes.

`0` como resultado de una derrota real es un valor semántico válido y debe tratarse como tal.

`0` **no** puede utilizarse como un marcador silencioso de "resultado desconocido". Tampoco pueden utilizarse `None`, `-1` u otro valor artificial como sustituto silencioso de un target no determinable. Ver Sección 10.

---

## 8. Determinism and Reproducibility

Target Generation debe ser determinista: dada la misma información de entrada, debe producir siempre el mismo Prediction Target.

Target Generation debe ser reproducible: no debe depender de estado externo mutable, de aleatoriedad, ni de información que pueda variar entre ejecuciones para una misma observación.

---

## 9. Temporal Integrity

El Prediction Target representa el resultado real del partido, mientras que los Analytical Feature Models representan información disponible antes del partido.

Utilizar el resultado final del partido para producir el Prediction Target no constituye, por sí mismo, data leakage. El leakage aparecería si ese resultado se incorporara incorrectamente como feature.

En consecuencia:

- Target Generation puede consumir el resultado real del partido para producir el target.
- Target Generation **no** debe convertir ese resultado en una feature.
- Target Generation **no** debe consumir información de otros partidos para producir el target de la observación actual.

Esta specification no introduce ventanas temporales adicionales.

---

## 10. Invalid / Unavailable Targets

Puede existir una observación cuyo resultado no esté disponible o esté incompleto (por ejemplo: partido no finalizado, resultado ausente, información insuficiente).

Ante esta situación:

- No debe producirse silenciosamente `None`, `0`, `-1` u otro placeholder para fingir que existe un target válido.
- La especificación distingue conceptualmente entre (1) un Prediction Target válido y (2) un target no determinable.
- La futura representación concreta de `PredictionTarget` debe permitir distinguir inequívocamente entre ambos casos.

El comportamiento exacto del sistema ante un target no determinable (exclusión de la observación, señalización de error explícito, u otro mecanismo) **no está decidido** por esta specification (ver Open Question 5).

---

## 11. Architectural Constraints

### 11.1 Dependencias permitidas

Target Generation puede depender de:

- La información necesaria ya provista para determinar el resultado de la observación.
- Una Target Definition (cuya representación concreta permanece como Open Question).

### 11.2 Dependencias prohibidas

Target Generation debe permanecer independiente de:

- SQLAlchemy, ORM, Session.
- Persistence, Repositories, Providers.
- NBA API y cualquier proveedor externo.
- pandas, DataFrames.
- Training Pipeline, Inference Pipeline, modelos de Machine Learning, entrenamiento, inferencia.
- Odds, EV, Kelly, bankroll.
- `DatasetBuilder`, `Dataset` y `DatasetRow` como dependencias de implementación.

### 11.3 Responsabilidades prohibidas

Target Generation no debe:

- Construir ni modificar `DatasetRow`.
- Construir `Dataset`.
- Decidir qué observaciones pertenecen a un Dataset.
- Entrenar modelos de Machine Learning.
- Generar predicciones.
- Evaluar modelos.
- Calcular probabilidades, odds, EV, ni gestionar Kelly o bankroll.
- Acceder directamente a persistence o a proveedores externos.

---

## 12. Files to Create

La ubicación definitiva del módulo de código para Target Generation no está decidida y se determinará durante la implementación futura. Cualquier referencia a una ubicación (por ejemplo, `src/sportsquant/datasets/`) es no vinculante y no debe presentarse como requisito.

---

## 13. Testability Requirements

Target Generation debe diseñarse de forma que sea testeable de manera aislada:

- Debe poder verificarse de forma determinista que, dada la misma información de entrada, se produce siempre el mismo Prediction Target.
- Debe poder verificarse la regla de generación para el primer problema predictivo (victoria/derrota) de forma independiente de persistence, proveedores externos, Machine Learning u otros componentes prohibidos en la Sección 11.2.
- Debe poder verificarse que un caso de resultado no disponible o incompleto no produce silenciosamente un placeholder inválido.

Esta specification no define casos de prueba concretos ni implementación de tests; corresponde a trabajo de implementación futuro.

---

## 14. Acceptance Criteria

Esta Implementation Specification se considera completa cuando:

- Documenta la responsabilidad de Target Generation de forma consistente con `docs/design/target-generation.md` (Frozen).
- Incorpora las reglas de generación del target para el primer problema predictivo.
- Documenta explícitamente la distinción entre `0` como derrota válida y `0` como placeholder prohibido.
- Documenta explícitamente que el empate queda fuera de alcance, sin atribuir esta decisión a una regla externa de la NBA.
- Documenta las dependencias y responsabilidades prohibidas.
- Mantiene abiertas, sin resolverlas, las cinco Open Questions listadas en la Sección 15.
- No introduce código, tests, ni modificaciones a `DatasetRow`, `Dataset`, `DatasetBuilder` o a ningún RFC existente.

---

## 15. Open Questions / Pending Decisions

Las siguientes cinco Open Questions permanecen explícitamente abiertas y no deben resolverse implícitamente durante la implementación:

1. **Representación concreta de PredictionTarget.** No está decidido si será un tipo dedicado, un entero, un booleano u otra representación.
2. **Representación concreta de Target Definition como componente de código.** No está decidido si será una clase, interfaz, función, enum u otra abstracción.
3. **Origen exacto de la información del resultado.** No está determinado exactamente de dónde salen los puntos finales dentro de los Analytical Feature Models existentes.
4. **Mecanismo de asociación entre Prediction Target y DatasetRow.** `DatasetRow` es inmutable y requiere target, pero no está definido el mecanismo concreto mediante el cual el target producido se asocia con la DatasetRow.
5. **Comportamiento ante targets no determinables.** No está decidido si se excluye la observación, se lanza o señala un error explícito, o se utiliza otro mecanismo.

---

## 16. Dependency on Future Work

La integración concreta entre Target Generation, DatasetBuilder y DatasetRow requiere una decisión y documentación formal posteriores, y no se resuelve en esta specification.

La implementación de DatasetBuilder permanece suspendida hasta que dicha integración sea formalmente especificada. No debe implementarse DatasetBuilder sin esa especificación previa.

---

## 17. Summary

Target Generation es la responsabilidad encargada de producir el Prediction Target a partir de la información necesaria del resultado real de un partido, aplicando una Target Definition. Es conceptualmente independiente de Feature Engineering, Dataset Generation, DatasetBuilder, Machine Learning, persistence y proveedores externos.

Para el primer problema predictivo, el target es binario (`1` = victoria, `0` = derrota), determinado por comparación de puntos al finalizar el partido, sin introducir un tercer resultado para empates. `0` es válido como derrota real, pero no puede usarse como placeholder de resultado desconocido.

Esta specification preserva, sin resolverlas, las cinco Open Questions relativas a la representación de PredictionTarget, la representación de Target Definition, el origen de los puntos finales, el mecanismo de asociación con DatasetRow, y el comportamiento ante targets no determinables. La integración con DatasetBuilder queda pendiente de decisión formal futura.