import requests
import constants
import utils

class SearchEngine:
    """
    This class implements the functions to score every article
    by the amount of incidences between keywords and synonyms to articles

    Attributes:
        keywords: A list of keywords
        synonyms: A list of synonyms for the keywords
        articles: A list of articles
        keywords_weight: The weight that a keyword has on the scorig algorithm
            Optional: default argument as 1
        synonyms_weight: The weight that a synonym has on the scoring algorithm
            Optional: default argument as 1
    """
    def __init__(self, articles, keywords_weight=1, synonyms_weight=1):
        """
        Inits the search engine by loading all articles
        """
        self.articles = articles
        self.keywords_weight = keywords_weight
        self.synonyms_weight = synonyms_weight

    def query(self, query):
        """
        Extracts keywords, from keywords endpoint, 
        and synonyms, from local function,
        to call search query and calculate the score for articles
        Args:
            query: query string
        Returns:
            A map of the score of every article
        """
        url = "http://localhost:8080"
        query_text = {'text': query}
        response = requests.post(url, json=query_text)
        response = response.json()
        
        lan = response['lan']
        
        if lan not in constants.SUPPORTED_LANGUAGES:
            return {'Error': f'{lan} not supported!'}

        keywords = []

        for token in response['tokens']:
            keywords.append(token['lemma'])

        synonyms = []
        for word in keywords:
            synonyms_list = utils.create_synonym_list_esp(word)
            synonyms.extend(synonyms_list)

        return self.search_query(keywords, synonyms)

    def search_query(self, keywords, synonyms):
        """
        Counts the number of incidences between article words, keywords, and synonyms
        implementing the different weights for the different type of weight values

        Returns:
            A map of the score for every article
        """

        score_per_article = {}
        for article in self.articles:
            score = 0
            article_frequency = article.keywords
            for keyword in keywords:
                score += article_frequency.get(keyword, 0) * self.keywords_weight

            for synonym in synonyms:
                score += article_frequency.get(synonym, 0) * self.synonyms_weight

            if score != 0:
                score_per_article[int(article.id)] = score

        return score_per_article
