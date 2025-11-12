# coding=utf-8
"""
Crypto news platform crawlers
"""

import json
import re
import time
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


class BaseCrawler:
    """Base crawler class"""
    
    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def get_proxies(self):
        """Get proxy configuration"""
        if self.proxy_url:
            return {"http": self.proxy_url, "https": self.proxy_url}
        return None
    
    def fetch_page(self, url: str, timeout: int = 15) -> Optional[BeautifulSoup]:
        """Fetch and parse a web page"""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=timeout
            )
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def crawl(self) -> List[Dict]:
        """Crawl news from the platform. Must be implemented by subclasses."""
        raise NotImplementedError


class CoinDeskCrawler(BaseCrawler):
    """CoinDesk crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl CoinDesk news"""
        items = []
        try:
            # CoinDesk RSS feed
            rss_url = "https://www.coindesk.com/arc/outboundfeeds/rss/"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]  # Get top 50
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"CoinDesk crawl error: {e}")
        
        return items


class CointelegraphCrawler(BaseCrawler):
    """Cointelegraph crawler - filtered for Base chain content"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Cointelegraph news, filtering for Base chain, Coinbase L2, Superchain"""
        items = []
        try:
            # Cointelegraph RSS feed
            rss_url = "https://cointelegraph.com/rss"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            # Keywords to filter for Base-related content
            base_keywords = ['base chain', 'coinbase l2', 'superchain', 'base network', 'base ecosystem']
            
            entries = soup.find_all('item')[:100]  # Check more entries to filter
            index = 1
            for entry in entries:
                title_elem = entry.find('title')
                link_elem = entry.find('link')
                description_elem = entry.find('description')
                
                if title_elem and link_elem:
                    title = title_elem.get_text().strip()
                    link = link_elem.get_text().strip()
                    description = description_elem.get_text().strip() if description_elem else ""
                    
                    # Check if title or description contains Base-related keywords
                    text_to_check = (title + " " + description).lower()
                    if any(keyword.lower() in text_to_check for keyword in base_keywords):
                        items.append({
                            "title": title,
                            "url": link,
                            "mobileUrl": link,
                            "rank": index
                        })
                        index += 1
                        if index > 50:
                            break
        except Exception as e:
            print(f"Cointelegraph crawl error: {e}")
        
        return items


class DecryptCrawler(BaseCrawler):
    """Decrypt crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Decrypt news"""
        items = []
        try:
            # Decrypt RSS feed
            rss_url = "https://decrypt.co/feed"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"Decrypt crawl error: {e}")
        
        return items


class BeInCryptoCrawler(BaseCrawler):
    """BeInCrypto crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl BeInCrypto news"""
        items = []
        try:
            # BeInCrypto RSS feed
            rss_url = "https://beincrypto.com/feed/"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"BeInCrypto crawl error: {e}")
        
        return items


class CoinGapeCrawler(BaseCrawler):
    """CoinGape crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl CoinGape news"""
        items = []
        try:
            # CoinGape RSS feed
            rss_url = "https://coingape.com/feed/"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"CoinGape crawl error: {e}")
        
        return items


class CryptonewsCrawler(BaseCrawler):
    """Cryptonews crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Cryptonews news"""
        items = []
        try:
            # Cryptonews RSS feed
            rss_url = "https://cryptonews.com/news/feed/"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"Cryptonews crawl error: {e}")
        
        return items


class TheBlockCrawler(BaseCrawler):
    """The Block crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl The Block news"""
        items = []
        try:
            # The Block RSS feed
            rss_url = "https://www.theblock.co/rss.xml"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"The Block crawl error: {e}")
        
        return items


class CoinpediaCrawler(BaseCrawler):
    """Coinpedia crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Coinpedia news"""
        items = []
        try:
            # Coinpedia RSS feed
            rss_url = "https://coinpedia.org/feed/"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"Coinpedia crawl error: {e}")
        
        return items


class BaseBlogCrawler(BaseCrawler):
    """Base Blog crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Base Blog news"""
        items = []
        try:
            # Base Blog RSS feed
            rss_url = "https://base.org/blog/feed"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            print(f"Base Blog crawl error: {e}")
        
        return items


class MirrorXYZCrawler(BaseCrawler):
    """Mirror.xyz crawler - searches for Base-related content"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Mirror.xyz for Base-related articles"""
        items = []
        try:
            # Mirror.xyz doesn't have a direct RSS, so we'll search for Base-related content
            # Using search API or scraping the homepage
            search_url = "https://mirror.xyz/_next/data/feed.json"
            # Alternative: scrape homepage and filter for Base
            homepage_url = "https://mirror.xyz"
            
            soup = self.fetch_page(homepage_url)
            if soup:
                # Look for article links containing "base" or related keywords
                articles = soup.find_all('a', href=True)
                base_keywords = ['base', 'base chain', 'coinbase l2', 'superchain']
                
                seen_titles = set()
                index = 1
                for article in articles[:100]:  # Check first 100 links
                    href = article.get('href', '')
                    text = article.get_text().strip().lower()
                    
                    # Check if link or text contains Base-related keywords
                    if any(keyword in text or keyword in href.lower() for keyword in base_keywords):
                        title = article.get_text().strip()
                        if title and title not in seen_titles and len(title) > 10:
                            full_url = urljoin(homepage_url, href) if href.startswith('/') else href
                            items.append({
                                "title": title,
                                "url": full_url,
                                "mobileUrl": full_url,
                                "rank": index
                            })
                            seen_titles.add(title)
                            index += 1
                            if index > 50:
                                break
        except Exception as e:
            print(f"Mirror.xyz crawl error: {e}")
        
        return items


class BaseMirrorCrawler(BaseCrawler):
    """Base Mirror (base.mirror.xyz) crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Base Mirror blog"""
        items = []
        try:
            # Base Mirror RSS feed
            rss_url = "https://base.mirror.xyz/feed"
            response = requests.get(
                rss_url,
                headers=self.headers,
                proxies=self.get_proxies(),
                timeout=15
            )
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            
            entries = soup.find_all('item')[:50]
            for index, entry in enumerate(entries, 1):
                title = entry.find('title')
                link = entry.find('link')
                if title and link:
                    items.append({
                        "title": title.get_text().strip(),
                        "url": link.get_text().strip(),
                        "mobileUrl": link.get_text().strip(),
                        "rank": index
                    })
        except Exception as e:
            # If RSS fails, try scraping the page
            try:
                homepage_url = "https://base.mirror.xyz"
                soup = self.fetch_page(homepage_url)
                if soup:
                    articles = soup.find_all(['article', 'div'], class_=lambda x: x and ('post' in x.lower() or 'article' in x.lower()))
                    for index, article in enumerate(articles[:50], 1):
                        title_elem = article.find(['h1', 'h2', 'h3', 'a'])
                        link_elem = article.find('a', href=True)
                        if title_elem and link_elem:
                            title = title_elem.get_text().strip()
                            link = link_elem.get('href', '')
                            if title:
                                full_url = urljoin(homepage_url, link) if link.startswith('/') else link
                                items.append({
                                    "title": title,
                                    "url": full_url,
                                    "mobileUrl": full_url,
                                    "rank": index
                                })
            except Exception as e2:
                print(f"Base Mirror crawl error: {e}, fallback error: {e2}")
        
        return items


class DeFiLlamaCrawler(BaseCrawler):
    """DeFiLlama News crawler"""
    
    def crawl(self) -> List[Dict]:
        """Crawl DeFiLlama news, focusing on Base"""
        items = []
        try:
            # DeFiLlama news page
            news_url = "https://defillama.com/news"
            soup = self.fetch_page(news_url)
            
            if soup:
                # Look for news articles
                articles = soup.find_all(['article', 'div'], class_=lambda x: x and ('news' in str(x).lower() or 'article' in str(x).lower() or 'post' in str(x).lower()))
                
                # Also try finding links with Base-related content
                base_keywords = ['base', 'base chain', 'coinbase l2']
                seen_titles = set()
                index = 1
                
                for article in articles[:100]:
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    link_elem = article.find('a', href=True)
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text().strip()
                        link = link_elem.get('href', '')
                        text_content = article.get_text().lower()
                        
                        # Filter for Base-related content
                        if any(keyword in text_content or keyword in title.lower() for keyword in base_keywords):
                            if title and title not in seen_titles and len(title) > 10:
                                full_url = urljoin(news_url, link) if link.startswith('/') else link
                                items.append({
                                    "title": title,
                                    "url": full_url,
                                    "mobileUrl": full_url,
                                    "rank": index
                                })
                                seen_titles.add(title)
                                index += 1
                                if index > 50:
                                    break
        except Exception as e:
            print(f"DeFiLlama crawl error: {e}")
        
        return items


class MessariCrawler(BaseCrawler):
    """Messari crawler - research reports about Base"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Messari for Base and Optimism research"""
        items = []
        try:
            # Messari research page
            research_url = "https://messari.io/research"
            soup = self.fetch_page(research_url)
            
            if soup:
                # Look for research articles
                base_keywords = ['base', 'base chain', 'coinbase l2', 'superchain', 'optimism']
                seen_titles = set()
                index = 1
                
                # Find article links
                articles = soup.find_all(['article', 'div', 'a'], class_=lambda x: x and ('research' in str(x).lower() or 'report' in str(x).lower() or 'article' in str(x).lower()))
                
                for article in articles[:100]:
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4'])
                    if not title_elem:
                        title_elem = article if article.name in ['h1', 'h2', 'h3', 'h4'] else None
                    
                    link_elem = article.find('a', href=True) if article.name != 'a' else article
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text().strip()
                        link = link_elem.get('href', '') if hasattr(link_elem, 'get') else str(link_elem.get('href', ''))
                        text_content = article.get_text().lower()
                        
                        # Filter for Base/Optimism related content
                        if any(keyword in text_content or keyword in title.lower() for keyword in base_keywords):
                            if title and title not in seen_titles and len(title) > 10:
                                full_url = urljoin(research_url, link) if link.startswith('/') else link
                                items.append({
                                    "title": title,
                                    "url": full_url,
                                    "mobileUrl": full_url,
                                    "rank": index
                                })
                                seen_titles.add(title)
                                index += 1
                                if index > 50:
                                    break
        except Exception as e:
            print(f"Messari crawl error: {e}")
        
        return items


class AirdropsIOCrawler(BaseCrawler):
    """Airdrops.io crawler - Base airdrop updates"""
    
    def crawl(self) -> List[Dict]:
        """Crawl Airdrops.io for Base airdrop updates"""
        items = []
        try:
            # Airdrops.io homepage or Base filter
            base_url = "https://airdrops.io"
            # Try to filter by Base
            search_url = f"{base_url}/?chain=base"
            soup = self.fetch_page(search_url)
            
            if not soup:
                soup = self.fetch_page(base_url)
            
            if soup:
                # Look for airdrop listings
                airdrops = soup.find_all(['div', 'article', 'li'], class_=lambda x: x and ('airdrop' in str(x).lower() or 'project' in str(x).lower()))
                
                seen_titles = set()
                index = 1
                
                for airdrop in airdrops[:100]:
                    title_elem = airdrop.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    link_elem = airdrop.find('a', href=True)
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text().strip()
                        link = link_elem.get('href', '')
                        
                        # Check if it's Base-related
                        text_content = airdrop.get_text().lower()
                        if 'base' in text_content or 'base' in title.lower():
                            if title and title not in seen_titles and len(title) > 5:
                                full_url = urljoin(base_url, link) if link.startswith('/') else link
                                items.append({
                                    "title": title,
                                    "url": full_url,
                                    "mobileUrl": full_url,
                                    "rank": index
                                })
                                seen_titles.add(title)
                                index += 1
                                if index > 50:
                                    break
        except Exception as e:
            print(f"Airdrops.io crawl error: {e}")
        
        return items


class CryptoSlateCrawler(BaseCrawler):
    """CryptoSlate crawler - filter by Base blockchain"""
    
    def crawl(self) -> List[Dict]:
        """Crawl CryptoSlate filtered by Base blockchain"""
        items = []
        try:
            # CryptoSlate with Base filter
            base_filter_url = "https://cryptoslate.com/?s=base+chain"
            soup = self.fetch_page(base_filter_url)
            
            if soup:
                # Look for article links
                articles = soup.find_all(['article', 'div'], class_=lambda x: x and ('post' in str(x).lower() or 'article' in str(x).lower() or 'news' in str(x).lower()))
                
                seen_titles = set()
                index = 1
                
                for article in articles[:100]:
                    title_elem = article.find(['h1', 'h2', 'h3', 'h4', 'a'])
                    link_elem = article.find('a', href=True)
                    
                    if title_elem and link_elem:
                        title = title_elem.get_text().strip()
                        link = link_elem.get('href', '')
                        
                        if title and title not in seen_titles and len(title) > 10:
                            full_url = urljoin(base_filter_url, link) if link.startswith('/') else link
                            items.append({
                                "title": title,
                                "url": full_url,
                                "mobileUrl": full_url,
                                "rank": index
                            })
                            seen_titles.add(title)
                            index += 1
                            if index > 50:
                                break
        except Exception as e:
            print(f"CryptoSlate crawl error: {e}")
        
        return items


# Crawler registry
CRAWLERS = {
    "coindesk": CoinDeskCrawler,
    "cointelegraph": CointelegraphCrawler,
    "decrypt": DecryptCrawler,
    "beincrypto": BeInCryptoCrawler,
    "coingape": CoinGapeCrawler,
    "cryptonews": CryptonewsCrawler,
    "theblock": TheBlockCrawler,
    "coinpedia": CoinpediaCrawler,
    "base-blog": BaseBlogCrawler,
    "mirror-xyz": MirrorXYZCrawler,
    "base-mirror": BaseMirrorCrawler,
    "defillama": DeFiLlamaCrawler,
    "messari": MessariCrawler,
    "airdrops-io": AirdropsIOCrawler,
    "cryptoslate": CryptoSlateCrawler,
}


def get_crawler(platform_id: str, proxy_url: Optional[str] = None) -> Optional[BaseCrawler]:
    """Get crawler instance for a platform"""
    crawler_class = CRAWLERS.get(platform_id.lower())
    if crawler_class:
        return crawler_class(proxy_url=proxy_url)
    return None


def crawl_platform(platform_id: str, proxy_url: Optional[str] = None) -> Dict:
    """
    Crawl a platform and return data in the expected format
    
    Returns:
        Dict with 'status' and 'items' keys, matching the old API format
    """
    crawler = get_crawler(platform_id, proxy_url)
    if not crawler:
        return {
            "status": "error",
            "message": f"Unknown platform: {platform_id}",
            "items": []
        }
    
    try:
        items = crawler.crawl()
        return {
            "status": "success",
            "items": items
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "items": []
        }

