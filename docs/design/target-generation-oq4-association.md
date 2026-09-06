Target Generation — OQ4 Association

Proyecto: SportsQuant-AI
Área: Dataset Generation / Target Generation
Tipo: Architecture Decision Record (ADR)
Estado: Decided

Objetivo: Registrar la decisión arquitectónica de OQ4 sobre el mecanismo técnico mediante el cual una representación analítica y su PredictionTarget se asocian correctamente para producir un DatasetRow.

1. Contexto

SportsQuant-AI separa explícitamente las responsabilidades de:

Feature Engineering;

Target Generation;

Dataset Generation;

DatasetBuilder;

Machine Learning.

Feature Engineering produce representaciones analíticas, actualmente mediante TeamGameFeature.

Target Generation produce el resultado observado que constituye el PredictionTarget.

DatasetRow representa una combinación de:

feature + target

y actualmente requiere ambos elementos.

Por otra parte, DatasetBuilder está definido explícitamente como un componente que:

transforma representaciones analíticas;

construye el Dataset;

no genera targets;

no calcula resultados deportivos;

no conoce conceptos de Machine Learning;

no deriva ni calcula prediction targets.

Esta separación genera una cuestión arquitectónica:

Si DatasetRow requiere un feature y un target, ¿cómo se establece técnicamente la correspondencia entre ambos sin transferir la responsabilidad de Target Generation a DatasetBuilder?

Esta cuestión corresponde a OQ4.

2. Problema arquitectónico

El problema no consiste simplemente en combinar dos objetos.

La arquitectura debe garantizar simultáneamente:

que el target corresponde al mismo evento y entidad deportiva que el feature;

que no existe asociación accidental por posición;

que cada observación válida tiene como máximo un target correspondiente;

que no se utilicen placeholders para representar targets indeterminables;

que DatasetBuilder no genere ni interprete targets;

que Target Generation no asuma responsabilidades de Dataset Generation;

que la asociación sea determinista y reproducible;

que la solución no introduzca una abstracción arquitectónica innecesaria.

Por lo tanto, OQ4 debe resolverse como un problema de identidad y composición, no como una simple operación de zip.

3. Principios ya establecidos

La asociación entre una representación analítica y su PredictionTarget debe basarse en identidad semántica y no exclusivamente en posición.

Una implementación conceptualmente equivalente a:

zip(features, targets)

no constituye por sí misma un mecanismo arquitectónico suficiente de asociación.

La posición puede utilizarse incidentalmente dentro de una implementación si la identidad ya fue garantizada por otro mecanismo, pero el orden de dos colecciones no debe ser la fuente de verdad de la correspondencia.

4. Alcance de este ADR

Este ADR resuelve exclusivamente:

Cómo establecer la asociación técnica entre una representación analítica y su PredictionTarget.

También establece las consecuencias directamente derivadas de esta asociación, especialmente:

identidad;

composición;

responsabilidad de la orquestación;

relación con DatasetBuilder;

relación con Target Generation;

condición necesaria para construir DatasetRow.

No pretende cerrar los demás Open Questions de Target Generation.

5. Fuera de alcance

Este ADR NO decide:

la representación definitiva de PredictionTarget;

la representación técnica de Target Definition;

el modelo definitivo de múltiples tipos de targets;

la política general ante targets indeterminables;

la infraestructura de persistencia;

SQLAlchemy;

Repository;

NBA API;

Machine Learning;

entrenamiento;

predicción;

calibración;

odds;

apuestas.

En particular:

Observation continúa siendo únicamente terminología descriptiva y no constituye un contrato técnico ni una nueva entidad de dominio.

6. Modelo conceptual

El flujo conceptual queda establecido como:

Historical Game
       │
       ├───────────────┐
       ▼               ▼
Feature Engineering   Target Generation
       │               │
       ▼               ▼
TeamGameFeature    PredictionTarget
       │               │
       └───────┬───────┘
               │
               ▼
     Dataset Generation
      Orchestration
               │
               ▼
          DatasetRow

El punto de convergencia pertenece a la orquestación de Dataset Generation.

7. Identidad de la asociación

La identidad seleccionada para una observación analítica de equipo dentro de un partido es:

(game_id, team_id)

Por ejemplo:

(game_id=1001, team_id=10)
(game_id=1001, team_id=20)

representan dos observaciones diferentes dentro del mismo partido.

Esta identidad utiliza los campos primitivos existentes:

game_id: str
team_id: int

No se introduce una nueva abstracción únicamente para representar esta identidad.

8. Requisitos del mecanismo de asociación

El mecanismo seleccionado debe cumplir como mínimo:

8.1 Identidad

Debe permitir determinar a qué observación pertenece un feature y a qué observación pertenece un target.

8.2 Correspondencia correcta

Debe impedir que un target perteneciente a una observación sea asociado accidentalmente con otra.

8.3 Determinismo

La misma entrada debe producir la misma asociación.

8.4 Reproducibilidad

La asociación no debe depender de factores accidentales como:

orden incidental;

iteración no determinista;

estado mutable externo.

8.5 1:1

Para el Dataset actual debe poder garantizarse la correspondencia esperada entre:

una representación analítica
        ↕
un prediction target

cuando ambos existen y son válidos.

8.6 Separación de responsabilidades

La solución no debe convertir a DatasetBuilder en un generador de targets.

8.7 No introducir ML

La asociación debe permanecer independiente del entrenamiento y de cualquier modelo predictivo.

9. Alternativas consideradas

Alternativa A — Asociación por posición

Conceptualmente:

for feature, target in zip(features, targets):
    ...

Evaluación

RECHAZADA como fuente de verdad arquitectónica.

La posición no representa identidad. Una colección incompleta o reordenada puede producir asociaciones incorrectas. Puede existir como detalle incidental de una implementación únicamente cuando una garantía de identidad independiente ya haya sido establecida.

Alternativa B — Asociación mediante identidad estructural existente

En esta alternativa, la representación analítica y la información necesaria para identificar el target utilizan la identidad estructural:

Feature
  ├── game_id
  └── team_id

Target association
  ├── game_id
  └── team_id

La orquestación utiliza esa identidad para establecer la correspondencia.

Evaluación

SELECCIONADA.

Ventajas relevantes:

no requiere una nueva entidad;

preserva la separación de responsabilidades;

hace explícita la correspondencia;

permite validar targets faltantes o duplicados;

mantiene la solución simple;

es compatible con el TeamGameFeature existente.

La decisión no implica que Target Generation deba transportar identidad dentro de su resultado actual. La identidad permanece como responsabilidad de la coordinación de Dataset Generation.

Alternativa C — Value Object de identidad

Podría definirse una representación explícita como:

ObservationIdentity
    game_id
    team_id

Evaluación

RECHAZADA para OQ4.

La identidad estructural existente es suficiente para la decisión actual y no existe evidencia arquitectónica que justifique introducir otra abstracción.

Alternativa D — Entidad o componente intermedio de asociación

Podría introducirse una entidad formal como:

Observation
    ├── Feature
    └── PredictionTarget

o un componente independiente de ensamblado.

Evaluación

RECHAZADA para OQ4.

Introduciría complejidad y una nueva abstracción cuya única finalidad sería resolver el ensamblado. La orquestación de Dataset Generation ya posee la responsabilidad conceptual de coordinar las partes necesarias.

El término Observation puede seguir utilizándose de forma descriptiva, pero no se convierte en entidad ni modelo técnico.

10. Decisión

OQ4 queda formalmente resuelto de la siguiente manera:

La asociación entre una representación analítica y su PredictionTarget utilizará la identidad estructural existente (game_id, team_id).

No se introduce un Identity Value Object.

No se introduce una entidad Observation.

No se utiliza la posición de colecciones como fuente de verdad de la asociación.

11. Contrato de identidad

La identidad seleccionada está compuesta por:

game_id: str
team_id: int

y se representa conceptualmente como:

(game_id, team_id)

La decisión utiliza los campos ya existentes en el dominio actual.

No se crea un nuevo tipo únicamente para encapsularlos.

La unicidad y las validaciones concretas de entradas duplicadas o ambiguas son responsabilidades de la especificación de Dataset Generation y permanecen como trabajo posterior cuando corresponda.

12. Responsabilidad de Dataset Generation Orchestration

La orquestación de Dataset Generation es responsable de coordinar la correspondencia.

Esto significa que debe preservar y utilizar:

(game_id, team_id)

para garantizar que:

TeamGameFeature
       ↕
PredictionTarget

pertenecen a la misma observación semántica.

La orquestación no genera el target.

Tampoco se introduce un componente independiente denominado Dataset Row Assembly.

El ensamblaje es una responsabilidad interna de la orquestación de Dataset Generation.

13. Responsabilidad de Target Generation

Target Generation permanece identity-free bajo esta decisión.

Su contrato actual no cambia:

generate_win_loss_target(
    team_points: int | None,
    opponent_points: int | None
) -> int

Target Generation es responsable de determinar el target a partir de la información histórica correspondiente.

No es responsable de:

construir Dataset;

construir DatasetRow;

ejecutar DatasetBuilder;

coordinar múltiples representaciones;

realizar Machine Learning;

gestionar la asociación entre colecciones de features y targets.

OQ4 no modifica el contrato de Target Generation.

14. Responsabilidad de DatasetBuilder

DatasetBuilder permanece target-unaware.

No debe:

calcular ganador
comparar puntos
interpretar resultados
buscar resultados
generar labels
derivar prediction targets

Su contrato actual no se modifica como consecuencia directa de OQ4.

El hecho de que DatasetRow requiera:

feature + target

no autoriza a DatasetBuilder a generar el target.

La forma concreta en que DatasetBuilder participará en la construcción final deberá definirse en una especificación posterior derivada de esta decisión.

15. DatasetRow

El contrato actual de DatasetRow requiere:

feature
target

Por lo tanto, una instancia válida de DatasetRow solamente puede construirse cuando:

existe el TeamGameFeature;

existe un target válido;

ambos han sido asociados mediante (game_id, team_id).

No se debe asumir una instancia parcial como:

DatasetRow(feature)

si dicha instancia no es válida bajo el contrato actual.

Tampoco se modifica DatasetRow como consecuencia directa de OQ4.

16. Condición de construcción y orden conceptual

OQ4 establece una condición necesaria:

TeamGameFeature
        +
PredictionTarget
        ↓
association by (game_id, team_id)
        ↓
DatasetRow(feature, target)

Por tanto:

Un DatasetRow final no puede construirse válidamente antes de que feature y target estén disponibles y correctamente asociados.

Esta decisión no determina por sí sola el mecanismo concreto de invocación entre Target Generation y DatasetBuilder ni cierra el orden de implementación de todos los pasos de Dataset Generation.

La discrepancia documental existente sobre el orden entre Dataset Row Construction y Target Generation deberá resolverse posteriormente en la actualización de las especificaciones afectadas.

17. Targets indeterminables

OQ4 no introduce una política para targets indeterminables.

Se mantiene la regla:

Undeterminable Target
        ≠
Loss

No deben utilizarse como placeholders de asociación:

None
0
-1
UNKNOWN

La política final de exclusión, aborto o comportamiento configurable permanece abierta.

18. Validaciones

El mecanismo de asociación deberá permitir, como mínimo, detectar conceptualmente:

Target faltante

Existe un feature cuya identidad no tiene target correspondiente.

Target duplicado

Existe más de un target para la misma identidad.

Identidad inconsistente

Los identificadores utilizados para establecer la correspondencia no son compatibles.

Asociación ambigua

No puede determinarse de forma única qué target corresponde al feature.

Target inválido

Target Generation produjo un resultado que no cumple su contrato.

La política específica de respuesta a estas condiciones no queda cerrada por OQ4.

19. Data Leakage Boundary

La asociación no modifica la frontera conceptual de data leakage.

El resultado observado del partido constituye el target y no debe incorporarse como feature predictiva por el hecho de compartir identidad.

Se mantiene:

Analytical Feature
        ↓
DatasetRow.feature


Observed Outcome
        ↓
PredictionTarget

El mecanismo de asociación únicamente establece que ambos pertenecen a la misma observación histórica.

20. Determinismo y reproducibilidad

El mecanismo seleccionado debe ser determinista y reproducible.

Dado el mismo conjunto de entradas, la correspondencia debe producir siempre el mismo resultado.

La identidad (game_id, team_id) constituye la fuente semántica de la asociación; el orden incidental de colecciones no.

La garantía concreta de implementación y sus validaciones se definirá en las especificaciones posteriores.

21. Consecuencias

Positivas

La identidad de asociación queda explícita.

Se evita utilizar posición como fuente de verdad.

Target Generation permanece independiente de Dataset Generation.

DatasetBuilder permanece ajeno a la generación de targets.

No se introduce una abstracción de identidad innecesaria.

Se conserva el diseño actual de DatasetRow.

Se mantiene una frontera clara entre feature y target.

Negativas / trabajo posterior

La orquestación de Dataset Generation debe implementar correctamente la asociación.

Deben definirse validaciones concretas para faltantes, duplicados y ambigüedades.

Debe resolverse la discrepancia documental sobre el orden de construcción.

La especificación actual de DatasetBuilder requiere una revisión para hacer explícito cómo se integra con la asociación ya decidida.

Deben actualizarse los documentos afectados antes de implementar DatasetBuilder.

22. Criterios de decisión

Criterio

Importancia

Corrección de asociación

Crítica

Identidad semántica

Crítica

Separación de responsabilidades

Crítica

Determinismo

Alta

Reproducibilidad

Alta

Simplicidad

Alta

Testabilidad

Alta

Extensibilidad

Media

Nuevas abstracciones

Minimizar

Acoplamiento con infraestructura

Prohibido

La alternativa B es la alternativa más simple que satisface los requisitos actuales sin introducir una abstracción adicional.

23. Preguntas internas analizadas por este ADR

Las siguientes preguntas corresponden al análisis técnico de OQ4 y no deben confundirse con los Open Questions OQ1–OQ5 de Target Generation:

¿Dónde reside la identidad utilizada para asociar feature y target?

¿Es suficiente la identidad estructural existente?

¿Es necesario un Value Object explícito de identidad?

¿Quién coordina técnicamente la asociación?

¿Qué datos necesita Dataset Generation para realizarla?

¿Qué información debe producir Target Generation?

¿DatasetBuilder debe generar o interpretar el target?

¿En qué momento puede construirse válidamente DatasetRow?

¿Qué condición debe cumplirse antes del ensamblaje final?

¿Cómo se preserva el determinismo?

¿La solución requiere modificar el contrato actual de Target Generation?

¿La solución requiere introducir una nueva entidad de dominio?

¿Qué trabajo documental debe realizarse antes de implementar?

Estas preguntas quedan respondidas por la decisión anterior o explícitamente trasladadas a trabajo posterior.

24. Relación con Open Questions de Target Generation

OQ4 es la única cuestión de Target Generation que este ADR cierra.

Permanecen abiertos:

OQ1

OQ2

OQ3

OQ5

Este ADR no debe interpretarse como una resolución implícita de dichas cuestiones.

25. Decisión arquitectónica formal

La decisión completa queda registrada como:

Identity:
    (game_id, team_id)

Identity representation:
    Existing primitive fields

Identity Value Object:
    No

Observation entity:
    No

Association source of truth:
    Semantic identity, not position

Association responsibility:
    Dataset Generation orchestration

Target Generation:
    Identity-free; current contract unchanged

DatasetBuilder:
    Target-unaware; current contract unchanged as direct consequence of OQ4

DatasetRow:
    Constructed only after feature + target are available and associated

Independent Dataset Row Assembly component:
    No

La construcción conceptual queda:

TeamGameFeature
       +
Target Generation result
       ↓
association by (game_id, team_id)
       ↓
DatasetRow(feature, target)
       ↓
Dataset

El mecanismo concreto de invocación y las APIs necesarias para implementar esta secuencia requieren especificación posterior.

26. Documentos afectados posteriormente

La decisión de OQ4 deberá reflejarse, mediante cambios separados y explícitos, en los documentos que resulten afectados.

Como mínimo:

docs/specifications/dataset-builder.md
docs/design/dataset-generation-orchestration.md
docs/architecture/machine-learning.md
docs/specifications/target-generation.md

Estos documentos no han sido modificados por este ADR.

En particular:

dataset-builder.md deberá explicar cómo participa DatasetBuilder sin generar targets.

dataset-generation-orchestration.md deberá incorporar formalmente la asociación por (game_id, team_id).

machine-learning.md deberá resolver la discrepancia documental sobre el orden.

target-generation.md deberá reflejar que OQ4 queda resuelto sin introducir identidad en Target Generation.

Las actualizaciones anteriores pertenecen a trabajos posteriores y deberán revisarse de forma independiente.

27. Consecuencia para la implementación

La implementación de DatasetBuilder continúa suspendida.

El orden correcto del trabajo posterior es:

OQ4 Decision
      ↓
Update affected documentation
      ↓
Implementation Specification
      ↓
Define Dataset Generation orchestration contract
      ↓
Define DatasetBuilder contract compatible with OQ4
      ↓
Implementation
      ↓
Tests

No se debe implementar DatasetBuilder mientras sus contratos continúen presentando la tensión conocida entre:

DatasetBuilder.build(features)

y:

DatasetRow(feature, target)

sin una especificación que defina claramente cómo la orquestación entrega los elementos necesarios.

28. Estado final

OQ4 está resuelto.

La decisión vigente es:

La asociación entre una representación analítica y su PredictionTarget se realizará mediante la identidad estructural existente (game_id, team_id), coordinada por la orquestación de Dataset Generation. Target Generation permanece identity-free, DatasetBuilder permanece target-unaware, y no se introduce un Identity Value Object ni una entidad Observation.

No se realizan cambios de código como consecuencia directa de este ADR.