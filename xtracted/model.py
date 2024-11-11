import re
from abc import ABC, abstractmethod
from typing import Any, ClassVar, Optional, Pattern

from pydantic import (
    AfterValidator,
    AnyHttpUrl,
    AnyUrl,
    BaseModel,
)
from typing_extensions import Annotated
from xtracted_common.model import XtractedUrl

from xtracted.crawlers.amazon.amazon_params import AmazonParams

allowed_hosts = [
    'www.amazon.com.au',
    'www.amazon.com.be',
    'www.amazon.com.br',
    'www.amazon.ca',
    'www.amazon.cn',
    'www.amazon.eg',
    'www.amazon.fr',
    'www.amazon.de',
    'www.amazon.in',
    'www.amazon.it',
    'www.amazon.co.jp',
    'www.amazon.com.mx',
    'www.amazon.nl',
    'www.amazon.pl',
    'www.amazon.sa',
    'www.amazon.sg',
    'www.amazon.co.za',
    'www.amazon.es',
    'www.amazon.se',
    'www.amazon.com.tr',
    'www.amazon.ae',
    'www.amazon.co.uk',
    'www.amazon.com',
]

amazon_url_asin_path = re.compile(r'.*/dp/[A-Z0-9]{10}.*')


def check_amazon_valid_url(url: AnyHttpUrl) -> Optional[AnyHttpUrl]:
    if url.scheme != 'https':
        raise InvalidUrlException(
            f'Url {url} is invalid. Only url with https scheme are valid.'
        )

    if url.host not in allowed_hosts:
        domains = ',\n'.join(allowed_hosts)
        raise InvalidUrlException(
            f"""Url {url} is invalid. Valid domain are one of \n{domains}"""
        )

    if url.path and not amazon_url_asin_path.match(url.path):
        raise InvalidUrlException(
            f'Url {url} is invalid. Url must be an Amazon product page url'
        )
    return url


ValidAmazonUrl = Annotated[AnyHttpUrl, AfterValidator(check_amazon_valid_url)]


class CrawlException(Exception):
    pass


class Extractor(ABC):
    @abstractmethod
    async def crawl(self) -> None:
        pass


class InvalidUrlException(Exception):
    pass


class CrawlJobInput(BaseModel):
    """
    Crawl job Representation. Contains mainly a set of urls.
    """

    urls: set[ValidAmazonUrl] = set()
    params: Optional[AmazonParams] = None


class CrawlJobFreeInput(CrawlJobInput):
    urls: set[AnyUrl] = set()
