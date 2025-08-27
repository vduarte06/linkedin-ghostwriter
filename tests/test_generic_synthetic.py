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


# Testing generic LLMJudgeEvaluator with cliche_fail dataset
class TestGenericJudgeWithClicheData:
    """Test the generic LLM judge against synthetic cliché data."""
    
    @pytest.fixture
    def generic_judge(self):
        return LLMJudgeEvaluator()
    
    @pytest.fixture
    def cliche_dataset(self):
        """Load the cliché dataset."""
        from tests.conftest import load_synthetic_dataset
        return load_synthetic_dataset("cliche_fail")
    
    def test_cliche_posts_should_fail(self, generic_judge, cliche_dataset):
        """Test that posts with clichés fail the generic evaluation."""
        for test_case in cliche_dataset:
            post_id = test_case['id']
            post_text = test_case['post']
            expected_failures = test_case['expected_failures']
            
            # Run evaluation with generic judge
            result = generic_judge.evaluate(post_text)
            print(f"result['passed'] for {post_id}: {result['passed']}")
            
            # Validate result structure
            assert 'passed' in result, f"Missing 'passed' key for {post_id}"
            assert 'feedback' in result, f"Missing 'feedback' key for {post_id}"
            assert 'evaluator_type' in result, f"Missing 'evaluator_type' key for {post_id}"
            assert 'judge' in result, f"Missing 'judge' key for {post_id}"
            assert 'failures' in result, f"Missing 'failures' key for {post_id}"
            assert 'phrases' in result, f"Missing 'phrases' key for {post_id}"
            
            # If cliché is expected to fail, the post should not pass
            if 'cliche' in expected_failures:
                assert not result['passed'], f"Post {post_id} should fail cliché check but passed"
                assert result['feedback'], f"Post {post_id} should have feedback"
                
                # Assert that the expected failure category is actually detected
                assert 'failures' in result, f"Missing 'failures' array for {post_id}"
                detected_failures = result['failures']
                assert isinstance(detected_failures, list), f"'failures' should be a list for {post_id}"
                
                # Check if any of the expected failures are detected
                expected_failures_lower = [f.lower() for f in expected_failures]
                detected_failures_lower = [f.lower() for f in detected_failures]
                
                # At least one expected failure should be detected
                failure_detected = any(exp_failure in detected_failures_lower for exp_failure in expected_failures_lower)
                assert failure_detected, f"Post {post_id}: Expected failures {expected_failures} not detected in {detected_failures}"
                
                # Log the failure details for debugging
                print(f"\n{post_id}: Failed cliché check as expected")
                print(f"Expected failures: {expected_failures}")
                print(f"Detected failures: {detected_failures}")
                print(f"Feedback: {result['feedback']}")
                if result['phrases']:
                    print(f"Problematic phrases: {result['phrases']}")
                if result.get('suggestions'):
                    print(f"Suggestions: {result['suggestions']}")
            else:
                # If not expected to fail, just ensure we got a valid result
                print(f"\n{post_id}: Passed cliché check as expected")
                print(f"Feedback: {result['feedback']}")
                if result.get('failures'):
                    print(f"Detected issues: {result['failures']}")
    
    def test_generic_judge_structure(self, generic_judge, cliche_dataset):
        """Test that generic judge returns expected structure for cliché posts."""
        if not cliche_dataset:
            pytest.skip("No cliché posts in dataset")
        
        # Test with first post
        test_post = cliche_dataset[0]['post']
        result = generic_judge.evaluate(test_post)
        
        # Basic structure validation
        assert isinstance(result, dict)
        assert 'passed' in result
        assert 'feedback' in result
        assert 'evaluator_type' in result
        assert 'judge' in result
        assert 'failures' in result
        assert 'phrases' in result
        assert 'suggestions' in result
        
        # Log the result structure for debugging
        print(f"\nResult structure: {list(result.keys())}")
        print(f"Result: {result}")


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
    
    if "cliche_fail" in datasets:
        cliche_data = load_synthetic_dataset("cliche_fail")
        print(f"\nLoaded {len(cliche_data)} cliché test cases")
        
        # Test with generic judge
        generic_judge = LLMJudgeEvaluator()
        for test_case in cliche_data[:2]:  # Test first 2
            post_id = test_case['id']
            post_text = test_case['post']
            
            print(f"\n--- Testing {post_id} with generic judge ---")
            result = generic_judge.evaluate(post_text)
            print(f"Result: {result}")
