from playwright.sync_api import sync_playwright
import urllib.parse

def obtener_url_producto(context, referencia):
    # URL base de búsqueda en el sitio de Phywe
    base_search_url = 'https://www.phywe.com/search/?query='

    # Construye la URL de búsqueda con la referencia
    search_url = base_search_url + urllib.parse.quote(referencia)

    # Crea una nueva página en el contexto existente
    page = context.new_page()

    try:
        # Navega directamente a la URL de búsqueda
        page.goto(search_url, wait_until='networkidle')

        # Verifica si la URL final es diferente a la de búsqueda
        if page.url != search_url:
            # Si la URL cambia, probablemente estamos en la página del producto
            return page.url

        # Alternativamente, buscar un título de producto o un código de referencia
        # Intenta buscar un elemento que esté presente en todas las páginas de productos
        producto_titulo = page.query_selector('h1')
        if producto_titulo:
            return page.url
        else:
            print(f"No se encontró el producto para la referencia {referencia}")
            return None

    except Exception as e:
        print(f"Error al obtener la URL del producto para la referencia {referencia}: {e}")
        return None
    finally:
        page.close()

def main():
    # Lee las referencias desde el archivo referencias.txt
    with open('referencias.txt', 'r', encoding='utf-8') as f:
        referencias = [line.strip() for line in f if line.strip()]

    with sync_playwright() as p:
        # Inicia el navegador una vez
        browser = p.chromium.launch()
        context = browser.new_context()

        for referencia in referencias:
            try:
                print(f"Buscando URL para la referencia: {referencia}")
                url = obtener_url_producto(context, referencia)
                if not url:
                    continue  # Si no se encontró la URL, pasa a la siguiente referencia

                page = context.new_page()
                print(f"Procesando: {url}")
                page.goto(url, wait_until='networkidle')

                # Genera un nombre de archivo basado en la referencia
                pdf_file_name = f"{referencia}.pdf"

                # Genera el PDF utilizando los estilos de impresión
                page.pdf(path=pdf_file_name, format='A4', print_background=True)

                print(f"PDF guardado: {pdf_file_name}")
                page.close()
            except Exception as e:
                print(f"Error al procesar la referencia {referencia}: {e}")
        browser.close()

if __name__ == "__main__":
    main()
