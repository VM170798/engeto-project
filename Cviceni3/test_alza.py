import re
import pytest
from playwright.sync_api import Page, BrowserContext, expect, sync_playwright


BASE_URL = "https://www.alza.cz"
MICE_CATEGORY_URL = f"{BASE_URL}/mysi/18842900.htm"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Přepíše výchozí nastavení kontextu: realistický UA + česká lokalizace."""
    return {
        **browser_context_args,
        "user_agent": USER_AGENT,
        "viewport": {"width": 1280, "height": 800},
        "locale": "cs-CZ",
    }

def _accept_cookies(page: Page) -> None:
    """
    Zavře cookie banner kliknutím na tlačítko přijetí.
    """
    try:
        """
        dle dokumentace jsem zjistil, ze na alze lze zavrit cookie banner pomoci tohoto prikazu
        """
        btn = page.locator(".js-cookies-info-accept").first
        if btn.is_visible(timeout=4000):
            btn.click()
            page.wait_for_timeout(600)
    except Exception:
        pass

def test_homepage_loads_and_search_is_visible(page: Page):
    """
    Ověřuje, že se domovská stránka Alza.cz úspěšně načte,
    titulek obsahuje 'Alza' a vyhledávací pole je zobrazeno.
    """
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=20000)

    _accept_cookies(page)

    expect(page).to_have_title(re.compile(r"Alza", re.IGNORECASE))

    search_input = page.locator('input[placeholder*="Co hled"]').first
    expect(search_input).to_be_visible(timeout=10000)

def test_search_returns_results(page: Page):
    """
    Ověřuje, že po zadání výrazu 'myš' do vyhledávacího pole
    se přejde na stránku kategorie se zobrazením alespoň jednoho produktu.
    """
    page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=20000)

    _accept_cookies(page)

    search_input = page.locator('input[placeholder*="Co hled"]').first
    expect(search_input).to_be_visible(timeout=10000)
    search_input.click()
    search_input.fill("myš")
    search_input.press("Enter")

    page.wait_for_load_state("networkidle", timeout=20000)

    product_boxes = page.locator(".box.browsingitem")
    expect(product_boxes.first).to_be_visible(timeout=15000)

    count = product_boxes.count()
    assert count > 0, f"Očekávány produkty ve výsledcích vyhledávání, nalezeno: {count}"

def test_add_product_to_cart(page: Page):
    """
    Ověřuje, že po kliknutí na tlačítko 'Do košíku' na stránce kategorie Myši
    se odesle požadavek na přidání do košíku a košík zobrazí alespoň 1 položku.
    """

    page.goto(MICE_CATEGORY_URL, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=20000)

    _accept_cookies(page)

    buy_button = page.locator("a.btnk1").first
    expect(buy_button).to_be_visible(timeout=10000)

    with page.expect_response(
        lambda r: "OrderCommodity" in r.url or "addToCart" in r.url.lower(),
        timeout=15000,
    ) as response_info:
        buy_button.click()

    response_info.value.finished()
    page.wait_for_timeout(2000)

    basket_icon = page.locator('[data-testid="headerBasketIcon"]')
    expect(basket_icon).to_be_visible(timeout=10000)

    page.wait_for_function(
        """() => {
            const el = document.querySelector('[data-testid="headerBasketIcon"]');
            return el && !el.getAttribute('aria-label').includes('0 polo');
        }""",
        timeout=10000,
    )

    aria_label = basket_icon.get_attribute("aria-label") or ""
    assert "0 polo" not in aria_label, (
        f"Produkt nebyl přidán do košíku. aria-label košíku: '{aria_label}'"
    )
