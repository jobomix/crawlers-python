import pathlib

from snapshottest.pytest import SnapshotSession

from crawlers.amazon.amazon_params import AmazonParams
from crawlers.amazon.amazon_product import crawl_amazon_product, extract_root_url

filepath = pathlib.Path(__file__).resolve().parent


def test_extract_root_url() -> None:
    root_url = extract_root_url(
        'https://www.amazon.com.au/customer-preferences/country?ref_=icp_lop_mop_chg&preferencesReturnUrl=/'
    )
    assert root_url == 'https://www.amazon.com.au'


def test_product_page_nl_be(snapshot: SnapshotSession) -> None:
    result = crawl_amazon_product(
        f'file://{filepath}/nl_BE/almond_oil.html', AmazonParams()
    )
    snapshot.assert_match(result)


def test_product_page_en_au(snapshot: SnapshotSession) -> None:
    result = crawl_amazon_product(
        f'file://{filepath}/en_AU/duracell.html', AmazonParams()
    )
    snapshot.assert_match(result)


def test_product_page_ar_ag(snapshot: SnapshotSession) -> None:
    result = crawl_amazon_product(
        f'file://{filepath}/ar_EG/inifinix.html', AmazonParams()
    )
    snapshot.assert_match(result)


def test_product_page_en_gb(snapshot: SnapshotSession) -> None:
    result = crawl_amazon_product(f'file://{filepath}/en_GB/gopro.html', AmazonParams())
    snapshot.assert_match(result)


def test_product_page_en_fr(snapshot: SnapshotSession) -> None:
    result = crawl_amazon_product(f'file://{filepath}/fr_FR/gopro.html', AmazonParams())
    snapshot.assert_match(result)


def test_product_page_de_de(snapshot: SnapshotSession) -> None:
    result = crawl_amazon_product(f'file://{filepath}/de_DE/gopro.html', AmazonParams())
    snapshot.assert_match(result)


def test_product_page_ja_ja(snapshot: SnapshotSession) -> None:
    result = crawl_amazon_product(
        f'file://{filepath}/ja_JP/makita.html', AmazonParams()
    )
    snapshot.assert_match(result)
