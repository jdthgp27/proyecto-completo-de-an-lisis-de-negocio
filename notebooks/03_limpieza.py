# ============================================================
# FASE 3 — Limpieza y preparación de datos
# Dataset: Online Retail II (UCI)
# Entregable: dataset limpio + variables nuevas
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# --- Rutas ---
RUTA_DATOS = Path("../datos/online_retail_II.xlsx")
RUTA_SALIDAS = Path("../salidas")
RUTA_LIMPIO = Path("../datos_limpios")
RUTA_FIGURAS = RUTA_SALIDAS / "figuras"
RUTA_TABLAS = RUTA_SALIDAS / "tablas"
RUTA_LIMPIO.mkdir(parents=True, exist_ok=True)
RUTA_FIGURAS.mkdir(parents=True, exist_ok=True)
RUTA_TABLAS.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. CARGA
# ============================================================
print("="*60)
print("1. CARGANDO DATOS")
print("="*60)

df = pd.concat([
    pd.read_excel(RUTA_DATOS, sheet_name="Year 2009-2010"),
    pd.read_excel(RUTA_DATOS, sheet_name="Year 2010-2011")
], ignore_index=True)

print(f"Filas iniciales: {len(df):,}")
print(f"Columnas iniciales: {df.columns.tolist()}")

# Renombrar columnas para evitar espacios (más cómodo para código)
df = df.rename(columns={
    'Customer ID': 'CustomerID',
    'Invoice': 'InvoiceNo',
    'Price': 'UnitPrice'
})

# ============================================================
# 2. REGISTRO DE PASOS DE LIMPIEZA
# ============================================================
registro_limpieza = []
def registrar(paso, antes, despues, motivo):
    registro_limpieza.append({
        'Paso': paso,
        'Filas antes': antes,
        'Filas después': despues,
        'Filas eliminadas': antes - despues,
        '% eliminado': round((antes - despues) / antes * 100, 2),
        'Motivo': motivo
    })
    print(f"\n{step_icon} {paso}")
    print(f"   Antes: {antes:,} | Después: {despues:,} | Eliminadas: {antes-despues:,}")

step_icon = "🧹"

# ============================================================
# 3. AGREGAR DUPLICADOS (en lugar de eliminarlos)
# ============================================================
print("\n" + "="*60)
print("2. TRATAMIENTO DE DUPLICADOS")
print("="*60)

filas_antes = len(df)

# Agrupar por todas las columnas excepto Quantity y sumar Quantity
# Esto convierte las compras repetidas del mismo producto en una sola fila
df_limpio = df.groupby(
    ['InvoiceNo', 'StockCode', 'Description', 'InvoiceDate',
     'UnitPrice', 'CustomerID', 'Country'],
    dropna=False
).agg({'Quantity': 'sum'}).reset_index()

filas_despues = len(df_limpio)
registrar('Agregación de duplicados (suma de Quantity)', filas_antes, filas_despues,
          'Compras repetidas del mismo producto en la misma factura')

# ============================================================
# 4. ELIMINAR CANCELACIONES
# ============================================================
print("\n" + "="*60)
print("3. ELIMINACIÓN DE CANCELACIONES")
print("="*60)

filas_antes = len(df_limpio)

# Cancelaciones: InvoiceNo empieza por 'C' O Quantity negativa
es_cancelacion = (
    df_limpio['InvoiceNo'].astype(str).str.startswith('C') |
    (df_limpio['Quantity'] < 0)
)
df_limpio = df_limpio[~es_cancelacion].copy()

filas_despues = len(df_limpio)
registrar('Eliminación de cancelaciones', filas_antes, filas_despues,
          'InvoiceNo empieza por "C" o Quantity negativa')

# ============================================================
# 5. ELIMINAR PRECIOS INVÁLIDOS
# ============================================================
print("\n" + "="*60)
print("4. ELIMINACIÓN DE PRECIOS INVÁLIDOS")
print("="*60)

filas_antes = len(df_limpio)

# Precios negativos o cero (excepto casos de cortesía, que no aplican aquí)
df_limpio = df_limpio[df_limpio['UnitPrice'] > 0].copy()

filas_despues = len(df_limpio)
registrar('Eliminación de precios <= 0', filas_antes, filas_despues,
          'Precio negativo o cero')

# ============================================================
# 6. TRATAMIENTO DE DESCRIPTION NULOS
# ============================================================
print("\n" + "="*60)
print("5. TRATAMIENTO DE DESCRIPTION NULOS")
print("="*60)

filas_antes = len(df_limpio)
nulos_desc_antes = df_limpio['Description'].isnull().sum()
print(f"Nulos en Description antes: {nulos_desc_antes:,}")

# Rellenar con el código de producto o eliminarlos (son solo 0.41%)
df_limpio = df_limpio.dropna(subset=['Description'])

filas_despues = len(df_limpio)
registrar('Eliminación de filas con Description nula', filas_antes, filas_despues,
          'Bajo porcentaje (0.41%) y sin valor para el análisis')

# ============================================================
# 7. TRATAMIENTO DE OUTLIERS EXTREMOS
# ============================================================
print("\n" + "="*60)
print("6. TRATAMIENTO DE OUTLIERS EXTREMOS")
print("="*60)

filas_antes = len(df_limpio)

# Estrategia: eliminar outliers por encima del percentil 99.9 de Quantity y UnitPrice
# (conservadores, no eliminamos valores legítimamente altos como pedidos mayoristas)
q99_qty = df_limpio['Quantity'].quantile(0.999)
q99_price = df_limpio['UnitPrice'].quantile(0.999)
print(f"Percentil 99.9 de Quantity: {q99_qty:.0f}")
print(f"Percentil 99.9 de UnitPrice: {q99_price:.2f}")

df_limpio = df_limpio[
    (df_limpio['Quantity'] <= q99_qty) &
    (df_limpio['UnitPrice'] <= q99_price)
].copy()

filas_despues = len(df_limpio)
registrar('Eliminación de outliers extremos (percentil 99.9)', filas_antes, filas_despues,
          'Valores extremos que distorsionan el análisis')

# ============================================================
# 8. CONVERSIÓN DE TIPOS
# ============================================================
print("\n" + "="*60)
print("7. CONVERSIÓN DE TIPOS")
print("="*60)

# CustomerID a Int64 (permitiendo nulos)
df_limpio['CustomerID'] = df_limpio['CustomerID'].astype('Int64')

# InvoiceNo y StockCode a string
df_limpio['InvoiceNo'] = df_limpio['InvoiceNo'].astype(str)
df_limpio['StockCode'] = df_limpio['StockCode'].astype(str)

# Country a categoría (más eficiente)
df_limpio['Country'] = df_limpio['Country'].astype('category')

print("Tipos tras la conversión:")
print(df_limpio.dtypes)

# ============================================================
# 9. CREACIÓN DE NUEVAS VARIABLES
# ============================================================
print("\n" + "="*60)
print("8. CREACIÓN DE VARIABLES DERIVADAS")
print("="*60)

# TotalPrice: valor total de la línea
df_limpio['TotalPrice'] = df_limpio['Quantity'] * df_limpio['UnitPrice']

# Variables temporales
df_limpio['Year'] = df_limpio['InvoiceDate'].dt.year
df_limpio['Month'] = df_limpio['InvoiceDate'].dt.month
df_limpio['Day'] = df_limpio['InvoiceDate'].dt.day
df_limpio['Hour'] = df_limpio['InvoiceDate'].dt.hour
df_limpio['DayOfWeek'] = df_limpio['InvoiceDate'].dt.dayofweek  # 0=lunes
df_limpio['Quarter'] = df_limpio['InvoiceDate'].dt.quarter
df_limpio['YearMonth'] = df_limpio['InvoiceDate'].dt.to_period('M').astype(str)

# Nombre del día de la semana
dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
df_limpio['DayName'] = df_limpio['DayOfWeek'].map(lambda x: dias[x])

# Es fin de semana
df_limpio['IsWeekend'] = df_limpio['DayOfWeek'].isin([5, 6])

print("Variables creadas:")
print(df_limpio[['TotalPrice', 'Year', 'Month', 'Hour', 'DayName', 'YearMonth']].head())

# ============================================================
# 10. SEPARAR DATASET PARA RFM (sin nulos en CustomerID)
# ============================================================
print("\n" + "="*60)
print("9. SEPARACIÓN DE DATASETS")
print("="*60)

# Dataset completo (para análisis general de ventas)
df_completo = df_limpio.copy()
print(f"Dataset COMPLETO: {len(df_completo):,} filas")

# Dataset RFM (solo clientes identificados)
df_rfm = df_limpio.dropna(subset=['CustomerID']).copy()
print(f"Dataset RFM (con CustomerID): {len(df_rfm):,} filas")
print(f"Clientes únicos en RFM: {df_rfm['CustomerID'].nunique():,}")

# ============================================================
# 11. VALIDACIÓN FINAL
# ============================================================
print("\n" + "="*60)
print("10. VALIDACIÓN FINAL")
print("="*60)

print(f"\nDimensiones finales (df_completo): {df_completo.shape}")
print(f"Dimensiones finales (df_rfm): {df_rfm.shape}")

print("\n--- Estadísticas descriptivas finales ---")
print(df_completo[['Quantity', 'UnitPrice', 'TotalPrice']].describe())

print("\n--- Nulos restantes ---")
print(df_completo.isnull().sum())

print("\n--- Rango temporal ---")
print(f"Fecha mínima: {df_completo['InvoiceDate'].min()}")
print(f"Fecha máxima: {df_completo['InvoiceDate'].max()}")

print("\n--- Valores negativos restantes ---")
print(f"Quantity < 0: {(df_completo['Quantity'] < 0).sum()}")
print(f"UnitPrice < 0: {(df_completo['UnitPrice'] < 0).sum()}")
print(f"TotalPrice < 0: {(df_completo['TotalPrice'] < 0).sum()}")

# ============================================================
# 12. VISUALIZACIÓN DE LA LIMPIEZA
# ============================================================
print("\n" + "="*60)
print("11. VISUALIZACIÓN DEL PROCESO DE LIMPIEZA")
print("="*60)

registro_df = pd.DataFrame(registro_limpieza)
print(registro_df.to_string(index=False))
registro_df.to_csv(RUTA_TABLAS / "07_registro_limpieza.csv", index=False)

# Gráfico del proceso
fig, ax = plt.subplots(figsize=(12, 6))
ax.barh(registro_df['Paso'], registro_df['Filas eliminadas'], color='indianred', edgecolor='white')
ax.set_title('Filas eliminadas en cada paso de la limpieza')
ax.set_xlabel('Número de filas eliminadas')
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "07_proceso_limpieza.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 07_proceso_limpieza.png")

# ============================================================
# 13. EXPORTAR DATASETS LIMPIOS
# ============================================================
print("\n" + "="*60)
print("12. EXPORTANDO DATASETS LIMPIOS")
print("="*60)

# Dataset completo
df_completo.to_csv(RUTA_LIMPIO / "online_retail_completo.csv", index=False)
print(f"✅ Guardado: datos_limpios/online_retail_completo.csv ({len(df_completo):,} filas)")

# Dataset RFM
df_rfm.to_csv(RUTA_LIMPIO / "online_retail_rfm.csv", index=False)
print(f"✅ Guardado: datos_limpios/online_retail_rfm.csv ({len(df_rfm):,} filas)")

# También en formato Parquet (más eficiente)
df_completo.to_parquet(RUTA_LIMPIO / "online_retail_completo.parquet", index=False)
df_rfm.to_parquet(RUTA_LIMPIO / "online_retail_rfm.parquet", index=False)
print("✅ Guardados también en formato Parquet (más rápido de cargar)")

print("\n" + "="*60)
print("✅ FASE 3 COMPLETADA")
print("="*60)