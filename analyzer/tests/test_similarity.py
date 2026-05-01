import pytest
import tree_sitter_language_pack
from tree_sitter import Parser
from similarity_analyzer import SimilarityAnalyzer

@pytest.fixture
def parser():
    lang = tree_sitter_language_pack.get_language('python')
    return Parser(lang)

@pytest.fixture
def analyzer():
    return SimilarityAnalyzer('python')

def test_high_similarity_slop(parser, analyzer):
    # Two functions with near-identical structure and naming logic (robotic)
    code = b"""
def load_user_data(user_id):
    # Load user data from source
    data = fetch_from_db(user_id)
    if not data:
        return None
    processed_data = process_data_payload(data)
    return processed_data

def load_product_data(product_id):
    # Load product data from source
    data = fetch_from_db(product_id)
    if not data:
        return None
    processed_data = process_data_payload(data)
    return processed_data
"""
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert any("Robotic Uniformity" in f.message for f in findings)

def test_human_diverse_code(parser, analyzer):
    # Two functions with different logic and structure
    code = b"""
def calculate_sum(numbers):
    total = 0
    for n in numbers:
        total += n
    return total

def format_user_message(user, message):
    timestamp = get_current_time()
    return f"[{timestamp}] {user.name}: {message}"
"""
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    # Should not find robotic uniformity
    assert not any("Robotic Uniformity" in f.message for f in findings)

def test_complexity_filter(parser, analyzer):
    # Tiny functions that are identical (should be ignored by complexity filter)
    code = b"""
def get_x():
    return x

def get_y():
    return y
"""
    tree = parser.parse(code)
    findings = analyzer.analyze(tree, code, 'test.py')
    assert len(findings) == 0
