# Dataset Builder — Implementation Specification

## Status

Frozen

---

## 1. Objective

El objetivo de esta especificación es traducir el Design RFC congelado
`docs/design/dataset-builder.md` en una especificación técnica precisa
que permita implementar `DatasetBuilder` sin requerir nuevas decisiones
arquitectónicas.

`DatasetBuilder` es el componente de Dataset Generation responsable de
transformar un `Iterable[TeamGameFeature]` en un `Dataset` compuesto
por instancias de `DatasetRow`, de acuerdo con las responsabilidades
congeladas en el RFC correspondiente.

Esta especificación no introduce responsabilidades nuevas, no modifica
las ya definidas, y no resuelve preguntas que el RFC dejó abiertas.

---

## 2. Scope

Esta especificación cubre exclusivamente:

- La definición de la API pública de `DatasetBuilder`.
- El flujo de transformación de `TeamGameFeature` a `DatasetRow` y de
  `DatasetRow` a `Dataset`.
- Los requisitos de comportamiento exigidos por el RFC congelado.
- Los casos límite que deben comportarse de forma definida.
- Las restricciones arquitectónicas ya establecidas.
- El alcance de las pruebas unitarias mínimas requeridas.

Esta especificación **no** cubre:

- Ninguna lógica de generación, cálculo o derivación de prediction
  targets. Esta especificación cubre exclusivamente la etapa de
  Dataset Row Construction dentro de la Dataset Generation Strategy
  definida en `docs/architecture/machine-learning.md`. La derivación
  del prediction target de cada observación corresponde a la etapa
  subsiguiente de Target Generation, definida en esa misma arquitectura
  como parte de Dataset Generation, y queda fuera del alcance de este
  documento.
- Ninguna lógica de validación, exportación, persistencia o
  entrenamiento.

---

## 3. Public API

### Clase

`DatasetBuilder`

Componente sin estado, con una única responsabilidad: transformar un
`Iterable[TeamGameFeature]` en un `Dataset`. La especificación no
impone que `DatasetBuilder` se implemente como clase con instancias
reutilizables ni como función libre expuesta bajo un nombre de clase;
sea cual sea la forma concreta, el componente debe comportarse como
una unidad sin estado mutable entre invocaciones.

### Método

`build`

- **Nombre del método:** `build`
- **Parámetro de entrada:** un `Iterable[TeamGameFeature]`
- **Tipo de retorno:** `Dataset`

### Firma conceptual

```python
build(features: Iterable[TeamGameFeature]) -> Dataset
```

### Tipos de entrada

- `features`: cualquier objeto que cumpla el protocolo `Iterable` de
  `TeamGameFeature`, sin asumir una colección concreta (lista, tupla,
  generador u otro iterable compatible).

### Tipos de salida

- Una instancia de `Dataset`, tal como fue definida en
  `src/sportsquant/datasets/dataset.py`, compuesta por instancias de
  `DatasetRow`, tal como fueron definidas en
  `src/sportsquant/datasets/dataset_row.py`.

---

## 4. Construction Flow

El proceso de construcción debe seguir, paso a paso, el siguiente flujo:

1. **Recepción del iterable de entrada.** `DatasetBuilder` recibe un
   `Iterable[TeamGameFeature]` a través del método `build`.

2. **Recorrido del iterable.** Cada `TeamGameFeature` del iterable se
   procesa exactamente una vez, en el orden en que es producido por el
   iterable.

3. **Transformación de `TeamGameFeature` a `DatasetRow`.** Por cada
   `TeamGameFeature` recibido, se construye una instancia de
   `DatasetRow` que conserva, sin modificación, el estado analítico
   representado por ese `TeamGameFeature`. Esta etapa corresponde
   específicamente a Dataset Row Construction dentro de la Dataset
   Generation Strategy; la asociación del prediction target
   correspondiente a cada observación se resuelve en la etapa
   subsiguiente de Target Generation, fuera del alcance de este
   documento.

4. **Acumulación de `DatasetRow`.** Las instancias de `DatasetRow`
   resultantes se acumulan preservando el orden de aparición del
   `TeamGameFeature` de origen dentro del iterable de entrada.

5. **Ensamblaje del `Dataset`.** Una vez recorrido por completo el
   iterable de entrada, se construye una única instancia de `Dataset`
   a partir de la colección ordenada de `DatasetRow` acumuladas.

6. **Retorno del `Dataset`.** El método `build` retorna la instancia de
   `Dataset` resultante.

Este flujo corresponde exactamente a la etapa de "Dataset Row
Construction" descrita conceptualmente en
`docs/architecture/machine-learning.md`, y no incluye ninguna etapa
adicional de validación, generación de targets o exportación.

---

## 5. Behavioral Requirements

- **Determinismo:** dado el mismo `Iterable[TeamGameFeature]` (mismo
  contenido y mismo orden), `build` debe producir siempre un `Dataset`
  equivalente en contenido y orden.
- **Preservación del orden:** el orden de las instancias de
  `DatasetRow` dentro del `Dataset` resultante debe corresponder
  exactamente al orden en que los `TeamGameFeature` fueron producidos
  por el iterable de entrada.
- **Inmutabilidad:** el `Dataset` retornado debe ser una instancia
  inmutable, de acuerdo con la implementación ya congelada de
  `Dataset`. Cada `DatasetRow` que lo compone debe ser igualmente
  inmutable, de acuerdo con la implementación ya congelada de
  `DatasetRow`.
- **No modificación de `TeamGameFeature`:** `DatasetBuilder` no debe
  mutar, reemplazar campos, ni alterar de ninguna forma las instancias
  de `TeamGameFeature` recibidas como entrada.
- **Construcción de `DatasetRow`:** cada `DatasetRow` construido debe
  corresponder a exactamente un `TeamGameFeature` de entrada, en una
  relación 1:1, sin fusionar, omitir ni duplicar observaciones.
- **Construcción de `Dataset`:** el `Dataset` resultante debe contener
  exactamente una `DatasetRow` por cada `TeamGameFeature` recibido, ni
  más ni menos.

---

## 6. Edge Cases

- **Iterable vacío:** si el `Iterable[TeamGameFeature]` de entrada no
  produce ningún elemento, `build` debe retornar un `Dataset` válido
  cuya colección de observaciones esté vacía.
- **Dataset vacío como resultado:** un `Dataset` vacío es un resultado
  legítimo de `build`.
- **Iterable de cualquier tipo compatible:** `build` debe comportarse
  de forma idéntica con listas, tuplas, generadores u otros iterables.
- **Recorrido único:** no debe asumirse que el iterable admite
  múltiples recorridos.

---

## 7. Architectural Constraints

### Dependencias permitidas

- `TeamGameFeature`.
- `Dataset`.
- `DatasetRow`.
- Biblioteca estándar necesaria para recorrer el iterable y construir
  la colección resultante.

### Dependencias prohibidas

- SQLAlchemy, ORM, Session o Persistence.
- pandas o DataFrames.
- Training Pipeline o Inference Pipeline.
- Machine Learning.
- Repositories o Providers.
- Orquestadores de alto nivel.
- Exportación o serialización.

### Responsabilidades prohibidas

- Validar ausencia de data leakage.
- Validar consistencia estructural, ausencia de duplicados o presencia
  de columnas requeridas.
- Definir estrategias de partición temporal de train/validation/test.
- Exportar, versionar o serializar el `Dataset` resultante.
- Acceder a agregados de dominio, a Persistence o a proveedores de
  datos externos.
- Entrenar, evaluar o realizar inferencia con modelos.
- Implementar la etapa de Target Generation, ni derivar o asociar un
  prediction target a ninguna observación como parte de la propia
  implementación de `DatasetBuilder`. Esta restricción aplica
  exclusivamente a este componente; no debe interpretarse como una
  prohibición sobre la etapa de Target Generation en sí, la cual es
  responsabilidad de una etapa distinta y posterior dentro de la misma
  capa de Dataset Generation.

---

## 8. Files to Create

- `src/sportsquant/datasets/dataset_builder.py`

---

## 9. Files to Modify

No es necesario modificar ningún archivo existente.

---

## 10. Unit Testing Strategy

Archivo:

`tests/datasets/test_dataset_builder.py`

Debe validar:

- Dataset vacío.
- Un elemento.
- Múltiples elementos.
- Preservación del orden.
- Tipo de retorno.
- Inmutabilidad.
- Compatibilidad con distintos iterables.

---

## 11. Acceptance Criteria

La implementación será correcta si:

- Expone `DatasetBuilder.build(...)`.
- Convierte `Iterable[TeamGameFeature]` en `Dataset`.
- Mantiene relación 1:1.
- Preserva el orden.
- No modifica la entrada.
- Produce estructuras inmutables.
- Es determinista.
- No introduce responsabilidades prohibidas.
- Cumple todas las pruebas unitarias.

---

## 12. Implementation Notes

- Esta especificación no define cómo se deriva o asocia el prediction
  target de una observación, ya que esa etapa corresponde a Target
  Generation, la fase subsiguiente de la Dataset Generation Strategy ya
  definida en `docs/architecture/machine-learning.md`, y queda fuera
  del alcance de este documento. Cualquier decisión de implementación
  relacionada con esa etapa deberá resolverse en una especificación
  separada correspondiente a Target Generation, dentro de Dataset
  Generation, y no debe anticiparse ni resolverse durante la
  implementación de `DatasetBuilder`.

- La implementación debe limitarse estrictamente al flujo descrito en
  la sección 4.

- Cualquier ambigüedad deberá resolverse consultando
  `docs/design/dataset-builder.md`.