import asyncio
import os
import sys
from playwright.async_api import async_playwright
import nest_asyncio

# Forzar el uso del event loop correcto según el sistema operativo
if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
else:
    try:
        import uvloop
        uvloop.install()
    except ImportError:
        pass

async def main():
    print("[INFO] Iniciando navegador...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # Muestra el navegador
        page = await browser.new_page()

        print("[INFO] Navegando a Amazon...")
        await page.goto("https://www.amazon.es")
        print("[OK] Pagina cargada")

        try:
            print("[INFO] Rellenando campo de búsqueda...")
            await page.fill('#twotabsearchtextbox', 'God of War')  # Cambia el término de búsqueda
            print("[OK] Campo de búsqueda rellenado")

            print("[INFO] Haciendo clic en el botón de búsqueda...")
            await page.click('#nav-search-submit-button')
            print("[OK] Búsqueda iniciada")

            print("[INFO] Esperando que se carguen los resultados...")
            await page.wait_for_load_state("networkidle")  # Asegura que todas las solicitudes se completen
            await page.wait_for_timeout(3000)  # 3 segundos adicionales para asegurar la carga
            print("[OK] Resultados cargados")

            html = await page.content()
            with open("amazon_search.html", "w", encoding="utf-8") as f:
                f.write(html)
            print("[INFO] HTML guardado en 'amazon_search.html' para inspección manual")

            try:
                print("[INFO] Intentando extraer título del primer producto...")

                # Selector actualizado para el título del primer producto
                titulo_elem = await page.locator(
                    "div.s-result-item.s-result-item.aplast div.a-section.a-spacing-none.h2 a.a-link-normal.s-no-outline"
                ).first.get_by_role("heading", name="Título del producto").first

                if await titulo_elem.is_visible():
                    titulo = await titulo_elem.text_content()
                    print(f"[OK] Título encontrado: {titulo}")
                else:
                    print("[ERROR] El título no es visible o no existe")

            except Exception as e:
                print(f"[ERROR] No se pudo encontrar el título: {e}")

            # Extraer todos los títulos de los resultados
            titulos = await page.locator(
                "div.s-result-item.s-result-item.aplast div.a-section.a-spacing-none.h2 a.a-link-normal.s-no-outline"
            ).all_text_contents()

            print(f"[OK] Títulos encontrados: {titulos}")

            # Mantener el navegador abierto para inspección
            print("[INFO] Pausa para inspección manual. Presione Enter en la consola para continuar.")
            input("Presione Enter para cerrar el navegador...")

        except Exception as e:
            print(f"[ERROR] Ocurrió un error durante la ejecución: {e}")

        finally:
            print("[INFO] Cerrando navegador...")
            await browser.close()
            print("[OK] Navegador cerrado")

# Ejecutar el script
if __name__ == "__main__":
    nest_asyncio.apply()  # ✅ Patch the loop
    asyncio.run(main())   # ✅ Run the async main
