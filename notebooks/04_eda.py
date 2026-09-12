# ============================================================
# FASE 4 — Análisis Exploratorio de Datos (EDA)
# Dataset: Online Retail II (limpio)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# --- Rutas ---
RUTA_LIMPIO = Path("../datos_limpios")
RUTA_FIGURAS = Path("../salidas/figuras")
RUTA_TABLAS = Path("../salidas/tablas")
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
RUTA_TABLAS.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. CARGA DE DATOS LIMPIOS
# ============================================================
print("="*60)
print("1. CARGANDO DATOS LIMPIOS")
print("="*60)

df = pd.read_csv(RUTA_LIMPIO / "online_retail_completo.csv")
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
df['CustomerID'] = df['CustomerID'].astype('Int64')
df['Country'] = df['Country'].astype('category')

print(f"Filas: {len(df):,}")
print(f"Columnas: {df.shape[1]}")
print(f"Rango temporal: {df['InvoiceDate'].min()} → {df['InvoiceDate'].max()}")

# ============================================================
# 2. MATRIZ DE CORRELACIÓN
# ============================================================
print("\n" + "="*60)
print("2. MATRIZ DE CORRELACIÓN")
print("="*60)

# Correlación entre variables numéricas
vars_numericas = ['Quantity', 'UnitPrice', 'TotalPrice']
correlacion = df[vars_numericas].corr()

print("\nMatriz de correlación (Pearson):")
print(correlacion.round(3))

correlacion.to_csv(RUTA_TABLAS / "08_correlacion.csv")

# Heatmap de correlación
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(correlacion, annot=True, cmap='coolwarm', center=0,
            fmt='.3f', square=True, linewidths=1, ax=ax,
            cbar_kws={'label': 'Coeficiente de correlación'})
ax.set_title('Matriz de correlación entre variables numéricas')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "08_correlacion_heatmap.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 08_correlacion_heatmap.png")

# ============================================================
# 3. ANÁLISIS TEMPORAL
# ============================================================
print("\n" + "="*60)
print("3. ANÁLISIS TEMPORAL")
print("="*60)

# 3.1 Ingresos por mes
ingresos_mes = df.groupby('YearMonth')['TotalPrice'].sum().reset_index()

fig, ax = plt.subplots(figsize=(14, 6))
ax.plot(ingresos_mes['YearMonth'], ingresos_mes['TotalPrice'] / 1000,
        marker='o', color='darkgreen', linewidth=2)
ax.set_title('Ingresos mensuales (2009-2011)')
ax.set_xlabel('Mes')
ax.set_ylabel('Ingresos (miles de £)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "09_ingresos_mensuales.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 09_ingresos_mensuales.png")

# 3.2 Ingresos por día de la semana
ingresos_dia = df.groupby('DayName')['TotalPrice'].sum().reindex(
    ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
)

fig, ax = plt.subplots(figsize=(12, 6))
ingresos_dia.plot(kind='bar', color='steelblue', edgecolor='white', ax=ax)
ax.set_title('Ingresos por día de la semana')
ax.set_xlabel('Día')
ax.set_ylabel('Ingresos (£)')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "10_ingresos_por_dia.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 10_ingresos_por_dia.png")

# 3.3 Ingresos por hora
ingresos_hora = df.groupby('Hour')['TotalPrice'].sum()

fig, ax = plt.subplots(figsize=(12, 6))
ingresos_hora.plot(kind='bar', color='teal', edgecolor='white', ax=ax)
ax.set_title('Ingresos por hora del día')
ax.set_xlabel('Hora')
ax.set_ylabel('Ingresos (£)')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "11_ingresos_por_hora.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 11_ingresos_por_hora.png")

# ============================================================
# 4. ANÁLISIS GEOGRÁFICO
# ============================================================
print("\n" + "="*60)
print("4. ANÁLISIS GEOGRÁFICO")
print("="*60)

# 4.1 Top 10 países por ingresos
top_paises_ingresos = (
    df.groupby('Country')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 países por ingresos:")
print(top_paises_ingresos.round(2))

fig, ax = plt.subplots(figsize=(12, 6))
top_paises_ingresos.plot(kind='barh', color='seagreen', edgecolor='white', ax=ax)
ax.set_title('Top 10 países por ingresos')
ax.set_xlabel('Ingresos (£)')
ax.set_ylabel('País')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "12_top_paises_ingresos.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 12_top_paises_ingresos.png")

# 4.2 Ingresos por país (excluyendo UK)
ingresos_no_uk = (
    df[df['Country'] != 'United Kingdom']
    .groupby('Country')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(12, 6))
ingresos_no_uk.plot(kind='barh', color='coral', edgecolor='white', ax=ax)
ax.set_title('Top 10 países por ingresos (excluyendo Reino Unido)')
ax.set_xlabel('Ingresos (£)')
ax.set_ylabel('País')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "13_top_paises_no_uk.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 13_top_paises_no_uk.png")

# ============================================================
# 5. ANÁLISIS DE PRODUCTOS
# ============================================================
print("\n" + "="*60)
print("5. ANÁLISIS DE PRODUCTOS")
print("="*60)

# 5.1 Top 10 productos por ingresos (no por cantidad)
top_prod_ingresos = (
    df.groupby('Description')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 productos por ingresos:")
print(top_prod_ingresos.round(2))

fig, ax = plt.subplots(figsize=(12, 6))
top_prod_ingresos.plot(kind='barh', color='darkorange', edgecolor='white', ax=ax)
ax.set_title('Top 10 productos por ingresos')
ax.set_xlabel('Ingresos (£)')
ax.set_ylabel('Producto')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "14_top_productos_ingresos.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 14_top_productos_ingresos.png")

# 5.2 Dispersión Quantity vs TotalPrice
sample = df.sample(n=min(5000, len(df)), random_state=42)

fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(sample['Quantity'], sample['TotalPrice'], alpha=0.3, color='purple', s=10)
ax.set_title('Dispersión: Quantity vs TotalPrice (muestra de 5.000)')
ax.set_xlabel('Cantidad')
ax.set_ylabel('Total Price (£)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "15_dispersion_quantity_totalprice.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 15_dispersion_quantity_totalprice.png")

# 5.3 Dispersión UnitPrice vs TotalPrice
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(sample['UnitPrice'], sample['TotalPrice'], alpha=0.3, color='red', s=10)
ax.set_title('Dispersión: UnitPrice vs TotalPrice (muestra de 5.000)')
ax.set_xlabel('Precio unitario (£)')
ax.set_ylabel('Total Price (£)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "16_dispersion_unitprice_totalprice.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 16_dispersion_unitprice_totalprice.png")

# ============================================================
# 6. ANÁLISIS POR SEGMENTOS
# ============================================================
print("\n" + "="*60)
print("6. ANÁLISIS POR SEGMENTOS")
print("="*60)

# 6.1 Ticket medio por país (Top 10)
ticket_medio = (
    df.groupby('Country')['TotalPrice']
    .agg(['mean', 'median', 'count'])
    .sort_values('mean', ascending=False)
    .head(10)
)
print("\nTicket medio por país (Top 10):")
print(ticket_medio.round(2))
ticket_medio.to_csv(RUTA_TABLAS / "09_ticket_medio_pais.csv")

# 6.2 Número de pedidos por cliente (Top 10)
pedidos_cliente = (
    df[df['CustomerID'].notna()]
    .groupby('CustomerID')['InvoiceNo']
    .nunique()
    .sort_values(ascending=False)
    .head(10)
)
print("\nTop 10 clientes por número de pedidos:")
print(pedidos_cliente)

# 6.3 Ingresos por cliente (Top 10)
ingresos_cliente = (
    df[df['CustomerID'].notna()]
    .groupby('CustomerID')['TotalPrice']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("\nTop 10 clientes por ingresos:")
print(ingresos_cliente.round(2))

# ============================================================
# 7. DISTRIBUCIÓN DE INGRESOS POR TRANSACCIÓN
# ============================================================
print("\n" + "="*60)
print("7. DISTRIBUCIÓN DE INGRESOS POR TRANSACCIÓN")
print("="*60)

fig, ax = plt.subplots(figsize=(12, 6))
df[df['TotalPrice'] < df['TotalPrice'].quantile(0.99)]['TotalPrice'].hist(
    bins=50, color='mediumseagreen', edgecolor='white', ax=ax
)
ax.set_title('Distribución de ingresos por transacción (sin outliers)')
ax.set_xlabel('Total Price (£)')
ax.set_ylabel('Frecuencia')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "17_distribucion_ingresos.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 17_distribucion_ingresos.png")

# ============================================================
# 8. RESUMEN FINAL
# ============================================================
print("\n" + "="*60)
print("8. RESUMEN DEL EDA")
print("="*60)

print(f"\nIngresos totales del periodo: £{df['TotalPrice'].sum():,.2f}")
print(f"Ingresos medios por transacción: £{df['TotalPrice'].mean():.2f}")
print(f"Ingresos medianos por transacción: £{df['TotalPrice'].median():.2f}")
print(f"Número de pedidos únicos: {df['InvoiceNo'].nunique():,}")
print(f"Número de clientes únicos: {df['CustomerID'].nunique():,}")
print(f"Número de productos únicos: {df['StockCode'].nunique():,}")
print(f"País con más ingresos: {df.groupby('Country')['TotalPrice'].sum().idxmax()}")
print(f"Mes con más ingresos: {df.groupby('YearMonth')['TotalPrice'].sum().idxmax()}")
print(f"Día con más ingresos: {df.groupby('DayName')['TotalPrice'].sum().idxmax()}")

print("\n✅ FASE 4 COMPLETADA")
print("Revisa las figuras en salidas/figuras/ y las tablas en salidas/tablas/")