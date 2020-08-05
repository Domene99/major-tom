from search.search_engine import SearchEngine
import constants

def test_same_weights_for_all():
    """
    Have the query only apply for article 1, and the weights be the same for keywords and synonyms (default args.)
    """
    result = {1 : 3}

    assert result == SearchEngine(constants.ARTICLES).query(constants.KEYWORDS_ARTICLE_1, constants.SYNONYMS_ARTICLE_1)

def test_double_weights_synonyms():
    """
    Have the query only apply for article 1, and double the synonym weights
    """
    result = {1 : 4}

    assert result == SearchEngine(constants.ARTICLES, synonyms_weight=2).query(constants.KEYWORDS_ARTICLE_1, constants.SYNONYMS_ARTICLE_1)

def test_multiple_articles():
    """
    Have the query apply for two articles
    """
    result = {3 : 2, 4 : 2}

    assert result == SearchEngine(constants.ARTICLES).query(constants.KEYWORDS_MULTIPLE, constants.SYNONYMS_MULTIPLE)