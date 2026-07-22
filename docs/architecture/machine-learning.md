# Arquitectura de Machine Learning

## Status

Propuesto

---

## Propósito

Este documento define la arquitectura de transición entre Feature
Engineering y Machine Learning dentro de SportsQuant-AI.

La arquitectura se organiza en tres capas independientes:

```
Feature Engineering
        │
        ▼
Dataset Generation
        │
        ▼
Machine Learning
```

- **Feature Engineering** produce Analytical Feature Models a partir de
  agregados de dominio.
- **Dataset Generation** transforma Analytical Feature Models en datasets
  reproducibles, listos para entrenamiento.
- **Machine Learning** consume datasets ya generados y validados; nunca
  los produce.

Este documento define el diseño del primer modelo predictivo, la capa de
Dataset Generation, el Training Pipeline, el Inference Pipeline y los
principios arquitectónicos que gobiernan estas capas.

Ningún código de Dataset Generation o de Machine Learning debe
implementarse antes de que este documento haya sido revisado y aprobado.

La arquitectura descrita aquí no depende de ningún Feature Model
concreto. Debe permitir que en el futuro existan múltiples Analytical
Feature Models — por ejemplo `TeamGameFeature`, `PlayerGameFeature`,
`LineupFeature` o `BettingFeature` — sin requerir cambios en este
documento.

---

## Objetivo del Primer Modelo

El primer modelo tiene un objetivo deliberadamente acotado: producir una
estimación de probabilidad calibrada para un resultado observable de un
partido de la NBA, utilizando exclusivamente información disponible antes
del inicio del partido o derivada de datos históricos ya cerrados.

El primer modelo no busca:

- Generar señales de apuesta.
- Calcular valor esperado.
- Determinar tamaño de stake.
- Optimizar retorno financiero.

Esas responsabilidades pertenecen a etapas posteriores, claramente
separadas de la estimación de probabilidad.

El primer modelo busca únicamente:

- Validar el pipeline completo desde Feature Engineering, pasando por
  Dataset Generation, hasta Machine Learning.
- Producir una probabilidad calibrada y auditable.
- Servir como fundación arquitectónica para modelos futuros.

---

## Primer Problema de ML

El primer problema de Machine Learning es un problema de clasificación
binaria supervisada.

Definición del problema:

Dado el estado de un equipo antes de un partido, estimar la probabilidad
de que dicho equipo gane el partido.

Este problema fue elegido porque:

- El target es simple, verificable y no ambiguo.
- Los datos necesarios ya son producidos por la capa de Feature
  Engineering, a través de Analytical Feature Models correspondientes al
  equipo y al partido.
- No requiere reconstrucción de possessions ni play-by-play.
- Permite validar el pipeline completo sin introducir complejidad
  innecesaria.

Problemas más complejos (spread, totals, player props) quedan fuera del
alcance del primer modelo.

---

## Dataset Generation

Dataset Generation es una capa arquitectónica independiente, ubicada
entre Feature Engineering y Machine Learning.

Su responsabilidad exclusiva es transformar Analytical Feature Models en
datasets reproducibles. Machine Learning nunca genera datasets; Machine
Learning únicamente consume datasets ya construidos, validados y
exportados por esta capa.

Dataset Generation es responsable de:

- Construir las filas del dataset a partir de Analytical Feature Models.
- Generar el target de predicción para cada fila.
- Validar la ausencia de data leakage en cada fila generada.
- Validar la consistencia estructural del dataset (nulos, duplicados,
  tipos de datos).
- Exportar datasets reproducibles y versionados.

Dataset Generation no entrena modelos, no realiza inferencia y no
contiene lógica de evaluación de modelos. Esas responsabilidades
pertenecen exclusivamente a la capa de Machine Learning.

### Dataset Specification

El dataset del primer modelo se construye a partir de Analytical Feature
Models enriquecidos, una fila por equipo por partido.

Cada fila del dataset representa:

- Un equipo.
- Un partido específico.
- El estado estadístico de ese equipo antes de la agregación de
  resultado final.

El dataset debe cumplir las siguientes propiedades:

- Una fila por (game_id, team_id).
- Sin filas duplicadas.
- Sin valores nulos en las columnas requeridas por el modelo.
- Reproducible a partir de los Analytical Feature Models originales.
- Versionado, de forma que un dataset generado en una fecha determinada
  pueda ser reconstruido posteriormente.

El dataset no contiene lógica de negocio ni transformación adicional más
allá de la ya definida en Feature Engineering.

### Prediction Target

El target del primer modelo es una variable binaria:

- `1` si el equipo representado por la fila ganó el partido.
- `0` si el equipo representado por la fila perdió el partido.

El target se deriva exclusivamente de los puntos anotados por el equipo y
por su oponente, una vez finalizado el partido.

El target nunca debe estar presente, directa o indirectamente, entre las
features utilizadas para el entrenamiento.

### Allowed Features

Las features permitidas son exclusivamente aquellas que representan el
estado de un equipo antes de que el resultado del partido sea conocido.

Ejemplos de features permitidas:

- Estadísticas históricas agregadas del equipo previas al partido.
- Promedios móviles calculados sobre partidos anteriores.
- Indicadores de local o visitante.
- Porcentajes de tiro históricos, calculados sobre partidos previos.
- Identificadores de equipo y oponente, únicamente como referencia
  categórica, no como fuente de fuga de información.

Toda feature permitida debe poder justificarse como disponible en el
momento de la predicción, antes del inicio del partido, sin importar de
qué Analytical Feature Model concreto provenga.

### Forbidden Features (Data Leakage)

Las siguientes categorías de información están explícitamente prohibidas
como features del primer modelo, por constituir fuga de información
(data leakage), independientemente del Analytical Feature Model del que
provengan:

- Estadísticas del propio partido que se intenta predecir (puntos,
  tiros de campo, asistencias, etc. del partido actual).
- Cualquier estadística derivada del resultado final del partido actual.
- Porcentajes de tiro calculados sobre el partido actual.
- Información posterior al inicio del partido, incluyendo play-by-play,
  possessions o box scores del propio partido.
- Cualquier variable calculada usando datos de partidos futuros respecto
  a la fecha del partido predicho.

Ninguna feature puede incorporar información que no estuviera disponible
en el momento real de la predicción. Esta regla es de cumplimiento
obligatorio y no admite excepciones por conveniencia de implementación.

### Dataset Generation Strategy

La generación del dataset sigue una estrategia secuencial y determinista:

```
Analytical Feature Models
        │
        ▼
Dataset Row Construction
        │
        ▼
Target Generation
        │
        ▼
Leakage Validation
        │
        ▼
Consistency Validation
        │
        ▼
Dataset Export
        │
        ▼
Training Dataset
```

Principios de la estrategia:

- Dataset Generation consume Analytical Feature Models ya producidos por
  Feature Engineering; no accede directamente a agregados de dominio ni
  a fuentes de datos externas.
- Dataset Row Construction ensambla cada fila del dataset a partir de un
  Analytical Feature Model, sin introducir transformación de negocio
  adicional.
- Target Generation deriva el target de predicción de acuerdo con la
  definición establecida en Prediction Target.
- Leakage Validation verifica que ninguna columna prohibida esté
  presente en el dataset final.
- Consistency Validation verifica ausencia de nulos, ausencia de
  duplicados y correspondencia de tipos de datos.
- Dataset Export produce un dataset reproducible y versionado, sin
  contener lógica de negocio adicional.
- La generación del dataset debe ser reproducible: la misma fecha de
  corte y el mismo conjunto de Analytical Feature Models deben producir
  siempre el mismo dataset.

---

## Temporal Train/Validation/Test Split

Dado que los datos son series temporales de partidos, la partición de
datos debe respetar estrictamente el orden cronológico.

Principios obligatorios:

- El conjunto de entrenamiento contiene únicamente partidos anteriores en
  el tiempo al conjunto de validación.
- El conjunto de validación contiene únicamente partidos anteriores en el
  tiempo al conjunto de prueba.
- No se permite mezclar aleatoriamente partidos de distintas fechas entre
  conjuntos (no shuffling temporal).
- La partición se define mediante fechas de corte explícitas, no
  mediante proporciones aleatorias.

Estructura conceptual:

```
Partidos más antiguos
        │
        ▼
   Train Set
        │
        ▼
Fecha de corte 1
        │
        ▼
Validation Set
        │
        ▼
Fecha de corte 2
        │
        ▼
   Test Set
        │
        ▼
Partidos más recientes
```

Esta estrategia previene la fuga temporal de información y garantiza que
la evaluación del modelo refleje su capacidad real de predicción sobre
partidos futuros respecto a los datos de entrenamiento.

---

## Training Pipeline

El Training Pipeline es responsable de transformar un dataset ya
generado y validado por Dataset Generation en un modelo entrenado y
evaluado.

Flujo conceptual:

```
Training Dataset
        │
        ▼
Training Feature Set
        │
        ▼
Model Training
        │
        ▼
Model Evaluation
        │
        ▼
Calibration Check
        │
        ▼
Trained Model
```

Responsabilidades:

- Training Feature Set determina qué columnas del dataset se utilizan
  como entrada del modelo, respetando estrictamente las Allowed
  Features definidas en Dataset Generation.
- Model Training ajusta el modelo únicamente sobre el conjunto de
  entrenamiento.
- Model Evaluation mide desempeño exclusivamente sobre los conjuntos de
  validación y prueba, nunca sobre el conjunto de entrenamiento.
- Calibration Check verifica que las probabilidades producidas por el
  modelo estén calibradas antes de considerar el modelo apto.
- Trained Model representa el resultado final versionado del
  entrenamiento, listo para ser consumido por el Inference Pipeline.

El Training Pipeline no genera datasets, no contiene lógica de acceso a
datos en vivo ni lógica de apuestas.

---

## Inference Pipeline

El Inference Pipeline es responsable de producir predicciones utilizando
un Trained Model ya validado.

Flujo conceptual:

```
Pre-Game Team State
        │
        ▼
Feature Assembly
        │
        ▼
Trained Model
        │
        ▼
Probability Estimate
        │
        ▼
Prediction Output
```

Responsabilidades:

- Feature Assembly construye el vector de features utilizando
  únicamente información disponible antes del partido.
- El Trained Model es cargado como una dependencia externa e inmutable
  respecto al pipeline de inferencia.
- Probability Estimate representa la salida cruda del modelo.
- Prediction Output es el resultado final expuesto a capas superiores
  (por ejemplo, futuras capas de valor esperado o apuestas).

El Inference Pipeline no reentrena el modelo, no genera datasets ni
modifica el Trained Model. Su única responsabilidad es producir
predicciones a partir de un modelo ya congelado.

---

## Architectural Principles

Los siguientes principios son de cumplimiento obligatorio para toda la
arquitectura de Dataset Generation y Machine Learning en SportsQuant-AI.

- Prevención estricta de data leakage en todas las etapas.
- Separación completa entre Feature Engineering, Dataset Generation,
  Training Pipeline e Inference Pipeline.
- Machine Learning nunca genera datasets; únicamente los consume.
- El Training Pipeline y el Inference Pipeline nunca comparten estado
  mutable.
- Los Trained Models son inmutables una vez generados.
- Toda predicción debe ser trazable hasta el dataset y el modelo que la
  produjeron.
- La calibración de probabilidades es un requisito de aprobación, no una
  mejora opcional.
- Ninguna lógica de apuestas, valor esperado o bankroll depende
  directamente del Training Pipeline ni del Inference Pipeline; dependen
  únicamente de la Probability Estimate expuesta como salida.
- La arquitectura debe permanecer independiente de un proveedor de datos
  específico, de una liga deportiva específica y de cualquier Analytical
  Feature Model concreto.

---

## Future Evolution

La evolución futura de esta arquitectura sigue el siguiente roadmap:

```
Machine Learning Architecture
        │
        ▼
Dataset Generation
        │
        ▼
Baseline Model
        │
        ▼
Model Evaluation
        │
        ▼
Probability Calibration
        │
        ▼
Inference Pipeline
        │
        ▼
Expected Value
        │
        ▼
Kelly Criterion
        │
        ▼
Backtesting
        │
        ▼
Production Deployment
```

- **Machine Learning Architecture** — este documento, que congela el
  diseño de transición entre Feature Engineering y Machine Learning.
- **Dataset Generation** — implementación de la capa responsable de
  construir, validar y exportar datasets reproducibles a partir de
  Analytical Feature Models.
- **Baseline Model** — implementación del primer modelo de clasificación
  binaria descrito en este documento, utilizado como referencia mínima
  de desempeño.
- **Model Evaluation** — definición y aplicación de métricas de
  desempeño sobre los conjuntos de validación y prueba.
- **Probability Calibration** — validación y ajuste de la calibración de
  las probabilidades producidas por el modelo.
- **Inference Pipeline** — implementación del pipeline de inferencia
  descrito en este documento, para producir predicciones sobre partidos
  futuros.
- **Expected Value** — capa que combina Probability Estimate con cuotas
  de mercado, ubicada estrictamente fuera del Training e Inference
  Pipeline.
- **Kelly Criterion** — capa de decisión financiera dependiente de la
  capa de Expected Value, nunca del modelo directamente.
- **Backtesting** — validación histórica de las decisiones producidas
  por las capas anteriores, respetando la misma disciplina de partición
  temporal definida en este documento.
- **Production Deployment** — despliegue del sistema completo en un
  entorno productivo, una vez que todas las capas anteriores han sido
  validadas y aprobadas.

Cada etapa futura debe documentarse de la misma manera antes de iniciar
su implementación.