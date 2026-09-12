# INFORME DE ANÁLISIS DE NEGOCIO
## Segmentación de clientes y recomendaciones estratégicas
### Dataset: Online Retail II (UCI Machine Learning Repository)

---

**Autor:** [Tu nombre]
**Fecha:** [Fecha actual]
**Herramientas utilizadas:** Python 3.13, pandas, numpy, matplotlib, seaborn, Power BI Desktop
**Repositorio:** [enlace a tu GitHub]

---

## Índice

1. Resumen ejecutivo
2. Introducción y objetivos
3. Selección del dataset
4. Importación y exploración de datos
5. Limpieza y preparación de datos
6. Análisis Exploratorio de Datos (EDA)
7. Segmentación RFM de clientes
8. Recomendaciones de negocio
9. KPIs de seguimiento
10. Conclusiones
11. Anexos

---

## 1. Resumen ejecutivo

El presente informe analiza el comportamiento de compra de **5.852 clientes** de una tienda online del Reino Unido durante el periodo **diciembre 2009 – diciembre 2011**, a partir del dataset público *Online Retail II* del repositorio UCI.

### Principales hallazgos

- **Ingresos totales del periodo:** £19.138.385,60 (aproximadamente 19,14 millones de libras).
- **Ticket medio por transacción:** £19,23.
- **Concentración extrema de ingresos:** el 22,13% de los clientes (segmento "Campeones") genera el **69,5% de los ingresos**.
- **Fuerte estacionalidad:** los ingresos se triplican en los meses de **octubre, noviembre y diciembre** (campaña navideña).
- **Dominancia geográfica:** el Reino Unido concentra el **91,9%** de las transacciones.
- **Mercados de alto valor:** Países Bajos y Australia tienen el ticket medio más alto (£105,27 y £91,91 respectivamente).
- **Alto valor en riesgo:** el segmento "En riesgo" (614 clientes) representa **£1,34M** de ingresos históricos en peligro de pérdida.

### Recomendaciones clave

1. **Programa VIP** para el segmento Campeones (proteger £11,4M anuales).
2. **Campaña de reactivación urgente** para el segmento En riesgo (recuperar ~£400K).
3. **Campaña de segunda compra** para Necesitan atención (potencial de +£409K).
4. **Upselling** para Leales (potencial de +£356K).
5. **Expansión internacional** en Países Bajos y Australia.

**Impacto potencial combinado:** **£1.165.418 adicionales en 12 meses** (7,1% de crecimiento).

---

## 2. Introducción y objetivos

### 2.1 Contexto

El comercio electrónico de productos de regalo y decoración del hogar es un sector altamente competitivo, con márgenes ajustados y una fuerte dependencia de la fidelización del cliente. En este contexto, comprender el comportamiento de compra y segmentar a los clientes se vuelve crítico para optimizar las estrategias de marketing y maximizar el retorno de la inversión.

### 2.2 Objetivos del análisis

1. **Explorar** la estructura y calidad del dataset de transacciones.
2. **Limpiar y preparar** los datos para el análisis.
3. **Realizar un EDA** para detectar patrones, tendencias y anomalías.
4. **Aplicar técnicas de Business Analytics** (segmentación RFM).
5. **Desarrollar recomendaciones accionables** justificadas con datos.

### 2.3 Metodología

| Fase | Descripción | Herramienta |
|---|---|---|
| 1. Selección | Evaluación de datasets candidatos | Análisis comparativo |
| 2. Exploración | Carga y análisis descriptivo | Python (pandas) |
| 3. Limpieza | Tratamiento de nulos, outliers y duplicados | Python (pandas) |
| 4. EDA | Correlaciones, patrones temporales y geográficos | Python (matplotlib, seaborn) |
| 5. RFM | Segmentación de clientes | Python (pandas) |
| 6. Recomendaciones | Propuestas accionables y KPIs | Análisis de negocio |

---

## 3. Selección del dataset

### 3.1 Candidatos evaluados

Se evaluaron tres datasets candidatos:

| Criterio | **Online Retail II (UCI)** | **Olist Brazilian E-Commerce** | **E-Commerce Transactions** |
|---|---|---|---|
| Origen | UCI Repository | Kaggle | Kaggle |
| Registros | **1.067.371** | ~100.000 | 25.000 |
| Periodo | 2009–2011 | 2016–2018 | 2020–2026 |
| Datos reales | ✅ Sí | ✅ Sí | ❌ Sintéticos |
| Idoneidad para RFM | **Muy alta** | Alta | Media |

### 3.2 Justificación de la elección

Se seleccionó el **Online Retail II** por:

1. **Es un dataset real** de una tienda online registrada en el Reino Unido.
2. **Es el estándar de referencia** para análisis RFM en la industria.
3. **Volumen suficiente** (más de 1M de transacciones) para análisis robusto.
4. **Nivel de suciedad adecuado** (nulos, cancelaciones, outliers) para demostrar habilidades de limpieza.
5. **Bien documentado y reproducible**.

### 3.3 Ficha técnica

| Característica | Valor |
|---|---|
| Nombre | Online Retail II |
| Fuente | UCI Machine Learning Repository |
| URL | https://archive.ics.uci.edu/dataset/502/online+retail+ii |
| Formato | Excel (.xlsx) |
| Tamaño | 43,5 MB |
| Instancias | 1.067.371 transacciones |
| Periodo | 01/12/2009 – 09/12/2011 |
| Licencia | CC BY 4.0 |

### 3.4 Variables del dataset

| Variable | Tipo | Descripción |
|---|---|---|
| InvoiceNo | Nominal | Número de factura (si empieza por "C", cancelación) |
| StockCode | Nominal | Código del producto |
| Description | Texto | Nombre del producto |
| Quantity | Numérico | Cantidad de unidades |
| InvoiceDate | Fecha/Hora | Fecha y hora de la transacción |
| UnitPrice | Numérico | Precio unitario (£) |
| CustomerID | Nominal | Identificador del cliente |
| Country | Texto | País de residencia |

---

## 4. Importación y exploración de datos

### 4.1 Carga del dataset

El dataset se cargó en Python usando `pandas`, unificando las dos hojas de Excel (`Year 2009-2010` y `Year 2010-2011`) en un único DataFrame.

**Resultado de la carga:**
- **Filas totales:** 1.067.371
- **Columnas:** 8
- **Rango temporal:** 2009-12-01 07:45 a 2011-12-09 12:50
- **Países únicos:** 43
- **Clientes únicos:** 5.942
- **Productos únicos:** 5.305

> **📸 Figura 1:** Captura de la exploración inicial del dataset (dimensiones, tipos de datos, nulos).

### 4.2 Estadísticas descriptivas iniciales

| Estadístico | Quantity | UnitPrice | CustomerID |
|---|---|---|---|
| Media | 9,94 | 4,64 | 15.324,64 |
| Mediana | 3,00 | 2,10 | 15.252,00 |
| Moda | 1 | 1,25 | — |
| Desv. estándar | 172,79 | 123,55 | 1.697,46 |
| Mínimo | -80.995 | -53.594,36 | 12.346,00 |
| Máximo | 80.995 | 38.970,00 | 18.287,00 |

**Interpretación:**
- La **media de Quantity (9,94)** muy superior a la **mediana (3)** indica una distribución **asimétrica a la derecha**.
- Los **valores negativos** en Quantity y UnitPrice corresponden a **cancelaciones y devoluciones**.
- El **CustomerID está codificado como float64**, cuando debería ser entero.

### 4.3 Valores nulos

| Variable | Nulos | Porcentaje |
|---|---|---|
| InvoiceNo | 0 | 0,00% |
| StockCode | 0 | 0,00% |
| Description | 4.382 | 0,41% |
| Quantity | 0 | 0,00% |
| InvoiceDate | 0 | 0,00% |
| UnitPrice | 0 | 0,00% |
| **CustomerID** | **243.007** | **22,77%** |
| Country | 0 | 0,00% |

**Hallazgo clave:** el 22,77% de las transacciones no tienen CustomerID, lo que obliga a **separar el dataset en dos versiones**: una completa (para análisis general) y otra filtrada (para RFM).

### 4.4 Duplicados

Se detectaron **34.335 filas duplicadas** (3,22%). Análisis detallado:

- 15.702 duplicados con CustomerID nulo.
- 15.540 duplicados con CustomerID presente.
- 902 duplicados con Quantity negativa.
- 0 duplicados con UnitPrice negativo.

**Conclusión:** tras revisar ejemplos concretos, la mayoría son **compras repetidas legítimas** del mismo producto en la misma factura, no errores de captura. **Decisión:** agregar (sumar Quantity) en lugar de eliminar.

### 4.5 Distribución geográfica

Top 5 países por número de transacciones:

| País | Transacciones |
|---|---|
| United Kingdom | 981.330 |
| EIRE (Irlanda) | 17.866 |
| Germany | 17.624 |
| France | 14.330 |
| Netherlands | 5.140 |

**Interpretación:** el Reino Unido concentra el **91,9%** de las transacciones. La tienda es principalmente británica.

---

## 5. Limpieza y preparación de datos

### 5.1 Pasos de limpieza aplicados

| # | Paso | Filas antes | Filas después | Eliminadas | % | Motivo |
|---|---|---|---|---|---|---|
| 1 | Agregación de duplicados | 1.067.371 | 1.022.443 | 44.928 | 4,21% | Compras repetidas del mismo producto |
| 2 | Eliminación de cancelaciones | 1.022.443 | 1.000.009 | 22.434 | 2,19% | Invoice 'C' o Quantity negativa |
| 3 | Eliminación de precios ≤ 0 | 1.000.009 | 997.393 | 2.616 | 0,26% | Precio inválido |
| 4 | Eliminación de Description nula | 997.393 | 997.393 | 0 | 0,00% | Ya no había nulos |
| 5 | Eliminación de outliers extremos (P99.9) | 997.393 | **995.416** | 1.977 | 0,20% | Valores extremos |

**Total:** 71.955 filas eliminadas (6,74% del dataset original).

> **📸 Figura 2:** Gráfico de barras mostrando las filas eliminadas en cada paso de la limpieza.

### 5.2 Variables derivadas creadas

| Variable | Descripción |
|---|---|
| TotalPrice | Quantity × UnitPrice |
| Year | Año de la transacción |
| Month | Mes (1–12) |
| Day | Día del mes |
| Hour | Hora del día |
| DayOfWeek | Día de la semana (0 = lunes) |
| DayName | Nombre del día en español |
| Quarter | Trimestre (1–4) |
| YearMonth | Año-Mes (formato YYYY-MM) |
| IsWeekend | Booleano: sábado o domingo |

### 5.3 Conversión de tipos

| Variable | Tipo original | Tipo final |
|---|---|---|
| CustomerID | float64 | Int64 |
| InvoiceNo | object | str |
| StockCode | object | str |
| Country | object | category |

### 5.4 Datasets finales

| Dataset | Filas | Columnas | Uso |
|---|---|---|---|
| `df_completo` | 995.416 | 18 | Análisis general de ventas |
| `df_rfm` | 767.853 | 18 | Segmentación RFM (5.852 clientes) |

### 5.5 Validación final

- ✅ **0 valores negativos** en Quantity, UnitPrice o TotalPrice.
- ✅ **Todos los nulos restantes** (227.563) están únicamente en CustomerID.
- ✅ **Rango temporal** preservado: 2009-12-01 a 2011-12-09.

### 5.6 Estadísticas descriptivas finales

| Estadístico | Quantity | UnitPrice | TotalPrice |
|---|---|---|---|
| Media | 10,04 | 3,44 | 19,22 |
| Mediana | 3,00 | 2,10 | 10,20 |
| Moda | 1 | 1,25 | — |
| Desv. estándar | 24,34 | 4,84 | 51,15 |
| Mínimo | 1 | 0,001 | 0,001 |
| Máximo | 500 | 162,60 | 4.707,36 |

---

## 6. Análisis Exploratorio de Datos (EDA)

### 6.1 Análisis de correlaciones

Matriz de correlación de Pearson entre variables numéricas:

| Par de variables | Coeficiente |
|---|---|
| Quantity ↔ TotalPrice | **0,632** |
| UnitPrice ↔ TotalPrice | 0,125 |
| Quantity ↔ UnitPrice | -0,131 |

> **📸 Figura 3:** Heatmap de correlación entre Quantity, UnitPrice y TotalPrice.

**Interpretación:** el ingreso por transacción depende **más del volumen que del precio**. La correlación negativa débil entre cantidad y precio sugiere que los productos más caros se venden en menores cantidades.

### 6.2 Análisis temporal

#### Ingresos mensuales

> **📸 Figura 4:** Serie temporal de ingresos mensuales (2009–2011).

**Hallazgos:**
- **Pico máximo en noviembre 2010:** ~1,46 M£.
- **Pico secundario en noviembre 2011:** ~1,40 M£.
- **Valles profundos en enero-febrero** de cada año (~500.000 £).
- **Estacionalidad clara:** campaña navideña concentra los mayores ingresos.

#### Ingresos por día de la semana

> **📸 Figura 5:** Ingresos por día de la semana.

| Día | Ingresos (£) |
|---|---|
| Jueves | ~3.900.000 |
| Martes | ~3.700.000 |
| Miércoles | ~3.400.000 |
| Lunes | ~3.300.000 |
| Viernes | ~2.900.000 |
| Domingo | ~1.800.000 |
| **Sábado** | **0 (cerrado)** |

#### Ingresos por hora

> **📸 Figura 6:** Ingresos por hora del día.

- Mayor facturación entre **10:00 y 15:00**.
- **Pico máximo a las 12:00** (~2,75 M£).
- Actividad nula antes de las 6:00 y después de las 20:00.

### 6.3 Análisis geográfico

Top 10 países por ingresos:

| País | Ingresos (£) |
|---|---|
| **United Kingdom** | **16.248.567** |
| EIRE (Irlanda) | 632.305 |
| Netherlands | 532.131 |
| Germany | 425.768 |
| France | 328.482 |
| Australia | 163.146 |
| Spain | 101.860 |
| Switzerland | 100.161 |
| Sweden | 83.162 |
| Belgium | 64.045 |

> **📸 Figura 7:** Top 10 países por ingresos.
> **📸 Figura 8:** Top 10 países excluyendo Reino Unido.

**Ticket medio por país (Top 10):**

| País | Media (£) | Mediana (£) |
|---|---|---|
| **Netherlands** | **105,27** | 69,60 |
| Australia | 91,91 | 35,40 |
| Japan | 70,36 | 55,20 |
| Sweden | 63,43 | 22,50 |
| Denmark | 50,78 | 24,96 |
| Lithuania | 42,56 | 30,00 |
| Hong Kong | 40,84 | 23,40 |
| Thailand | 40,40 | 15,60 |
| Singapore | 40,00 | 30,00 |
| EIRE | 36,97 | 17,70 |

**Conclusión:** UK domina en volumen, pero Países Bajos y Australia tienen el ticket medio más alto.

### 6.4 Análisis de productos

Top 10 productos por ingresos:

| Producto | Ingresos (£) |
|---|---|
| REGENCY CAKESTAND 3 TIER | 344.563 |
| WHITE HANGING HEART T-LIGHT HOLDER | 240.115 |
| PARTY BUNTING | 149.187 |
| JUMBO BAG RED RETROSPOT | 143.066 |
| POSTAGE | 112.154 |
| ASSORTED COLOUR BIRD ORNAMENT | 111.774 |
| PAPER CHAIN KIT 50'S CHRISTMAS | 100.592 |
| CHILLI LIGHTS | 85.489 |
| JUMBO BAG STRAWBERRY | 67.007 |
| HOT WATER BOTTLE TEA AND SYMPATHY | 63.518 |

> **📸 Figura 9:** Top 10 productos por ingresos.

**Hallazgo:** los productos más rentables **no coinciden** con los más vendidos por cantidad. Dominan artículos de decoración y regalo.

### 6.5 Análisis de clientes

**Top 10 clientes por número de pedidos:**

| CustomerID | Nº Pedidos |
|---|---|
| 14911 | 381 |
| 12748 | 330 |
| 17841 | 211 |
| 15311 | 208 |
| 13089 | 203 |

**Top 10 clientes por ingresos:**

| CustomerID | Ingresos (£) |
|---|---|
| 14646 | 507.320 |
| 18102 | 502.933 |
| 14156 | 298.240 |
| 14911 | 284.055 |
| 13694 | 190.862 |

**Conclusión:** alta concentración de ingresos en pocos clientes (patrón B2B).

### 6.6 Resumen del EDA

| Métrica | Valor |
|---|---|
| Ingresos totales | £19.138.385,60 |
| Ingreso medio por transacción | £19,23 |
| Ingreso mediano por transacción | £10,20 |
| Nº de pedidos únicos | 39.631 |
| Nº de clientes únicos | 5.852 |
| Nº de productos únicos | 4.913 |
| País con más ingresos | United Kingdom |
| Mes con más ingresos | Noviembre |
| Día con más ingresos | Jueves |

---

## 7. Segmentación RFM de clientes

### 7.1 Metodología

Se aplicó el análisis RFM a los **5.852 clientes** con identificador único:

- **Recencia (R):** días desde la última compra (fecha de referencia: 10/12/2011).
- **Frecuencia (F):** número de facturas únicas.
- **Monetario (M):** suma total del gasto (£).

Cada métrica se puntuó del **1 al 5** usando cuantiles (5 = mejor), y los clientes se agruparon en **6 segmentos de negocio**.

### 7.2 Estadísticas RFM

| Métrica | Media | Mediana | Mínimo | Máximo |
|---|---|---|---|---|
| Recencia (días) | 201,17 | 96 | 1 | 739 |
| Frecuencia | 6,26 | 3 | 1 | 381 |
| Monetario (£) | 2.808,96 | 880,38 | 2,90 | 507.320,36 |

### 7.3 Distribución de segmentos

> **📸 Figura 10:** Distribución de clientes por segmento.
> **📸 Figura 11:** Ingresos totales por segmento.

| Segmento | Clientes | % | Ingresos (£) | % Ingresos | Ingreso Medio (£) |
|---|---|---|---|---|---|
| **Campeones** | 1.295 | 22,13% | 11.432.476 | **69,5%** | 8.828,17 |
| **Leales** | 689 | 11,77% | 1.780.888 | 10,8% | 2.584,74 |
| **En riesgo** | 614 | 10,49% | 1.339.641 | 8,1% | 2.181,83 |
| **Otros** | 635 | 10,85% | 821.530 | 5,0% | 1.293,75 |
| **Necesitan atención** | 2.174 | 37,15% | 818.837 | 5,0% | 376,65 |
| **Potenciales leales** | 445 | 7,60% | 244.636 | 1,5% | 549,74 |

### 7.4 Heatmap R vs F

> **📸 Figura 12:** Heatmap de ingresos por Recencia y Frecuencia.

**Hallazgo:** la zona de mayor valor (R alto, F alto) acumula **£8.032.700** en ingresos.

### 7.5 Dispersión Recencia vs Monetario

> **📸 Figura 13:** Dispersión de clientes por Recencia y Monetario, coloreados por segmento.

### 7.6 Comparativa % clientes vs % ingresos

> **📸 Figura 14:** Comparativa del porcentaje de clientes vs porcentaje de ingresos por segmento.

### 7.7 Hallazgos clave

**Hallazgo 1: Concentración extrema en Campeones.**
El 22,13% de los clientes (1.295 personas) genera el **69,5% de los ingresos** (£11,43M de £16,44M totales).

**Hallazgo 2: El 37% de los clientes aporta solo el 5%.**
El segmento "Necesitan atención" (2.174 clientes) apenas aporta **£818.837** (5%), con ingreso medio de £376,65.

**Hallazgo 3: Los En riesgo aportan más que los Leales.**
Los 614 clientes "En riesgo" generan **£1,34M**, casi lo mismo que los 689 "Leales" (£1,78M).

**Hallazgo 4: El cliente más valioso genera el 3% de los ingresos.**
El cliente ID 14646 ha gastado **£507.320** (3,09% del total).

---

## 8. Recomendaciones de negocio

### 8.1 Tabla maestra de recomendaciones

| Segmento | Clientes | Ingresos (£) | Acción | Prioridad | Potencial |
|---|---|---|---|---|---|
| **Campeones** | 1.295 | 11.432.476 | Programa VIP | ALTA | Retener £11,4M/año |
| **Leales** | 689 | 1.780.888 | Upselling | MEDIA-ALTA | +£356.000 |
| **En riesgo** | 614 | 1.339.641 | Reactivación urgente | ALTA | +£400.000 |
| **Necesitan atención** | 2.174 | 818.837 | Segunda compra | MEDIA | +£409.418 |
| **Potenciales leales** | 445 | 244.636 | Email nurturing | MEDIA | +£89.000 |
| **Otros** | 635 | 821.530 | Análisis manual | BAJA | Optimización |

> **📸 Figura 15:** Matriz de priorización: clientes vs ingresos por segmento.

### 8.2 Recomendación 1: Programa VIP para Campeones

**Perfil:** 1.295 clientes (22,13%) → £11,43M (69,5% de ingresos).

**Acción:**
- Acceso anticipado a nuevos productos.
- Regalos exclusivos en fechas clave.
- Atención personalizada (gestor de cuenta para TOP 50).
- Envíos gratuitos y devoluciones sin coste.

**Objetivo:** mantener tasa de retención >90%.
**Impacto:** proteger £11,4M anuales.

### 8.3 Recomendación 2: Reactivación urgente para En riesgo

**Perfil:** 614 clientes → £1,34M de ingresos históricos.

**Acción:**
- Email personalizado "Te echamos de menos".
- Descuento del 15% + envío gratuito.
- Plazo limitado de 7 días.

**Objetivo:** recuperar el 30% del segmento.
**Impacto:** +£400.000.

### 8.4 Recomendación 3: Segunda compra para Necesitan atención

**Perfil:** 2.174 clientes (37,15%) → £818.837 (5% de ingresos).

**Acción:**
- Cupón de £10 por primera repetición.
- Recomendaciones personalizadas.
- Contenido de valor (guías, ideas).

**Objetivo:** convertir el 20% en Potenciales leales.
**Impacto:** +£409.418.

### 8.5 Recomendación 4: Upselling para Leales

**Perfil:** 689 clientes → £1,78M. Ingreso medio: £2.585.

**Acción:**
- Cross-selling: packs con productos complementarios.
- Suscripciones mensuales.
- Programas de puntos.

**Objetivo:** aumentar ticket medio un 20%.
**Impacto:** +£356.000.

### 8.6 Recomendación 5: Nurturing para Potenciales leales

**Perfil:** 445 clientes → £244.636.

**Acción:**
- Email nurturing con contenido.
- Incentivos progresivos.
- Programas de recomendación.

**Objetivo:** aumentar frecuencia a 3+ pedidos.
**Impacto:** +£89.000.

### 8.7 Recomendación 6: Expansión internacional

**Hallazgo:** Países Bajos y Australia tienen ticket medio muy superior a la media.

**Acción:** adaptar la estrategia comercial (idioma, logística, pago) para captar clientes en estos mercados.

### 8.8 Recomendación 7: Planificación estacional

**Hallazgo:** ingresos triplicados en oct-nov-dic; caída en enero-febrero.

**Acción:**
- Reforzar stock y logística en Q4.
- Campañas de "vuelta a la rutina" en enero.
- Promociones semanales los jueves.

### 8.9 Impacto potencial combinado

| Acción | Impacto estimado |
|---|---|
| Reactivación En riesgo | +£400.000 |
| Segunda compra Necesitan atención | +£409.418 |
| Upselling Leales | +£356.000 |
| **Total** | **£1.165.418** |

**Inversión estimada:** £50.000.
**ROI:** **23x**.

---

## 9. KPIs de seguimiento

| KPI | Valor Actual | Objetivo | Plazo |
|---|---|---|---|
| Tasa de retención de Campeones | >90% | Mantener >90% | Continuo |
| Tasa de reactivación de En riesgo | 0% | Recuperar 30% | 3 meses |
| Conversión Necesitan atención → Leales | 0% | Convertir 20% | 6 meses |
| Ticket medio global | £19,23 | Aumentar a £22,11 | 6 meses |
| Ingreso medio por cliente | £2.808,96 | Aumentar a £3.200 | 12 meses |
| Nº de pedidos por cliente | 6,26 | Aumentar a 7,5 | 12 meses |
| Tasa de recompra a 90 días | No medido | Superar 25% | 3 meses |

---

## 10. Conclusiones

El análisis del dataset Online Retail II ha permitido identificar **patrones claros de comportamiento** y **oportunidades de negocio cuantificables**. Los principales aprendizajes son:

1. **La concentración de ingresos es extrema:** unos pocos clientes (Campeones) generan la mayoría de los ingresos. Esto implica **riesgo** (dependencia) y **oportunidad** (foco).

2. **El volumen vende más que el precio:** la correlación Quantity ↔ TotalPrice es significativamente mayor que UnitPrice ↔ TotalPrice.

3. **La estacionalidad es determinante:** los ingresos se triplican en el Q4. La planificación logística y de marketing debe adaptarse a este ciclo.

4. **Existen mercados internacionales de alto valor:** aunque UK domina en volumen, Países Bajos y Australia tienen ticket medio más alto.

5. **La segmentación RFM permite acciones precisas:** no todos los clientes merecen la misma inversión. Los recursos deben priorizarse según el valor y el riesgo.

Las **7 recomendaciones propuestas** tienen un **impacto potencial combinado de £1,16M** en 12 meses (7,1% de crecimiento) con una inversión estimada de £50.000 (ROI 23x).

---

## 11. Anexos

### Anexo A: Estructura del repositorio
