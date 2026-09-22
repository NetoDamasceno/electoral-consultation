from playwright.sync_api import sync_playwright


URL_CONSULTA = (
    "https://www.tse.jus.br/servicos-eleitorais/autoatendimento-eleitoral"
    "?utm_source=chatgpt.com"
    "#/atendimento-eleitor/consultar-situacao-titulo-eleitor"
)


def consultar_eleitor(page, nome, data_nascimento):
    page.goto(URL_CONSULTA)

    campo_identificacao = page.get_by_placeholder(
        "Número do título eleitoral ou CPF ou nome"
    )

    campo_identificacao.fill(nome)

    campo_identificacao.press("Tab")

    page.wait_for_timeout(500)

    page.keyboard.type(data_nascimento)

    page.keyboard.press("Enter")

    page.wait_for_timeout(5000)

    aviso = page.get_by_text(
        "Não foi possível localizar um eleitor com os dados informados."
    )

    if aviso.is_visible():
         mensagem = (
            "Não foi possível localizar um eleitor com os dados informados. "
            "Verifique se todas as informações estão corretas."
         )

         page.goto(URL_CONSULTA)
                
         return {
            "situacao": "NÃO ENCONTRADO",
            "mensagem": mensagem,
         }

    situacao = page.locator(
        "span[class^='situacao-']"
    ).inner_text()

    mensagem = page.locator(
        "span[class^='situacao-']"
    ).locator("..").inner_text()

    return {
        "situacao": situacao,
        "mensagem": mensagem,
    }


with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)

    page = browser.new_page()

    resultado1 = consultar_eleitor(
        page,
        "LUIZ ANTONIO SOARES DAMASCENO NETO",
        "13/07/2005",
    )

    print(f"Consulta 1 - Situação: {resultado1['situacao']}")
    print(f"Consulta 1 - Mensagem: {resultado1['mensagem']}")


    resultado2 = consultar_eleitor(
        page,
        "Fulano de Tal",
        "13/07/2005",
    )

    print(f"Consulta 2 - Situação: {resultado2['situacao']}")
    print(f"Consulta 2 - Mensagem: {resultado2['mensagem']}")

    input("Pressione ENTER para fechar o navegador...")

    browser.close()