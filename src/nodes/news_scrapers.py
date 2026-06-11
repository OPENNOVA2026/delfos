import gc
from typing import TypedDict

import newspaper
from newspaper import Article
from rich.console import Group
from rich.live import Live

from core.config import NewsOrigin, get_config
from core.logger import console, logger
from nodes.graph_state import StateVoids
from src.core.settings import settings
from utils.displayers import build_progress_bar, build_spinner


class PaperType(TypedDict):
    paper: newspaper.Source
    origin: NewsOrigin


class GetNewspaperNews:
    def __init__(self):
        self.papers: list[PaperType] = []
        self.articles = []
        self.titles = []
        self.config = get_config(settings.config_id)
        self.news_spinner = build_spinner()
        self.paper_progress_bar = build_progress_bar()
        self.news_progress_bar = build_progress_bar()
        self.renders_group = Group(
            self.news_spinner, self.paper_progress_bar, self.news_progress_bar
        )
        self.live = Live(self.renders_group, console=console, transient=True)

    def __call__(self, state: StateVoids):
        self.news_spinner.add_task("Retrieving news!! :newspaper:", total=None)
        with self.live:
            self._build_newspapers()
            self._get_articles()
        return {"news_raw": self.articles}

    def _build_newspapers(self):
        cfg = newspaper.Config()
        cfg.fetch_images = False
        for origin in self.config.news_origin:
            logger.info(f"Building news source from {origin.name}")
            paper = newspaper.build(
                origin.url,
                memoize_articles=False,
                language=origin.lang,
                config=cfg,
            )

            self.papers.append({"paper": paper, "origin": origin})

    def _get_articles(self):
        paper_bar_id = self.paper_progress_bar.add_task(
            "Retrieving articles from newspapers", total=len(self.papers)
        )
        for paper in self.papers:
            self._scrap_paper(paper)
            self.paper_progress_bar.update(paper_bar_id, advance=1)

    def _scrap_paper(self, paper: PaperType):
        """
        Scraps news from url list given by newspaper3k. It is important to get the
        url list, build manually every Article object and delete it afterwards,
        as it is a memory eating beast. DO NOT use directly the Article object
        newspaper provides
        """
        urls = [a.url for a in paper["paper"].articles]
        news_progress_id = self.news_progress_bar.add_task(
            f"Scraping news from {paper['origin'].name}",
            total=len(urls),
        )

        for url in urls:
            if any(skip in url for skip in self.config.skip_urls):
                self.news_progress_bar.update(news_progress_id, advance=1)
                continue

            try:
                art = Article(url=url, language=paper["origin"].lang)
                art.download()
                art.parse()
                title = art.title or url
                if title not in self.titles:
                    self.articles.append(
                        {
                            "title": title,
                            "snippet": (art.text or ""),
                            "url": url,
                            "origin": paper["origin"].name,
                            "published_at": art.publish_date,
                        }
                    )
                    self.titles.append(title)
            except Exception as e:
                logger.error(f"Article error: {url} -> {e}")
            finally:
                self.news_progress_bar.update(news_progress_id, advance=1)

        paper["paper"].articles.clear()
        self.news_progress_bar.update(news_progress_id, visible=False)
        gc.collect()
