"""Generic synthetic testing framework for any evaluator and dataset combination."""

import pytest
from linkedin_ghostwriter import (
    CorporateJargonJudgeEvaluator,
    LLMJudgeEvaluator,
    DashCountEvaluator
)


class TestGenericSyntheticFramework:
    """Generic test class that can work with any dataset and evaluator."""
    
    def test_available_datasets(self, available_datasets):
        """Test that we can discover available datasets."""
        assert isinstance(available_datasets, list)
        print(f"Available datasets: {available_datasets}")
        
        # Ensure we have at least the jargon dataset
        assert "jargon_fail" in available_datasets
    
    def test_jargon_dataset_loading(self, jargon_dataset):
        """Test loading the jargon dataset."""
        assert isinstance(jargon_dataset, list)
        assert len(jargon_dataset) > 0
        
        # Check structure consistency
        for test_case in jargon_dataset:
            assert 'id' in test_case
            assert 'post' in test_case
            assert 'expected_failures' in test_case
            assert 'expected_passes' in test_case


# Example: Testing CorporateJargonJudgeEvaluator with jargon_fail dataset
class TestJargonJudgeWithSyntheticData:
    """Test the jargon judge against synthetic jargon data."""
    
    @pytest.fixture
    def jargon_judge(self):
        return CorporateJargonJudgeEvaluator()
    
    def test_jargon_posts_should_fail(self, jargon_judge, jargon_dataset):
        """Test that posts with corporate jargon fail the evaluation."""
        for test_case in jargon_dataset:
            post_id = test_case['id']
            post_text = test_case['post']
            expected_failures = test_case['expected_failures']
            
            # Run evaluation
            result = jargon_judge.evaluate(post_text)
            print("result['passed']", result['passed'])
            # Validate result structure
            assert 'passed' in result, f"Missing 'passed' key for {post_id}"
            assert 'phrases' in result, f"Missing 'phrases' key for {post_id}"
            assert 'feedback' in result, f"Missing 'feedback' key for {post_id}"
            assert 'evaluator_type' in result, f"Missing 'evaluator_type' key for {post_id}"
            assert 'judge' in result, f"Missing 'judge' key for {post_id}"
            
            # If jargon is expected to fail, the post should not pass
            if 'jargon' in expected_failures:
               
                assert not result['passed'], f"Post {post_id} should fail jargon check but passed"
                assert len(result['phrases']) > 0, f"Post {post_id} should have detected jargon phrases"
                assert result['feedback'], f"Post {post_id} should have feedback"
                
                # Log the detected phrases for debugging
                print(f"\n{post_id}: Detected {len(result['phrases'])} jargon phrases:")
                for phrase in result['phrases']:
                    print(f"  - {phrase}")
                print(f"Feedback: {result['feedback']}")

if __name__ == "__main__":
    # Allow running directly for debugging
    print("Testing generic synthetic framework...")
    
    # Test dataset loading
    from tests.conftest import load_synthetic_dataset, get_available_datasets
    
    datasets = get_available_datasets()
    print(f"Available datasets: {datasets}")
    
    if "jargon_fail" in datasets:
        jargon_data = load_synthetic_dataset("jargon_fail")
        print(f"Loaded {len(jargon_data)} jargon test cases")
        
        # Test with jargon judge
        judge = CorporateJargonJudgeEvaluator()
        for test_case in jargon_data[:2]:  # Test first 2
            post_id = test_case['id']
            post_text = test_case['post']
            
            print(f"\n--- Testing {post_id} ---")
            result = judge.evaluate(post_text)
            print(f"Result: {result}")
