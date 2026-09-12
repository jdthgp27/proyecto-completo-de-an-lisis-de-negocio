# ============================================================
# FASE 6 — Recomendaciones de negocio
# Genera informes concretos de acción por segmento
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)

# --- Rutas ---
RUTA_TABLAS = Path("../salidas/tablas")
RUTA_FIGURAS = Path("../salidas/figuras")

# ============================================================
# 1. CARGA DEL ANÁLISIS RFM
# ============================================================
print("="*60)
print("1. CARGANDO DATOS RFM")
print("="*60)

rfm = pd.read_csv(RUTA_TABLAS / "10_rfm_segmentos.csv")
rfm['CustomerID'] = rfm['CustomerID'].astype('Int64')

print(f"Clientes totales: {len(rfm):,}")
print(f"Ingresos totales: £{rfm['Monetary'].sum():,.2f}")

# ============================================================
# 2. CÁLCULO DE OPORTUNIDADES POR SEGMENTO
# ============================================================
print("\n" + "="*60)
print("2. OPORTUNIDADES POR SEGMENTO")
print("="*60)

# Definición de acciones y objetivos por segmento
acciones = {
    'Campeones': {
        'accion': 'Programa VIP: acceso anticipado, regalos exclusivos, atención personalizada',
        'objetivo': 'Mantener tasa de retención >90%',
        'prioridad': 'ALTA',
        'potencial': 'Retener £11,4M anuales'
    },
    'Leales': {
        'accion': 'Campaña de upselling: packs, suscripciones, cross-selling',
        'objetivo': 'Subir ticket medio un 20%',
        'prioridad': 'MEDIA-ALTA',
        'potencial': 'Aumentar £1,78M a ~£2,14M'
    },
    'En riesgo': {
        'accion': 'Reactivación urgente: email personalizado + descuento 15% + envío gratis',
        'objetivo': 'Recuperar el 30% del segmento',
        'prioridad': 'ALTA',
        'potencial': 'Recuperar ~£400K'
    },
    'Necesitan atención': {
        'accion': 'Campaña de segunda compra: incentivo por primera repetición',
        'objetivo': 'Convertir 20% en Potenciales leales',
        'prioridad': 'MEDIA',
        'potencial': 'Añadir ~£160K'
    },
    'Potenciales leales': {
        'accion': 'Email nurturing: contenido de valor + incentivo de recurrencia',
        'objetivo': 'Aumentar frecuencia a 3+ pedidos',
        'prioridad': 'MEDIA',
        'potencial': 'Subir ingreso medio de £550 a £750'
    },
    'Otros': {
        'accion': 'Análisis manual y reclasificación (segmento mixto)',
        'objetivo': 'Clasificar en segmentos estándar',
        'prioridad': 'BAJA',
        'potencial': 'Optimizar targeting'
    }
}

# Tabla de recomendaciones
df_acciones = pd.DataFrame(acciones).T
df_acciones.index.name = 'Segmento'

# Añadir métricas de cada segmento
metricas = rfm.groupby('Segmento').agg(
    N_Clientes=('CustomerID', 'count'),
    Ingresos_Totales=('Monetary', 'sum'),
    Ingreso_Medio=('Monetary', 'mean')
).round(2)

# Unir todo
recomendaciones = metricas.join(df_acciones)
recomendaciones = recomendaciones.sort_values('Ingresos_Totales', ascending=False)

print("\n--- TABLA MAESTRA DE RECOMENDACIONES ---")
print(recomendaciones.to_string())

recomendaciones.to_csv(RUTA_TABLAS / "12_recomendaciones_por_segmento.csv")

# ============================================================
# 3. CÁLCULO DE RIESGO Y OPORTUNIDAD
# ============================================================
print("\n" + "="*60)
print("3. CÁLCULO DE RIESGO Y OPORTUNIDAD")
print("="*60)

# Calcular el valor en riesgo (clientes "En riesgo")
en_riesgo = rfm[rfm['Segmento'] == 'En riesgo']
valor_en_riesgo = en_riesgo['Monetary'].sum()
pct_riesgo = valor_en_riesgo / rfm['Monetary'].sum() * 100

print(f"\n⚠️  VALOR EN RIESGO:")
print(f"   Clientes: {len(en_riesgo):,}")
print(f"   Ingresos históricos: £{valor_en_riesgo:,.2f}")
print(f"   % del total: {pct_riesgo:.2f}%")

# Calcular la oportunidad (clientes "Necesitan atención")
necesitan = rfm[rfm['Segmento'] == 'Necesitan atención']
valor_oportunidad = necesitan['Monetary'].sum()
potencial_crecimiento = valor_oportunidad * 0.5  # estimación conservadora 50%

print(f"\n🚀 OPORTUNIDAD DE CRECIMIENTO:")
print(f"   Clientes: {len(necesitan):,}")
print(f"   Ingresos actuales: £{valor_oportunidad:,.2f}")
print(f"   Potencial estimado (50% mejora): £{potencial_crecimiento:,.2f}")

# ============================================================
# 4. VISUALIZACIÓN: MATRIZ DE PRIORIZACIÓN
# ============================================================
print("\n" + "="*60)
print("4. VISUALIZACIÓN: MATRIZ DE PRIORIZACIÓN")
print("="*60)

fig, ax = plt.subplots(figsize=(12, 8))

# Preparar datos
plot_data = metricas.copy()
plot_data['N_Clientes_pct'] = plot_data['N_Clientes'] / plot_data['N_Clientes'].sum() * 100
plot_data['Ingresos_pct'] = plot_data['Ingresos_Totales'] / plot_data['Ingresos_Totales'].sum() * 100

# Scatter plot
scatter = ax.scatter(
    plot_data['N_Clientes_pct'],
    plot_data['Ingresos_pct'],
    s=plot_data['Ingreso_Medio'] / 50,
    c=plot_data['Ingreso_Medio'],
    cmap='YlOrRd',
    alpha=0.7,
    edgecolors='black',
    linewidth=2
)

# Anotaciones
for seg, row in plot_data.iterrows():
    ax.annotate(seg,
                xy=(row['N_Clientes_pct'], row['Ingresos_pct']),
                xytext=(5, 5), textcoords='offset points',
                fontsize=10, fontweight='bold')

# Líneas de referencia
ax.axhline(y=20, color='gray', linestyle='--', alpha=0.5)
ax.axvline(x=20, color='gray', linestyle='--', alpha=0.5)

ax.set_xlabel('% de clientes', fontsize=12)
ax.set_ylabel('% de ingresos', fontsize=12)
ax.set_title('Matriz de priorización: clientes vs ingresos por segmento', fontsize=13)
plt.colorbar(scatter, label='Ingreso medio por cliente (£)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(RUTA_FIGURAS / "23_matriz_priorizacion.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Guardado: 23_matriz_priorizacion.png")

# ============================================================
# 5. LISTAS ACCIONABLES (clientes objetivo por campaña)
# ============================================================
print("\n" + "="*60)
print("5. LISTAS DE CLIENTES OBJETIVO POR CAMPAÑA")
print("="*60)

# Campaña 1: Reactivación "En riesgo"
campaña_reactivacion = rfm[rfm['Segmento'] == 'En riesgo'][
    ['CustomerID', 'Recency', 'Frequency', 'Monetary']
].sort_values('Monetary', ascending=False)

campaña_reactivacion.to_csv(RUTA_TABLAS / "13_campaña_reactivacion.csv", index=False)
print(f"\n📧 Campaña 1 — Reactivación:")
print(f"   Clientes objetivo: {len(campaña_reactivacion):,}")
print(f"   Ingresos históricos: £{campaña_reactivacion['Monetary'].sum():,.2f}")
print(f"   Guardado: 13_campaña_reactivacion.csv")

# Campaña 2: Upselling "Necesitan atención"
campaña_upselling = rfm[rfm['Segmento'] == 'Necesitan atención'][
    ['CustomerID', 'Recency', 'Frequency', 'Monetary']
].sort_values('Monetary', ascending=False)

campaña_upselling.to_csv(RUTA_TABLAS / "14_campaña_upselling.csv", index=False)
print(f"\n📧 Campaña 2 — Upselling:")
print(f"   Clientes objetivo: {len(campaña_upselling):,}")
print(f"   Ingresos actuales: £{campaña_upselling['Monetary'].sum():,.2f}")
print(f"   Guardado: 14_campaña_upselling.csv")

# Campaña 3: VIP "Campeones"
campaña_vip = rfm[rfm['Segmento'] == 'Campeones'][
    ['CustomerID', 'Recency', 'Frequency', 'Monetary']
].sort_values('Monetary', ascending=False)

campaña_vip.to_csv(RUTA_TABLAS / "15_campaña_vip.csv", index=False)
print(f"\n📧 Campaña 3 — VIP Campeones:")
print(f"   Clientes objetivo: {len(campaña_vip):,}")
print(f"   Ingresos históricos: £{campaña_vip['Monetary'].sum():,.2f}")
print(f"   Guardado: 15_campaña_vip.csv")

# ============================================================
# 6. KPIs DE SEGUIMIENTO
# ============================================================
print("\n" + "="*60)
print("6. KPIs DE SEGUIMIENTO RECOMENDADOS")
print("="*60)

kpis = pd.DataFrame({
    'KPI': [
        'Tasa de retención de Campeones',
        'Tasa de reactivación de En riesgo',
        'Conversión Necesitan atención → Leales',
        'Ticket medio global',
        'Ingreso medio por cliente',
        'Nº de pedidos por cliente',
        'Tasa de recompra a 90 días'
    ],
    'Valor_Actual': [
        '>90%',
        f'{len(en_riesgo)} clientes',
        f'{len(necesitan)} clientes',
        '£19,23',
        '£2.808,96',
        '6,26',
        'No medido'
    ],
    'Objetivo': [
        'Mantener >90%',
        'Recuperar 30%',
        'Convertir 20%',
        'Aumentar 15% a £22,11',
        'Aumentar a £3.200',
        'Aumentar a 7,5',
        'Medir y superar 25%'
    ]
})

print(kpis.to_string(index=False))
kpis.to_csv(RUTA_TABLAS / "16_kpis_seguimiento.csv", index=False)

print("\n✅ FASE 6 COMPLETADA")