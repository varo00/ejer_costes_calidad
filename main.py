import pandas as pd
import matplotlib.pyplot as plt
import re

file_path = 'datosClientes.csv'
df_clientes = pd.read_csv(file_path)


# Definir costes asociados a las métricas
costos = {
    'Exactitud': 1000,
    'Completitud': 500,
    'Consistencia': 2000,
    'Validez': 300,
    'Integridad': 1500,
    'Actualización': 1200,
    'Accesibilidad': 1000
}
# Inicializar contadores de errores por tipo
errores = {clave : 0 for clave in costos}

# Exactitud: Identificación de registros con errores en campos esenciales como nombre o dirección
nulos_ambos = df_clientes['Nombre'].isnull() | (df_clientes['Nombre'] == "") | df_clientes['Dirección'].isnull() | (df_clientes['Dirección'] == "")
errores['Exactitud'] += nulos_ambos.sum()

# Completitud: Detección de registros con datos faltantes en campos críticos (nombre, dirección, correo electrónico).
nulos_todos = (df_clientes['Nombre'].isnull() | (df_clientes['Nombre'] == "")) & (df_clientes['Dirección'].isnull() | (df_clientes['Dirección'] == "")) & (df_clientes['Correo Electrónico'].isnull() | (df_clientes['Correo Electrónico'] == ""))
errores['Completitud'] += nulos_todos.sum()

# Consistencia: Verificación de que los números de teléfono cumplen con un formato estándar (+34 #########)
errores['Consistencia'] += df_clientes['Teléfono'].apply(
    lambda x : not bool(re.match(r'^\+34 \d{9}$', str(x)))
).sum()

# Validez: Validar el formato de los correos electrónicos (usuario@dominio.com)
errores['Validez'] += df_clientes['Correo Electrónico'].apply(
    lambda x: not bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', str(x)))
).sum()

# Integridad: Detectar pedidos marcados como inválidos
errores['Integridad'] += df_clientes['Pedido Válido'].str.strip().str.lower().eq('inválido').sum()

# Actualización: Detección de registros que no se han actualizado en más de 15 días
errores['Actualización'] += (df_clientes['Última Actualización (días)'] > 15).sum()

# Accesibilidad: Identificación de registros con tiempos de acceso superiores a 0.3 segundos
errores['Accesibilidad'] += (df_clientes['Tiempo Acceso (seg)'] > 0.3).sum()

impacto_economico = {clave: errores[clave]*costos[clave] for clave in costos}
impacto_economico_total = sum(impacto_economico.values())

# Imprimir los resultados
print("Errores detectados por métrica:")
for c, v in errores.items():
    print(f"- {c}: {v} errores")

print("\nImpacto económico por métrica:")
for c, v in impacto_economico.items():
    print(f"- {c}: {v} €")

print(f'\nImpacto Económico Total: {impacto_economico_total:,}€')

# Visualizacion de los resultados obtenidos
colores = ['#FFB6C1', '#87CEFA', '#90EE90', '#FFD700', '#9370DB', '#00CED1', '#FFA07A']
plt.figure(figsize=(15, 8))
plt.bar(impacto_economico.keys(), impacto_economico.values(), color=colores, edgecolor='black')

plt.title('Impacto Económico por Métrica de Calidad de Datos', fontsize=14, fontweight='bold')

plt.xlabel('Métrica de Calidad', fontsize=12)
plt.ylabel('Impacto Económico (€)', fontsize=12)
plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

#etiquetas sobre las barras
for i, value in enumerate(impacto_economico.values()):
    plt.text(i, value + 20000, f"{value:,} €", ha='center', fontsize=10, fontweight='bold')

# mostrar la gráfica
plt.tight_layout() # para que se vea más compacto
plt.show()