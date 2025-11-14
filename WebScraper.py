"""
Scraper Interactivo de Amazon
Ejecutar: python amazon_interactivo.py
"""

import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
import asyncio


class web_scraper:
    def __init__(self):
        self.productos = []
        self.seleccionados = []

    async def scrape_productos(self,tienda, busqueda, cantidad=20):
        """Scrapea productos de una web de ventas"""
        print(f"\n[BUSQUEDA] Buscando: {busqueda} en {tienda}")
        print(f"[INFO] Cantidad: {cantidad} productos\n")

        async with async_playwright() as p:
            # Abrir navegador
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            page = await context.new_page()

            url = f"https://www.{tienda}/s?k={busqueda.replace(' ', '+')}"

            print("URL generada:", url)
            await page.goto(url, timeout=90000)  # 90 segundos
            print("[OK] Pagina cargada")

            # Aceptar cookies
            try:
                await page.click('#sp-cc-accept', timeout=3000)
                print("[OK] Cookies aceptadas")
            except:
                pass

            # Esperar productos
            try:
                await page.wait_for_selector('div.s-result-item', timeout=60000)
            except:
                print("[ERROR] No se encontraron productos. Verifica el término de búsqueda.")
                return []

            # Extraer productos
            elements = await page.query_selector_all('div.s-result-item')
            print(f"[INFO] Encontrados {len(elements)} elementos\n")

            for i, elem in enumerate(elements[:cantidad]):
                try:
                    # Título
                    if tienda == "temu.com":
                        # Título
                        titulo_elem = await elem.query_selector('h2.title')
                        # Precio
                        precio_elem = await elem.query_selector('.price')
                        # Rating
                        rating_elem = await elem.query_selector('.rating')
                    else:
                        match tienda:
                            case "amazon.es":
                                titulo_elem = await elem.query_selector('h2.a-text-normal span')

                    titulo = await titulo_elem.inner_text() if titulo_elem else "Sin titulo"

                    # Precio
                    precio_elem = await elem.query_selector('.a-price-whole')
                    precio_frac = await elem.query_selector('.a-price-fraction')
                    if precio_elem and precio_frac:
                        whole = await precio_elem.inner_text()
                        frac = await precio_frac.inner_text()
                        whole_cleaned = ''.join(c for c in whole if c.isdigit())
                        precio = f"{whole_cleaned},{frac}"
                        try:
                            precio_num = float(precio.replace(',', '.'))
                        except:
                            precio_num = 0
                    else:
                        precio = "N/A"
                        precio_num = 0

                    # Rating
                    rating_elem = await elem.query_selector('.a-icon-alt')
                    rating_text = await rating_elem.inner_text() if rating_elem else "Sin valoracion"

                    # Extraer número de rating
                    try:
                        rating_num = float(rating_text.split()[0].replace(',', '.'))
                    except:
                        rating_num = 0

                    # Número de reseñas
                    reviews_elem = await elem.query_selector('span[aria-label*="estrellas"]')
                    if reviews_elem:
                        reviews_text = await reviews_elem.get_attribute('aria-label')
                        try:
                            # Extraer número de reseñas del texto como "4.5 de 5 estrellas 1.234"
                            parts = reviews_text.split()
                            num_reviews = int(''.join(c for c in parts[-1] if c.isdigit()))
                        except:
                            num_reviews = 0
                    else:
                        num_reviews = 0

                    # URL
                    link_elem = await elem.query_selector('h2 a')
                    link = await link_elem.get_attribute('href') if link_elem else ""
                    url_completa = f"https://www.amazon.es{link}" if link else ""

                    producto = {
                        'id': i + 1,
                        'titulo': titulo.strip(),
                        'precio': precio,
                        'precio_num': precio_num,
                        'rating': rating_text,
                        'rating_num': rating_num,
                        'num_reviews': num_reviews,
                        'url': url_completa
                    }

                    self.productos.append(producto)
                    print(f"{i + 1}. {titulo[:60]}...")
                    print(f"   Precio: {precio} EUR | Rating: {rating_text}")

                except Exception as e:
                    print(f"[ERROR] Error en producto {i + 1}: {e}")

            # Cerrar
            await browser.close()

        print(f"\n[OK] Scraping completado: {len(self.productos)} productos")
        return self.productos

    def mostrar_productos(self):
        """Muestra lista de productos"""
        if not self.productos:
            print("[ERROR] No hay productos para mostrar")
            return

        print("\n" + "="*80)
        print("PRODUCTOS ENCONTRADOS")
        print("="*80)

        for p in self.productos:
            print(f"\n[{p['id']}] {p['titulo'][:70]}")
            print(f"    Precio: {p['precio']} EUR")
            print(f"    Rating: {p['rating']} ({p['num_reviews']} resenas)")

    def seleccionar_interactivo(self):
        """Permite seleccionar productos interactivamente"""
        if not self.productos:
            print("[ERROR] No hay productos para seleccionar")
            return

        print("\n" + "="*80)
        print("SELECCION INTERACTIVA")
        print("="*80)
        print("\nOpciones:")
        print("  - Ingresa numeros separados por comas (ej: 1,3,5)")
        print("  - Ingresa 'todos' para seleccionar todos")
        print("  - Ingresa 'mejor' para seleccionar el mejor valorado")
        print("  - Ingresa 'barato' para seleccionar el mas barato")
        print("  - Ingresa 'salir' para terminar\n")

        while True:
            opcion = input(">>> ").strip().lower()

            if opcion == 'salir':
                break

            elif opcion == 'todos':
                self.seleccionados = self.productos.copy()
                print(f"[OK] Seleccionados {len(self.seleccionados)} productos")

            elif opcion == 'mejor':
                mejor = max(self.productos, key=lambda x: (x['rating_num'], x['num_reviews']))
                self.seleccionados = [mejor]
                print(f"[OK] Seleccionado: {mejor['titulo'][:60]}")
                print(f"    Rating: {mejor['rating']}")

            elif opcion == 'barato':
                validos = [p for p in self.productos if p['precio_num'] > 0]
                if validos:
                    barato = min(validos, key=lambda x: x['precio_num'])
                    self.seleccionados = [barato]
                    print(f"[OK] Seleccionado: {barato['titulo'][:60]}")
                    print(f"    Precio: {barato['precio']} EUR")
                else:
                    print("[ERROR] No hay productos con precio valido")

            else:
                # Intentar parsear números
                try:
                    ids = [int(x.strip()) for x in opcion.split(',')]
                    self.seleccionados = [p for p in self.productos if p['id'] in ids]

                    if self.seleccionados:
                        print(f"[OK] Seleccionados {len(self.seleccionados)} productos:")
                        for p in self.seleccionados:
                            print(f"  - {p['titulo'][:60]}")
                    else:
                        print("[ERROR] No se encontraron productos con esos IDs")

                except:
                    print("[ERROR] Opcion no valida")

            # Mostrar seleccionados actuales
            if self.seleccionados:
                total = sum(p['precio_num'] for p in self.seleccionados)
                print(f"\n[CARRITO] {len(self.seleccionados)} productos - Total: {total:.2f} EUR")

    def guardar_seleccion(self):
        """Guarda los productos seleccionados"""
        if not self.seleccionados:
            print("[INFO] No hay productos seleccionados para guardar")
            return

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Guardar todos los productos
        filename_all = f'productos_todos_{timestamp}.json'
        with open(filename_all, 'w', encoding='utf-8') as f:
            json.dump(self.productos, f, ensure_ascii=False, indent=2)

        # Guardar seleccionados
        filename_sel = f'productos_seleccionados_{timestamp}.json'
        with open(filename_sel, 'w', encoding='utf-8') as f:
            json.dump(self.seleccionados, f, ensure_ascii=False, indent=2)

        # Crear resumen
        total = sum(p['precio_num'] for p in self.seleccionados)
        resumen = {
            'fecha': timestamp,
            'total_productos': len(self.productos),
            'productos_seleccionados': len(self.seleccionados),
            'total_precio': total,
            'productos': self.seleccionados
        }

        filename_resumen = f'resumen_compra_{timestamp}.json'
        with open(filename_resumen, 'w', encoding='utf-8') as f:
            json.dump(resumen, f, ensure_ascii=False, indent=2)

        # Guardar solo los títulos de los seleccionados
        filename_titulos = f'titulos_seleccionados_{timestamp}.txt'
        with open(filename_titulos, 'w', encoding='utf-8') as f:
            for p in self.seleccionados:
                f.write(p['titulo'] + '\n')

        print(f"\n[OK] Guardado:")
        print(f"  - Todos: {filename_all}")
        print(f"  - Seleccionados: {filename_sel}")
        print(f"  - Resumen: {filename_resumen}")
        print(f"  - Títulos: {filename_titulos}")

    def mostrar_resumen(self):
        """Muestra resumen de la selección"""
        if not self.seleccionados:
            print("\n[INFO] No hay productos seleccionados")
            return

        print("\n" + "="*80)
        print("RESUMEN DE COMPRA")
        print("="*80)

        total = 0
        for i, p in enumerate(self.seleccionados, 1):
            print(f"\n{i}. {p['titulo'][:70]}")
            print(f"   Precio: {p['precio']} EUR")
            print(f"   Rating: {p['rating']}")
            print(f"   URL: {p['url'][:60]}...")
            if p['precio_num'] > 0:
                total += p['precio_num']

        print("\n" + "-"*80)
        print(f"TOTAL: {total:.2f} EUR")
        print("="*80)


async def main():
    """Función principal"""
    print("\n" + "="*80)
    print("SCRAPER INTERACTIVO DE webs")
    print("="*80)

    # Configuración
    # Ir a la tienda
    print(f"pregunto por la tienda")
    tienda = input("¿En qué tienda quieres buscar? (por ejemplo: amazon.es o temu.com): ").strip()
    print(f"pregunto por el producto")
    busqueda = input("\n¿Qué quieres buscar?: ").strip()
    if not busqueda:
        busqueda = "articulos"

    try:
        cantidad = int(input("Cuantos productos quieres ver? [20]: ").strip() or "20")
    except:
        cantidad = 20

    # Crear scraper
    scraper = web_scraper()

    # Scrapear
    await scraper.scrape_productos(tienda, busqueda, cantidad)

    # Mostrar productos
    scraper.mostrar_productos()

    # Selección interactiva
    scraper.seleccionar_interactivo()

    # Mostrar resumen
    scraper.mostrar_resumen()

    # Guardar
    scraper.guardar_seleccion()

    print("\n[OK] Proceso completado!")


if __name__ == "__main__":
    asyncio.run(main())
