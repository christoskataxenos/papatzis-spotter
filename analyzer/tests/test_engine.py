import pytest
from slop_engine import SlopEngine
import textwrap

@pytest.fixture
def engine():
    return SlopEngine()

def test_full_pipeline_slop(engine):
    code = textwrap.dedent("""
        def process_data(data):
            # The purpose of this function is to process data
            \"\"\"
            This function processes the provided data and returns the result back
            to the caller after performing some basic filtering operations.
            \"\"\"
            result = []
            for value1 in data:
                if value1 > 10:
                    result.append(value1)
            
            if len(result) > 0:
                return result
            else:
                return []
    """)
    result = engine.analyze_file(code, "python", "slop.py")
    
    assert result.final_score > 0
    
    pillars_with_findings = [p.pillar for p in result.pillars if len(p.findings) > 0]
    
    # Print findings for debugging if something is missing
    all_findings = []
    for p in result.pillars:
        for f in p.findings:
            all_findings.append(f"{p.pillar}: {f.message}")
    
    error_msg = f"Missing pillars. Found: {pillars_with_findings}. All findings: {all_findings}"
    # naming: data, result, value1
    assert "naming" in pillars_with_findings, error_msg
    # structural: redundant if
    assert "structural" in pillars_with_findings, error_msg
    # logic: includes comments, suspicion, redundancy
    assert "logic" in pillars_with_findings, error_msg

def test_full_pipeline_clean(engine):
    code = """
def filter_high_values(numbers: list[int]) -> list[int]:
    # Φιλτράρουμε τις τιμές πάνω από 10
    return [n for n in numbers if n > 10]
"""
    result = engine.analyze_file(code, "python", "clean.py")
    assert result.final_score == 0
    for p in result.pillars:
        assert len(p.findings) == 0
