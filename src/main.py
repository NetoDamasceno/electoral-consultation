from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://www.tse.jus.br/servicos-eleitorais/autoatendimento-eleitoral"
        "?utm_source=chatgpt.com"
        "#/atendimento-eleitor/consultar-situacao-titulo-eleitor"
    )

    campo_identificacao = page.get_by_placeholder(
        "Número do título eleitoral ou CPF ou nome"
    )

    campo_identificacao.fill("LUIZ ANTONIO SOARES DAMASCENO NETO")

    campo_identificacao.press("Tab")

    page.wait_for_timeout(500)

    page.keyboard.type("13/07/2005")

    page.keyboard.press("Enter")

    page.wait_for_timeout(5000)

    situacao = page.locator("span[class^='situacao-']").inner_text()
    mensagem = page.locator("span[class^='situacao-']").locator("..").inner_text()

    print(f"Situação encontrada: {situacao}")
    print(f"Mensagem: {mensagem}")

    input("Pressione ENTER para fechar o navegador...")

    browser.close()