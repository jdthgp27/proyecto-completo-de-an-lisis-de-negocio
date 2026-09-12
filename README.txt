📊 Online Retail II — Análisis de Negocio y Segmentación de Clientes
Proyecto de Business Analytics que combina Python, análisis estadístico y segmentación RFM para identificar oportunidades de crecimiento comercial en un dataset real de e-commerce.

https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white
https://img.shields.io/badge/pandas-3.0.5-150458?logo=pandas&logoColor=white
https://img.shields.io/badge/License-MIT-green.svg
https://img.shields.io/badge/Status-Completado-success.svg
https://img.shields.io/badge/Dataset-UCI-blue.svg

📌 Descripción del proyecto
Este proyecto realiza un análisis de negocio completo sobre el dataset Online Retail II del repositorio UCI, que contiene 1.067.371 transacciones de una tienda online británica de regalo y decoración entre diciembre 2009 y diciembre 2011.

El objetivo es responder a una pregunta clave de negocio:

¿Cómo podemos aumentar los ingresos con los clientes que ya tenemos?

Para ello se aplica un pipeline completo de análisis de datos: limpieza, análisis exploratorio (EDA), segmentación RFM y generación de recomendaciones accionables con impacto cuantificado.

🎯 Objetivos
Explorar la estructura y calidad del dataset de transacciones.

Limpiar y preparar los datos (nulos, duplicados, outliers, cancelaciones).

Realizar un EDA para detectar patrones, tendencias y anomalías.

Aplicar técnicas de Business Analytics (segmentación RFM).

Desarrollar recomendaciones accionables justificadas con datos y cuantificadas en impacto económico.

🔍 Principales hallazgos
#	Hallazgo	Impacto
1	El 22% de los clientes (Campeones) genera el 70% de los ingresos	Concentración extrema de ingresos
2	614 clientes "En riesgo" con £1,34M de ingresos históricos	8,15% del total en peligro
3	2.174 clientes "Necesitan atención" aportan solo el 5% de ingresos	Mayor oportunidad de crecimiento
4	Fuerte estacionalidad navideña	Ingresos triplicados en Q4
5	Dominancia geográfica de UK (92%) pero Países Bajos y Australia con ticket medio más alto	Oportunidad de expansión
Impacto potencial combinado: £1.165.418 adicionales en 12 meses (7,1% de crecimiento).

🛠️ Tecnologías utilizadas
Herramienta	Uso
Python 3.13	Lenguaje principal
pandas 3.0.5	Manipulación de datos
numpy	Operaciones numéricas
matplotlib 3.11.2	Visualizaciones base
seaborn 0.13.2	Visualizaciones estadísticas
openpyxl 3.1.5	Lectura de archivos Excel
pyarrow 25.0.1	Exportación a Parquet
Power BI Desktop	Dashboard final (opcional)
📁 Estructura del repositorio
text
online-retail-analysis/
│
├── datos/                              # Dataset original (no versionado)
│   └── online_retail_II.xlsx
│
├── datos_limpios/                      # Datasets procesados (entregable)
│   ├── online_retail_completo.csv
│   ├── online_retail_completo.parquet
│   ├── online_retail_rfm.csv
│   └── online_retail_rfm.parquet
│
├── notebooks/                          # Scripts de Python organizados por fase
│   ├── 01_exploracion.py               # Fase 2: carga y exploración inicial
│   ├── 02_exploracion_avanzada.py      # Fase 2b: duplicados + visualizaciones
│   ├── 03_limpieza.py                  # Fase 3: limpieza y preparación
│   ├── 04_eda.py                       # Fase 4: análisis exploratorio
│   ├── 05_rfm.py                       # Fase 5: segmentación RFM
│   └── 06_recomendaciones.py           # Fase 6: recomendaciones de negocio
│
├── salidas/
│   ├── figuras/                        # 23 gráficos generados
│   └── tablas/                         # 16 tablas de resultados
│
├── docs/
│   ├── informe_final.md                # Informe completo del análisis
│   ├── informe_final.pdf               # Versión PDF del informe
│   └── presentacion.md                 # Esquema de presentación ejecutiva
│
├── LICENSE
└── README.md
🚀 Cómo ejecutar el proyecto
1. Clonar el repositorio
bash
git clone https://github.com/tu-usuario/online-retail-analysis.git
cd online-retail-analysis
2. Crear y activar un entorno virtual
bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
3. Instalar dependencias
bash
pip install -r requirements.txt
4. Descargar el dataset
Descarga el archivo online_retail_II.xlsx desde el UCI Machine Learning Repository y colócalo en la carpeta datos/.

5. Ejecutar los scripts en orden
bash
cd notebooks
python 01_exploracion.py
python 02_exploracion_avanzada.py
python 03_limpieza.py
python 04_eda.py
python 05_rfm.py
python 06_recomendaciones.py
Los resultados (figuras y tablas) se guardarán automáticamente en salidas/.

📊 Estructura del análisis
Fase 1 — Selección del dataset
Evaluación de 3 candidatos (Online Retail II, Olist, E-Commerce Transactions) y justificación de la elección.

Fase 2 — Importación y exploración
1.067.371 transacciones brutas.

22,77% de nulos en CustomerID.

34.335 duplicados identificados como compras repetidas legítimas.

Fase 3 — Limpieza y preparación
5 pasos aplicados:

Agregación de duplicados (suma de Quantity).

Eliminación de cancelaciones (Invoice con 'C' o Quantity < 0).

Eliminación de precios ≤ 0.

Eliminación de Description nulas.

Eliminación de outliers extremos (percentil 99.9).

Resultado: 995.416 transacciones limpias (93,3% del original).

Fase 4 — Análisis Exploratorio de Datos (EDA)
Matriz de correlación: Quantity ↔ TotalPrice = 0,632.

Patrones temporales: picos en oct-nov-dic, caída en enero-febrero.

Análisis geográfico: UK domina con 92% de ingresos.

Análisis de productos: top 10 por ingresos.

Fase 5 — Segmentación RFM
Cálculo de Recencia, Frecuencia y Monetario por cliente.

Puntuaciones R, F, M del 1 al 5.

Clasificación en 6 segmentos: Campeones, Leales, En riesgo, Necesitan atención, Potenciales leales, Otros.

Fase 6 — Recomendaciones de negocio
7 recomendaciones accionables con impacto cuantificado:

Programa VIP para Campeones.

Campaña de reactivación para En riesgo.

Campaña de segunda compra para Necesitan atención.

Upselling para Leales.

Nurturing para Potenciales leales.

Expansión internacional en Países Bajos y Australia.

Planificación estacional adaptada al Q4.

📈 Segmentación RFM — Resultados
Segmento	Clientes	%	Ingresos (£)	% Ingresos	Ingreso Medio (£)
Campeones	1.295	22,13%	11.432.476	69,5%	8.828,17
Leales	689	11,77%	1.780.888	10,8%	2.584,74
En riesgo	614	10,49%	1.339.641	8,1%	2.181,83
Otros	635	10,85%	821.530	5,0%	1.293,75
Necesitan atención	2.174	37,15%	818.837	5,0%	376,65
Potenciales leales	445	7,60%	244.636	1,5%	549,74
💰 Impacto potencial del plan de acción
Acción	Impacto estimado
Reactivación "En riesgo"	+£400.000
Segunda compra "Necesitan atención"	+£409.418
Upselling "Leales"	+£356.000
Nurturing "Potenciales leales"	+£89.000
Total	£1.165.418
Inversión estimada: £50.000
ROI: 23x
Crecimiento proyectado: +7,1%

📸 Capturas del análisis
Segmentación de clientes
https://salidas/figuras/18_distribucion_segmentos.png

Ingresos por segmento
https://salidas/figuras/19_ingresos_por_segmento.png

Matriz de priorización
https://salidas/figuras/23_matriz_priorizacion.png

Serie temporal de ingresos
https://salidas/figuras/09_ingresos_mensuales.png

📄 Documentación
Informe completo: docs/informe_final.md

Presentación ejecutiva: docs/presentacion.md

Dataset limpio (CSV): datos_limpios/online_retail_completo.csv

Segmentación RFM: datos_limpios/online_retail_rfm.csv

🎯 Entregables del proyecto
Este proyecto cubre los tres entregables exigidos por el reto de Business Analytics:

✅ Informe de análisis — con visualizaciones, hallazgos y recomendaciones.

✅ Dataset limpio y preparado — con variables transformadas y derivadas.

✅ Presentación ejecutiva — 12 diapositivas para público no técnico.

🔄 Próximas mejoras
□ Migrar el análisis a Power BI para tener un dashboard interactivo.
□ Implementar clustering K-means complementario al análisis RFM.
□ Análisis de cohortes de retención.
□ Predicción de churn con modelos de Machine Learning.
□ Ampliar el análisis de series temporales con SARIMA o Prophet.
🤝 Contribuciones
Las contribuciones son bienvenidas. Si quieres mejorar el proyecto:

Haz un fork del repositorio.

Crea una rama: git checkout -b feature/nueva-mejora.

Commit: git commit -m "Añade nueva funcionalidad".

Push: git push origin feature/nueva-mejora.

Abre un Pull Request.

📜 Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo LICENSE para más detalles.

👤 Autor
Judit Giravent

LinkedIn: tu-perfil

GitHub: @jdthgp27


🙏 Agradecimientos
UCI Machine Learning Repository por proporcionar el dataset Online Retail II.

pandas, matplotlib y seaborn por las librerías utilizadas.

⭐ Si este proyecto te ha resultado útil, considera darle una estrella en GitHub.

