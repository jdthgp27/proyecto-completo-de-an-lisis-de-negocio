# ============================================================
# FASE 2 (ampliada) — Análisis de duplicados y EDA inicial
# Dataset: Online Retail II (UCI)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# --- Configuración de rutas ---
RUTA_DATOS = Path("../datos/online_retail_II.xlsx")
RUTA_FIGURAS = Path("../salidas/figuras")
RUTA_TABLAS = Path("../salidas/tablas")
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
RUTA_TABLAS.mkdir(parents=True, exist_ok=True)

# --- Carga ---
print("Cargando datos...")
df = pd.concat([
    pd.read_excel(RUTA_DATOS, sheet_name="Year 2009-2010"),
    pd.read_excel(RUTA_DATOS, sheet_name="Year 2010-2011")
], ignore_index=True)

print(f"Total de filas originales: {len(df):,}")

# ============================================================
# 1. ANÁLISIS DE DUPLICADOS
# ============================================================
print("\n" + "="*60)
print("1. ANÁLISIS DE DUPLICADOS")
print("="*60)

# 1.1 Duplicados exactos (todas las columnas)
duplicados_exactos = df.duplicated().sum()
print(f"\nDuplicados exactos (todas las columnas): {duplicados_exactos:,}")

# 1.2 Duplicados sin considerar Customer ID (por si el nulo hace que se repitan)
cols_sin_customer = [c for c in df.columns if c != 'Customer ID']
duplicados_sin_customer = df.duplicated(subset=cols_sin_customer).sum()
print(f"Duplicados sin considerar 'Customer ID': {duplicados_sin_customer:,}")

# 1.3 Ver algunos ejemplos de duplicados
print("\n--- EJEMPLOS DE FILAS DUPLICADAS (primeras 5) ---")
mask_dup = df.duplicated(keep=False)
ejemplos = df[mask_dup].sort_values(by=list(df.columns)).head(10)
print(ejemplos.to_string())

# 1.4 ¿Los duplicados tienen Customer ID o son nulos?
duplicados_df = df[df.duplicated(keep=False)]
nulos_en_dup = duplicados_df['Customer ID'].isnull().sum()
print(f"\nDuplicados con Customer ID nulo: {nulos_en_dup:,}")
print(f"Duplicados con Customer ID presente: {len(duplicados_df) - nulos_en_dup:,}")

# 1.5 ¿Los duplicados tienen Quantity o Price negativos?
neg_qty_dup = (duplicados_df['Quantity'] < 0).sum()
neg_price_dup = (duplicados_df['Price'] < 0).sum()
print(f"Duplicados con Quantity negativa: {neg_qty_dup:,}")
print(f"Duplicados con Price negativo: {neg_price_dup:,}")

# 1.6 Guardar ejemplo de duplicados
ejemplos.to_csv(RUTA_TABLAS / "05_ejemplos_duplicados.csv", index=False)

# ============================================================
# 2. VISUALIZACIONES EXPLORATORIAS
# ============================================================
print("\n" + "="*60)
print("2. GENERANDO VISUALIZACIONES")
print("="*60)

# --- 2.1 Histograma de Quantity ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Quantity (filtrado a valores razonables para visualización)
q_filtrado = df[(df['Quantity'] > 0) & (df['Quantity'] < df['Quantity'].quantile(0.99))]
axes[0].hist(q_filtrado['Quantity'], bins=50, color='steelblue', edgecolor='white')
axes[0].set_title('Distribución de Quantity (sin outliers, > 0)')
axes[0].set_xlabel('Cantidad')
axes[0].set_ylabel('Frecuencia')

# Price (filtrado)
p_filtrado = df[(df['Price'] > 0) & (df['Price'] < df['Price'].quantile(0.99))]
axes[1].hist(p_filtrado['Price'], bins=50, color='coral', edgecolor='white')
axes[1].set_title('Distribución de Price (sin outliers, > 0)')
axes[1].set_xlabel('Precio (£)')
axes[1].set_ylabel('Frecuencia')

plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "01_histogramas_quantity_price.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 01_histogramas_quantity_price.png")

# --- 2.2 Boxplots de Quantity y Price ---
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].boxplot(df['Quantity'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='steelblue', alpha=0.7))
axes[0].set_title('Boxplot de Quantity')
axes[0].set_ylabel('Cantidad')
axes[0].grid(True, alpha=0.3)

axes[1].boxplot(df['Price'], vert=True, patch_artist=True,
                boxprops=dict(facecolor='coral', alpha=0.7))
axes[1].set_title('Boxplot de Price')
axes[1].set_ylabel('Precio (£)')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "02_boxplots_quantity_price.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 02_boxplots_quantity_price.png")

# --- 2.3 Top 10 países por número de transacciones ---
fig, ax = plt.subplots(figsize=(12, 6))
top_paises = df['Country'].value_counts().head(10)
top_paises.plot(kind='barh', color='seagreen', edgecolor='white', ax=ax)
ax.set_title('Top 10 países por número de transacciones')
ax.set_xlabel('Número de transacciones')
ax.set_ylabel('País')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "03_top_paises.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 03_top_paises.png")

# --- 2.4 Top 10 productos más vendidos (por cantidad total) ---
fig, ax = plt.subplots(figsize=(12, 6))
top_productos = (
    df[df['Quantity'] > 0]
    .groupby('Description')['Quantity']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
top_productos.plot(kind='barh', color='darkorange', edgecolor='white', ax=ax)
ax.set_title('Top 10 productos más vendidos (por cantidad total)')
ax.set_xlabel('Cantidad total vendida')
ax.set_ylabel('Producto')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "04_top_productos.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 04_top_productos.png")

# --- 2.5 Evolución mensual de transacciones ---
df['YearMonth'] = df['InvoiceDate'].dt.to_period('M').astype(str)
evolucion = df.groupby('YearMonth').size()

fig, ax = plt.subplots(figsize=(14, 6))
evolucion.plot(kind='line', marker='o', color='purple', ax=ax)
ax.set_title('Evolución mensual del número de transacciones (2009–2011)')
ax.set_xlabel('Mes')
ax.set_ylabel('Número de transacciones')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "05_evolucion_mensual.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 05_evolucion_mensual.png")

# --- 2.6 Distribución de transacciones por hora del día ---
df['Hour'] = df['InvoiceDate'].dt.hour
fig, ax = plt.subplots(figsize=(12, 5))
df['Hour'].value_counts().sort_index().plot(kind='bar', color='teal', edgecolor='white', ax=ax)
ax.set_title('Distribución de transacciones por hora del día')
ax.set_xlabel('Hora')
ax.set_ylabel('Número de transacciones')
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "06_transacciones_por_hora.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 06_transacciones_por_hora.png")

# ============================================================
# 3. ANÁLISIS DE VALORES NEGATIVOS Y OUTLIERS
# ============================================================
print("\n" + "="*60)
print("3. VALORES NEGATIVOS Y OUTLIERS")
print("="*60)

# 3.1 Transacciones con Quantity negativa (cancelaciones)
neg_qty = df[df['Quantity'] < 0]
print(f"\nTransacciones con Quantity < 0: {len(neg_qty):,} ({len(neg_qty)/len(df)*100:.2f}%)")

# 3.2 Transacciones con Invoice que empieza por 'C' (cancelaciones oficiales)
cancelaciones = df[df['Invoice'].astype(str).str.startswith('C')]
print(f"Transacciones con Invoice empezando por 'C': {len(cancelaciones):,}")

# 3.3 Outliers por IQR en Quantity
Q1 = df['Quantity'].quantile(0.25)
Q3 = df['Quantity'].quantile(0.75)
IQR = Q3 - Q1
lim_inf = Q1 - 1.5 * IQR
lim_sup = Q3 + 1.5 * IQR
outliers_qty = df[(df['Quantity'] < lim_inf) | (df['Quantity'] > lim_sup)]
print(f"\nOutliers en Quantity (IQR): {len(outliers_qty):,} ({len(outliers_qty)/len(df)*100:.2f}%)")
print(f"  Límite inferior: {lim_inf:.2f}, Límite superior: {lim_sup:.2f}")

# 3.4 Outliers por IQR en Price
Q1p = df['Price'].quantile(0.25)
Q3p = df['Price'].quantile(0.75)
IQRp = Q3p - Q1p
lim_infp = Q1p - 1.5 * IQRp
lim_supp = Q3p + 1.5 * IQRp
outliers_price = df[(df['Price'] < lim_infp) | (df['Price'] > lim_supp)]
print(f"\nOutliers en Price (IQR): {len(outliers_price):,} ({len(outliers_price)/len(df)*100:.2f}%)")
print(f"  Límite inferior: {lim_infp:.2f}, Límite superior: {lim_supp:.2f}")

# ============================================================
# 4. GUARDAR RESULTADOS
# ============================================================
print("\n" + "="*60)
print("4. GUARDANDO RESULTADOS")
print("="*60)

resumen = pd.DataFrame({
    'Métrica': [
        'Filas totales', 'Duplicados exactos', 'Duplicados sin Customer ID',
        'Nulos en Customer ID', 'Nulos en Description',
        'Quantity < 0', 'Invoice empieza por C',
        'Outliers Quantity (IQR)', 'Outliers Price (IQR)',
        'Clientes únicos', 'Productos únicos', 'Países únicos'
    ],
    'Valor': [
        len(df), duplicados_exactos, duplicados_sin_customer,
        df['Customer ID'].isnull().sum(), df['Description'].isnull().sum(),
        len(neg_qty), len(cancelaciones),
        len(outliers_qty), len(outliers_price),
        df['Customer ID'].nunique(), df['StockCode'].nunique(), df['Country'].nunique()
    ]
})
resumen.to_csv(RUTA_TABLAS / "06_resumen_exploracion.csv", index=False)
print(resumen.to_string(index=False))

print("\n✅ Análisis completado. Revisa salidas/figuras/ y salidas/tablas/")