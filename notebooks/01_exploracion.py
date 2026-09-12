# ============================================================
# FASE 2 — Importación y exploración inicial
# Dataset: Online Retail II (UCI)
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# --- Configuración de estilo de gráficos ---
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# --- 1. Carga de datos ---
# El archivo contiene 2 hojas: "Year 2009-2010" y "Year 2010-2011"
ruta = Path("../datos/online_retail_II.xlsx")

print("Cargando hojas del Excel...")
hoja_1 = pd.read_excel(ruta, sheet_name="Year 2009-2010")
hoja_2 = pd.read_excel(ruta, sheet_name="Year 2010-2011")

# Unimos ambas hojas en un único DataFrame
df = pd.concat([hoja_1, hoja_2], ignore_index=True)

# --- 2. Exploración inicial ---
print("\n=== PRIMERAS FILAS ===")
print(df.head())

print("\n=== ÚLTIMAS FILAS ===")
print(df.tail())

print("\n=== DIMENSIONES ===")
print(f"Filas: {df.shape[0]:,}")
print(f"Columnas: {df.shape[1]}")

print("\n=== NOMBRES DE COLUMNAS ===")
print(df.columns.tolist())

print("\n=== TIPOS DE DATOS ===")
print(df.dtypes)

print("\n=== INFORMACIÓN GENERAL ===")
df.info()

print("\n=== ESTADÍSTICAS DESCRIPTIVAS (numéricas) ===")
print(df.describe())

print("\n=== VALORES NULOS POR COLUMNA ===")
print(df.isnull().sum())

print("\n=== PORCENTAJE DE NULOS ===")
print((df.isnull().sum() / len(df) * 100).round(2))

print("\n=== DUPLICADOS ===")
print(f"Filas duplicadas: {df.duplicated().sum():,}")

print("\n=== RANGO DE FECHAS ===")
print(f"Fecha mínima: {df['InvoiceDate'].min()}")
print(f"Fecha máxima: {df['InvoiceDate'].max()}")

print("\n=== PAÍSES ÚNICOS ===")
print(f"Número de países: {df['Country'].nunique()}")
print(df['Country'].value_counts().head(10))

print("\n=== CLIENTES ÚNICOS ===")
print(f"Clientes únicos (sin contar nulos): {df['Customer ID'].nunique():,}")

print("\n=== PRODUCTOS ÚNICOS ===")
print(f"Productos únicos (StockCode): {df['StockCode'].nunique():,}")

# --- 3. Guardar resumen para el informe ---
salida = Path("../salidas/tablas")
salida.mkdir(parents=True, exist_ok=True)

# Estadísticas descriptivas
df.describe().to_csv(salida / "01_estadisticas_descriptivas.csv")

# Nulos
df.isnull().sum().to_csv(salida / "02_valores_nulos.csv")

# Top 10 países
df['Country'].value_counts().head(10).to_csv(salida / "03_top_paises.csv")

# Top 10 productos
df['Description'].value_counts().head(10).to_csv(salida / "04_top_productos.csv")

print("\n✅ Resúmenes exportados en salidas/tablas/")