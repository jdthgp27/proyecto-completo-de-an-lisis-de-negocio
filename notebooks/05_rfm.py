# ============================================================
# FASE 5 — Segmentación RFM
# Dataset: Online Retail II (clientes identificados)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import datetime as dt

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# --- Rutas ---
RUTA_LIMPIO = Path("../datos_limpios")
RUTA_FIGURAS = Path("../salidas/figuras")
RUTA_TABLAS = Path("../salidas/tablas")
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
RUTA_TABLAS.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. CARGA DEL DATASET RFM
# ============================================================
print("="*60)
print("1. CARGANDO DATASET RFM")
print("="*60)

df = pd.read_csv(RUTA_LIMPIO / "online_retail_rfm.csv")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['CustomerID'] = df['CustomerID'].astype('Int64')

print(f"Filas: {len(df):,}")
print(f"Clientes únicos: {df['CustomerID'].nunique():,}")
print(f"Rango temporal: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")

# ============================================================
# 2. CÁLCULO DE RFM POR CLIENTE
# ============================================================
print("\n" + "="*60)
print("2. CÁLCULO DE RFM")
print("="*60)

# Fecha de referencia: un día después de la última transacción
fecha_referencia = df['InvoiceDate'].max() + dt.timedelta(days=1)
print(f"Fecha de referencia para Recencia: {fecha_referencia}")

# Agregación por cliente
rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (fecha_referencia - x.max()).days,  # Recencia
    'InvoiceNo': 'nunique',                                       # Frecuencia
    'TotalPrice': 'sum'                                           # Monetario
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

print(f"\nRFM calculado para {len(rfm):,} clientes")
print("\nPrimeras 5 filas:")
print(rfm.head())

print("\nEstadísticas descriptivas RFM:")
print(rfm[['Recency', 'Frequency', 'Monetary']].describe().round(2))

# ============================================================
# 3. ASIGNACIÓN DE PUNTUACIONES (1-5)
# ============================================================
print("\n" + "="*60)
print("3. ASIGNACIÓN DE PUNTUACIONES")
print("="*60)

# R: menor recencia = mejor → invertimos las etiquetas
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)

# F: mayor frecuencia = mejor
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5,
                         labels=[1, 2, 3, 4, 5]).astype(int)

# M: mayor monetario = mejor
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5]).astype(int)

# Puntuación RFM combinada (3 dígitos)
rfm['RFM_Score'] = rfm['R_Score'].astype(str) + \
                   rfm['F_Score'].astype(str) + \
                   rfm['M_Score'].astype(str)

# Suma de puntuaciones (para clasificación rápida)
rfm['RFM_Total'] = rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']

print("\nDistribución de puntuaciones R:")
print(rfm['R_Score'].value_counts().sort_index())
print("\nDistribución de puntuaciones F:")
print(rfm['F_Score'].value_counts().sort_index())
print("\nDistribución de puntuaciones M:")
print(rfm['M_Score'].value_counts().sort_index())

# ============================================================
# 4. SEGMENTACIÓN DE CLIENTES
# ============================================================
print("\n" + "="*60)
print("4. SEGMENTACIÓN DE CLIENTES")
print("="*60)

def segmentar(row):
    """Asigna un segmento de negocio según las puntuaciones RFM."""
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']

    # Campeones: compran reciente, frecuente y mucho
    if r >= 4 and f >= 4 and m >= 4:
        return 'Campeones'
    # Leales: compran reciente, frecuente
    elif r >= 3 and f >= 4:
        return 'Leales'
    # Potenciales leales: recientes pero no muy frecuentes
    elif r >= 4 and f <= 2:
        return 'Potenciales leales'
    # Nuevos: muy recientes pero poco frecuentes
    elif r == 5 and f == 1:
        return 'Nuevos'
    # En riesgo: no compran reciente pero eran buenos clientes
    elif r <= 2 and f >= 3 and m >= 3:
        return 'En riesgo'
    # Necesitan atención: recencia media-baja, frecuencia y valor medio
    elif r <= 3 and f <= 3 and m <= 3:
        return 'Necesitan atención'
    # Perdidos: no compran desde hace mucho, baja frecuencia y bajo valor
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Perdidos'
    # Otros: clientes que no encajan en las categorías anteriores
    else:
        return 'Otros'

rfm['Segmento'] = rfm.apply(segmentar, axis=1)

# Distribución de segmentos
print("\nDistribución de segmentos:")
segmentos_count = rfm['Segmento'].value_counts()
print(segmentos_count)

print("\nPorcentaje por segmento:")
print((segmentos_count / len(rfm) * 100).round(2))

# Ingresos por segmento
print("\nIngresos totales por segmento:")
ingresos_seg = rfm.groupby('Segmento')['Monetary'].sum().sort_values(ascending=False)
print(ingresos_seg.round(2))

# Ingreso medio por cliente en cada segmento
print("\nIngreso medio por cliente en cada segmento:")
ingreso_medio_seg = rfm.groupby('Segmento')['Monetary'].mean().sort_values(ascending=False)
print(ingreso_medio_seg.round(2))

# Guardar tabla RFM
rfm.to_csv(RUTA_TABLAS / "10_rfm_segmentos.csv", index=False)
print("\n✅ Guardado: 10_rfm_segmentos.csv")

# ============================================================
# 5. VISUALIZACIONES
# ============================================================
print("\n" + "="*60)
print("5. GENERANDO VISUALIZACIONES")
print("="*60)

# --- 5.1 Distribución de clientes por segmento ---
fig, ax = plt.subplots(figsize=(10, 6))
colores = sns.color_palette('viridis', n_colors=len(segmentos_count))
segmentos_count.plot(kind='bar', color=colores, edgecolor='white', ax=ax)
ax.set_title('Distribución de clientes por segmento')
ax.set_xlabel('Segmento')
ax.set_ylabel('Número de clientes')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "18_distribucion_segmentos.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 18_distribucion_segmentos.png")

# --- 5.2 Ingresos por segmento (treemap simplificado con barras) ---
fig, ax = plt.subplots(figsize=(12, 6))
ingresos_seg_sorted = ingresos_seg.sort_values()
colors = sns.color_palette('rocket', n_colors=len(ingresos_seg_sorted))
ingresos_seg_sorted.plot(kind='barh', color=colors, edgecolor='white', ax=ax)
ax.set_title('Ingresos totales por segmento de cliente')
ax.set_xlabel('Ingresos (£)')
ax.set_ylabel('Segmento')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "19_ingresos_por_segmento.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 19_ingresos_por_segmento.png")

# --- 5.3 Heatmap de puntuaciones R vs F ---
pivot_rf = rfm.pivot_table(
    values='Monetary',
    index='R_Score',
    columns='F_Score',
    aggfunc='sum'
)

fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(pivot_rf / 1000, annot=True, fmt='.1f', cmap='YlOrRd',
            cbar_kws={'label': 'Ingresos (miles de £)'}, ax=ax)
ax.set_title('Heatmap: Ingresos por Recencia (R) y Frecuencia (F)')
ax.set_xlabel('F_Score (Frecuencia)')
ax.set_ylabel('R_Score (Recencia)')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "20_heatmap_rf.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 20_heatmap_rf.png")

# --- 5.4 Dispersión Recencia vs Monetario coloreado por segmento ---
fig, ax = plt.subplots(figsize=(12, 7))
colores_seg = {
    'Campeones': 'darkgreen',
    'Leales': 'green',
    'Potenciales leales': 'lightgreen',
    'Nuevos': 'skyblue',
    'Necesitan atención': 'orange',
    'En riesgo': 'red',
    'Perdidos': 'darkred',
    'Otros': 'gray'
}
for seg, color in colores_seg.items():
    sub = rfm[rfm['Segmento'] == seg]
    ax.scatter(sub['Recency'], sub['Monetary'], alpha=0.4, s=15,
               label=seg, color=color)
ax.set_title('Clientes por Recencia y Monetario, coloreados por segmento')
ax.set_xlabel('Recencia (días desde última compra)')
ax.set_ylabel('Monetario (£)')
ax.set_yscale('log')  # escala logarítmica para ver mejor
ax.legend(loc='upper right', fontsize=9)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "21_dispersion_rfm_segmento.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 21_dispersion_rfm_segmento.png")

# --- 5.5 Comparativa: % clientes vs % ingresos por segmento ---
comparativa = pd.DataFrame({
    '% Clientes': (rfm['Segmento'].value_counts() / len(rfm) * 100),
    '% Ingresos': (rfm.groupby('Segmento')['Monetary'].sum() / rfm['Monetary'].sum() * 100)
}).sort_values('% Ingresos', ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
comparativa.plot(kind='bar', color=['steelblue', 'darkorange'], edgecolor='white', ax=ax)
ax.set_title('Comparativa: % de clientes vs % de ingresos por segmento')
ax.set_xlabel('Segmento')
ax.set_ylabel('Porcentaje (%)')
plt.xticks(rotation=45, ha='right')
ax.legend(loc='upper right')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "22_comparativa_clientes_ingresos.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 22_comparativa_clientes_ingresos.png")

# ============================================================
# 6. RESUMEN FINAL
# ============================================================
print("\n" + "="*60)
print("6. RESUMEN FINAL DEL ANÁLISIS RFM")
print("="*60)

print(f"\nTotal de clientes analizados: {len(rfm):,}")
print(f"Ingresos totales generados: £{rfm['Monetary'].sum():,.2f}")
print(f"Ingreso medio por cliente: £{rfm['Monetary'].mean():.2f}")
print(f"Ingreso mediano por cliente: £{rfm['Monetary'].median():.2f}")
print(f"\nCliente con mayor gasto: ID {rfm.loc[rfm['Monetary'].idxmax(), 'CustomerID']} "
      f"(£{rfm['Monetary'].max():,.2f})")
print(f"Cliente más frecuente: ID {rfm.loc[rfm['Frequency'].idxmax(), 'CustomerID']} "
      f"({rfm['Frequency'].max()} pedidos)")

print("\n--- Resumen por segmento ---")
resumen_seg = rfm.groupby('Segmento').agg({
    'CustomerID': 'count',
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['sum', 'mean']
}).round(2)
resumen_seg.columns = ['N_Clientes', 'Recencia_Media', 'Frecuencia_Media',
                        'Ingresos_Totales', 'Ingreso_Medio']
print(resumen_seg)

resumen_seg.to_csv(RUTA_TABLAS / "11_resumen_segmentos.csv")
print("\n✅ Guardado: 11_resumen_segmentos.csv")

print("\n✅ FASE 5 COMPLETADA")