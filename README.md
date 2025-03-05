# Precios de Oro y Plata - La Dobla Bullion

Esta es una aplicación en Python que muestra los precios en tiempo real de monedas y lingotes de oro y plata . Utiliza la API de CoinGecko para obtener los precios spot del oro (PAX Gold) y la plata (Kinesis Silver), calcula los precios de los productos basándose en su peso y prima, y los presenta en una interfaz gráfica creada con Tkinter.

## Características
- **Precios en Tiempo Real**: Actualiza los precios cada 60 segundos usando datos de CoinGecko.
- **Categorías de Productos**: Incluye monedas de oro bullion, monedas de plata, monedas de oro viejo, monedas de colección, lingotes de oro y lingotes de plata.
- **Interfaz Gráfica**: Muestra los precios en una tabla con barra de desplazamiento, junto con los precios spot por onza y por gramo.
- **Exportación**: Permite guardar los precios en un archivo CSV con un solo clic.
- **Manejo de Errores**: Reintenta las solicitudes a la API y notifica al usuario si fallan.

## Requisitos
- Python 3.x
- Librerías:
  - `requests` (para las solicitudes a la API)
  - `tkinter` (incluido con Python por defecto)

