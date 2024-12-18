from typing import Any
from unittest.mock import Mock

from xtracted_common.model import AmazonProductUrl

from tests.integration.amazon_server import new_web_app
from xtracted.context import CrawlContext
from xtracted.crawlers.amazon.amazon_async_product import AmazonAsyncProduct


async def test_extract_data_update_crawl_context(aiohttp_server: Any) -> None:
    server = await aiohttp_server(new_web_app())

    ctx = Mock(spec=CrawlContext)
    crawl_url = AmazonProductUrl(
        job_id='124667',
        url=f'http://localhost:{server.port}/dp/B01GFPWTI4?x=foo&bar=y',
        uid='dummy-uid',
    )
    ctx.get_crawl_url.return_value = crawl_url
    aap = AmazonAsyncProduct(crawl_context=ctx)
    await aap.crawl()
    extracted = ctx.complete.call_args.args[0]
    ctx.complete.assert_called_once()
    assert extracted['asin'] == 'B01GFPWTI4'
    assert (
        extracted['url'] == f'http://localhost:{server.port}/dp/B01GFPWTI4?x=foo&bar=y'
    )


async def test_with_failing_product(aiohttp_server: Any) -> None:
    server = await aiohttp_server(new_web_app())

    ctx = Mock(spec=CrawlContext)
    crawl_url = AmazonProductUrl(
        job_id='124667',
        url=f'http://localhost:{server.port}/dp/B0BXD1PRJQ?x=foo&bar=y',
        uid='dummy-uid',
    )
    ctx.get_crawl_url.return_value = crawl_url
    aap = AmazonAsyncProduct(crawl_context=ctx)
    await aap.crawl()
    ctx.fail.assert_called_once()
