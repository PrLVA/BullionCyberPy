import tkinter as tk
from tkinter import ttk
import requests
import time
import csv
from tkinter import messagebox

# Diccionarios de productos (podrían cargarse desde un archivo JSON en el futuro)
monedas_oro = {
    "Krugerrand": {"peso_gramos": 31.1035, "prima": 0.03},
    "American Eagle": {"peso_gramos": 31.1035, "prima": 0.05},
    "Maple Leaf": {"peso_gramos": 31.1035, "prima": 0.04},
    "Philharmonic": {"peso_gramos": 31.1035, "prima": 0.037},
    "Britannia": {"peso_gramos": 31.1035, "prima": 0.035},
    "Buffalo": {"peso_gramos": 31.1035, "prima": 0.045}
}

monedas_plata = {
    "Silver Eagle": {"peso_gramos": 31.1035, "prima": 0.33},
    "Maple Leaf Plata": {"peso_gramos": 31.1035, "prima": 0.33},
    "Philharmonic Plata": {"peso_gramos": 31.1035, "prima": 0.33},
    "Britannia Plata": {"peso_gramos": 31.1035, "prima": 0.33},
    "Libertad Plata": {"peso_gramos": 31.1035, "prima": 0.33},
    "Panda Plata": {"peso_gramos": 30.0, "prima": 0.39}
}

monedas_oro_viejo = {
    "100 Coronas Austria": {"peso_gramos": 30.49, "prima": 0.10},
    "25 Pesetas España 1877-1885": {"peso_gramos": 7.258, "prima": 0.20},
    "Caciques Venezuela": {"peso_gramos": 1.5, "prima": 3.50},
    "20 Francos Suizos": {"peso_gramos": 5.805, "prima": 0.15},
    "Soberano Británico": {"peso_gramos": 7.322, "prima": 0.20}
}

monedas_oro_coleccion = {
    "Libertad Reverse Proof": {"peso_gramos": 31.1035, "prima": 0.25},
    "Panda 1 oz 2023": {"peso_gramos": 30.0, "prima": 0.30},
    "Soberano Conmemorativo": {"peso_gramos": 7.322, "prima": 0.50},
    "Lince Ibérico 1 oz": {"peso_gramos": 31.1035, "prima": 0.40}
}

lingotes_oro = {
    "Lingote 2g": {"peso_gramos": 2.0, "prima": 0.10},
    "Lingote 10g": {"peso_gramos": 10.0, "prima": 0.06},
    "Lingote 50g": {"peso_gramos": 50.0, "prima": 0.03},
    "Lingote 100g": {"peso_gramos": 100.0, "prima": 0.02},
    "Lingote 1kg": {"peso_gramos": 1000.0, "prima": 0.01}
}

lingotes_plata = {
    "Lingote Plata 1 oz": {"peso_gramos": 31.10, "prima": 0.33},
    "Lingote Plata 100g": {"peso_gramos": 100.0, "prima": 0.15},
    "Lingote Plata 250g": {"peso_gramos": 250.0, "prima": 0.08},
    "Lingote Plata 1kg": {"peso_gramos": 1000.0, "prima": 0.05},
    "Lingote Plata 5kg": {"peso_gramos": 5000.0, "prima": 0.03}
}

# Obtener precio de PAX Gold (oro) en EUR
def obtener_precio_paxg():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=pax-gold&vs_currencies=eur"
    for _ in range(3):  # Reintentar 3 veces
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["pax-gold"]["eur"]
        except Exception as e:
            print(f"Error al obtener PAXG: {e}")
            time.sleep(2)
    messagebox.showwarning("API Error", "No se pudo obtener el precio del oro. Usando valor por defecto.")
    return 2700  # Valor por defecto

# Obtener precio de Kinesis Silver (plata) en EUR
def obtener_precio_plata():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=kinesis-silver&vs_currencies=eur"
    for _ in range(3):  # Reintentar 3 veces
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["kinesis-silver"]["eur"]
        except Exception as e:
            print(f"Error al obtener precio plata: {e}")
            time.sleep(2)
    messagebox.showwarning("API Error", "No se pudo obtener el precio de la plata. Usando valor por defecto.")
    return 30  # Valor por defecto

# Calcular precios de los ítems
def calcular_precios(precio_base, items, tipo):
    precio_por_gramo = precio_base / 31.1035  # Precio por gramo basado en 1 oz troy
    precios = {}
    if tipo in ["oro_viejo", "lingotes_oro", "oro_coleccion"]:
        for item, datos in items.items():
            valor_metal = precio_por_gramo * datos["peso_gramos"]
            precios[item] = round(valor_metal * (1 + datos["prima"]), 2)
    elif tipo in ["plata", "lingotes_plata"]:
        for item, datos in items.items():
            valor_metal = precio_por_gramo * datos["peso_gramos"]
            precios[item] = round(valor_metal * (1 + datos["prima"]), 2)
    else:  # Monedas de 1 oz
        for item, datos in items.items():
            precios[item] = round(precio_base * (1 + datos["prima"]), 2)
    return precios

# Insertar una categoría en la tabla
def insertar_categoria(tree, nombre_categoria, precios, datos_items):
    tree.insert("", "end", values=(f"--- {nombre_categoria} ---", ""), tags=("header",))
    for item, precio in precios.items():
        peso = datos_items[item]["peso_gramos"]
        tree.insert("", "end", values=(f"{item} ({peso}g)", f"{precio} €"))

# Exportar precios a CSV
def exportar_a_csv():
    precios_data = []
    for child in tree.get_children():
        valores = tree.item(child)["values"]
        precios_data.append(valores)
    
    with open(f"precios_{time.strftime('%Y%m%d_%H%M%S')}.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Item", "Precio (EUR)"])
        writer.writerows(precios_data)
    messagebox.showinfo("Éxito", "Precios exportados a CSV.")

# Actualizar la tabla
def actualizar_tabla():
    try:
        precio_oro = obtener_precio_paxg()
        precio_plata = obtener_precio_plata()
        precio_oro_gramo = precio_oro / 31.1035
        precio_plata_gramo = precio_plata / 31.1035
        
        precios_oro = calcular_precios(precio_oro, monedas_oro, "oro")
        precios_plata = calcular_precios(precio_plata, monedas_plata, "plata")
        precios_oro_viejo = calcular_precios(precio_oro, monedas_oro_viejo, "oro_viejo")
        precios_oro_coleccion = calcular_precios(precio_oro, monedas_oro_coleccion, "oro_coleccion")
        precios_lingotes_oro = calcular_precios(precio_oro, lingotes_oro, "lingotes_oro")
        precios_lingotes_plata = calcular_precios(precio_plata, lingotes_plata, "lingotes_plata")
        
        tree.delete(*tree.get_children())  # Limpiar tabla
        
        insertar_categoria(tree, "Monedas de Oro Bullion (1 oz)", precios_oro, monedas_oro)
        insertar_categoria(tree, "Monedas de Plata de Inversión", precios_plata, monedas_plata)
        insertar_categoria(tree, "Monedas de Oro Viejo", precios_oro_viejo, monedas_oro_viejo)
        insertar_categoria(tree, "Monedas de Oro de Colección", precios_oro_coleccion, monedas_oro_coleccion)
        insertar_categoria(tree, "Lingotes de Oro", precios_lingotes_oro, lingotes_oro)
        insertar_categoria(tree, "Lingotes de Plata", precios_lingotes_plata, lingotes_plata)
        
        label_paxg.config(text=f"Precio PAXG (EUR/oz oro): {precio_oro} €")
        label_plata.config(text=f"Precio Plata (EUR/oz): {precio_plata} €")
        label_oro_gramo.config(text=f"Precio oro por gramo: {precio_oro_gramo:.2f} €")
        label_plata_gramo.config(text=f"Precio plata por gramo: {precio_plata_gramo:.2f} €")
        ultima_actualizacion.config(text=f"Última actualización: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        estado.config(text="Estado: Actualización exitosa", fg="green")
    except Exception as e:
        estado.config(text=f"Estado: Error en actualización ({str(e)})", fg="red")
    
    ventana.after(60000, actualizar_tabla)  # Actualizar cada 60 segundos

# Crear ventana principal
ventana = tk.Tk()
ventana.title("Precios de Oro y Plata - La Dobla Bullion")
ventana.geometry("450x800")
ventana.resizable(True, True)  # Ventana redimensionable

# Etiquetas de precios
label_paxg = tk.Label(ventana, text="Precio Oro (EUR/oz oro): Cargando...")
label_paxg.pack(pady=5)
label_plata = tk.Label(ventana, text="Precio Plata (EUR/oz): Cargando...")
label_plata.pack(pady=5)
label_oro_gramo = tk.Label(ventana, text="Precio oro por gramo: Cargando...")
label_oro_gramo.pack(pady=5)
label_plata_gramo = tk.Label(ventana, text="Precio plata por gramo: Cargando...")
label_plata_gramo.pack(pady=5)

# Tabla con barra de desplazamiento
frame_tabla = tk.Frame(ventana)
frame_tabla.pack(pady=20, fill="both", expand=True)
scrollbar = tk.Scrollbar(frame_tabla)
scrollbar.pack(side="right", fill="y")
tree = ttk.Treeview(frame_tabla, columns=("Item", "Precio"), show="headings", yscrollcommand=scrollbar.set)
tree.heading("Item", text="Item")
tree.heading("Precio", text="Precio (EUR)")
tree.column("Item", width=250)
tree.column("Precio", width=150)
tree.tag_configure("header", background="#d3d3d3", font=("Arial", 10, "bold"))
tree.pack(fill="both", expand=True)
scrollbar.config(command=tree.yview)

# Botones
btn_actualizar = tk.Button(ventana, text="Actualizar Ahora", command=actualizar_tabla)
btn_actualizar.pack(pady=5)
btn_exportar = tk.Button(ventana, text="Exportar a CSV", command=exportar_a_csv)
btn_exportar.pack(pady=5)

# Etiquetas de estado y última actualización
ultima_actualizacion = tk.Label(ventana, text="Última actualización: -")
ultima_actualizacion.pack(pady=5)
estado = tk.Label(ventana, text="Estado: Iniciando...", fg="blue")
estado.pack(pady=5)

# Iniciar actualización
actualizar_tabla()

ventana.mainloop()