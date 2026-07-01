from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime


def gerar_seletor_css(tag, classe, id_elem):
    """Gera um seletor CSS prioritário para o elemento"""
    if id_elem:
        return f"#{id_elem}"
    if classe:
        classes = classe.strip().split()
        if len(classes) == 1:
            return f".{classes[0]}"
        else:
            return f".{'.'.join(classes)}"
    return tag


def gerar_xpath(tag, classe, id_elem, posicao):
    """Gera um XPath simplificado"""
    if id_elem:
        return f'//{tag}[@id="{id_elem}"]'
    if classe:
        classes = classe.strip().split()
        return f'//{tag}[contains(@class, "{classes[0]}")]'
    return f"//{tag}[{posicao}]"


def analisar_estrutura(url):
    """
    Analisa a estrutura de um site, extraindo tags, classes, IDs e textos.
    Agora com profundidade, posição, seletor CSS e XPath!
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True
        )  # Mudando pra headless pra ser mais rápido
        page = browser.new_page()
        page.goto(url, timeout=60000, wait_until="domcontentloaded")

        # Scroll pra carregar conteúdo dinâmico
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(1000)

        # Pega TODOS os elementos com posição e profundidade
        elementos = page.query_selector_all("*")

        dados = []
        for posicao, elem in enumerate(elementos, 1):
            try:
                tag = elem.evaluate("el => el.tagName.toLowerCase()")
                classe = elem.get_attribute("class") or ""
                id_elem = elem.get_attribute("id") or ""
                link = elem.get_attribute("href") or ""

                # Pega o texto de forma mais limpa
                texto = (
                    elem.inner_text().strip()[:300] if elem.inner_text().strip() else ""
                )

                # Calcula profundidade (nível no DOM)
                profundidade = elem.evaluate("""
                    (el) => {
                        let depth = 0;
                        let parent = el.parentElement;
                        while (parent) {
                            depth++;
                            parent = parent.parentElement;
                        }
                        return depth;
                    }
                """)

                # Pega o pai (opcional)
                pai = elem.evaluate(
                    "el => el.parentElement ? el.parentElement.tagName.toLowerCase() : ''"
                )

                # Gera seletores
                seletor_css = gerar_seletor_css(tag, classe, id_elem)
                xpath = gerar_xpath(tag, classe, id_elem, posicao)

                # Só adiciona se tiver algo relevante
                if texto or classe or id_elem or link:
                    dados.append(
                        {
                            "posicao": posicao,
                            "profundidade": profundidade,
                            "tag": tag,
                            "classe": classe,
                            "id": id_elem,
                            "link": link,
                            "texto": texto,
                            "pai": pai,
                            "seletor_css": seletor_css,
                            "xpath": xpath,
                        }
                    )
            except Exception as e:
                # Ignora elementos problemáticos
                pass

        print(f"✅ {len(dados)} elementos analisados.")
        browser.close()
        return dados


def salvar_excel(dados, nome_arquivo="estrutura.xlsx"):
    """Salva os dados em um arquivo Excel com formatação básica"""
    df = pd.DataFrame(dados)

    # Reordena as colunas pra ficar mais organizado
    colunas = [
        "posicao",
        "profundidade",
        "tag",
        "classe",
        "id",
        "seletor_css",
        "xpath",
        "link",
        "texto",
        "pai",
    ]
    df = df[colunas]

    # Salva com formatação
    with pd.ExcelWriter(nome_arquivo, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Estrutura", index=False)

        # Ajusta a largura das colunas
        worksheet = writer.sheets["Estrutura"]
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            worksheet.column_dimensions[column_letter].width = adjusted_width

    print(f"📁 Estrutura salva em {nome_arquivo}")


def mostrar_estatisticas(dados):
    """Mostra estatísticas básicas da análise"""
    tags = {}
    classes = {}
    ids = []

    for item in dados:
        tag = item["tag"]
        tags[tag] = tags.get(tag, 0) + 1

        if item["classe"]:
            for cls in item["classe"].split():
                classes[cls] = classes.get(cls, 0) + 1

        if item["id"]:
            ids.append(item["id"])

    print("\n" + "=" * 60)
    print("📊 ESTATÍSTICAS DA ANÁLISE")
    print("=" * 60)
    print(f"Total de elementos: {len(dados)}")
    print(f"Tags únicas: {len(tags)}")
    print(f"Classes únicas: {len(classes)}")
    print(f"IDs únicos: {len(set(ids))}")
    print(f"Links encontrados: {sum(1 for x in dados if x['link'])}")

    print("\n🏷️ TOP 10 TAGS:")
    for tag, count in sorted(tags.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {tag}: {count}")

    print("\n🏷️ TOP 10 CLASSES:")
    for cls, count in sorted(classes.items(), key=lambda x: x[1], reverse=True)[:10]:
        print(f"  {cls}: {count}")


def main():
    print("=" * 60)
    print("🏗️  STRUCT ANALYZER - VERSÃO TURBO")
    print("📌 Analisa a estrutura de qualquer site com profundidade e seletores")
    print("=" * 60)

    url = input("🌐 Qual site você quer analisar? ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"\n🔍 Analisando {url}...\n")

    dados = analisar_estrutura(url)

    if dados:
        nome_arquivo = f"estrutura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        salvar_excel(dados, nome_arquivo)
        mostrar_estatisticas(dados)
    else:
        print("❌ Nenhum dado foi extraído. Verifique a URL.")


if __name__ == "__main__":
    main()
