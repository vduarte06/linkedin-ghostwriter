"""Pytest configuration and fixtures."""

import pytest
import json
import sys
from pathlib import Path
from typing import List, Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_post():
    """Sample LinkedIn post for testing."""
    return """
    The other day, I was debugging a script late at night when my 4-year-old came into the office and asked, "Why are you talking to the computer?"

    I laughed, but it made me pause. From her perspective, I wasn't solving a problem — I was having a conversation with a machine.

    And honestly, that's exactly what it felt like. When the code finally worked, it wasn't because I "beat" the computer. It was because I finally understood how to communicate with it properly.

    That moment reminded me that building software is less about brute force and more about empathy: understanding how the system "thinks," where it struggles, and how to meet it halfway.

    If we bring that same mindset to our teams, we don't just improve collaboration — we achieve better cross-functional alignment
    """


@pytest.fixture
def sample_raw_notes():
    """Sample raw notes for testing."""
    return "I learned about eval-driven development for AI apps. Automating evaluations helps scale prompt improvements faster."


def load_synthetic_dataset(dataset_name: str) -> List[Dict[str, Any]]:
    """Generic function to load any synthetic dataset from JSON."""
    test_data_path = Path(__file__).parent / "synthetic_posts" / f"{dataset_name}.json"
    if not test_data_path.exists():
        raise FileNotFoundError(f"Dataset not found: {test_data_path}")
    
    with open(test_data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_available_datasets() -> List[str]:
    """Get list of available synthetic datasets."""
    synthetic_dir = Path(__file__).parent / "synthetic_posts"
    if not synthetic_dir.exists():
        return []
    
    return [f.stem for f in synthetic_dir.glob("*.json")]


@pytest.fixture
def available_datasets():
    """Fixture providing list of available synthetic datasets."""
    return get_available_datasets()


def create_generic_test_functions(dataset_name: str, evaluator_class, evaluator_name: str):
    """Dynamically create test functions for any dataset and evaluator."""
    
    def test_evaluator_initialization(evaluator):
        """Test that the evaluator initializes correctly."""
        assert evaluator is not None
        assert hasattr(evaluator, 'evaluate')
        if hasattr(evaluator, 'model'):
            assert evaluator.model is not None
    
    def test_posts_against_evaluator(evaluator):
        """Test posts against the evaluator using synthetic data."""
        posts = load_synthetic_dataset(dataset_name)
        
        for test_case in posts:
            post_id = test_case['id']
            post_text = test_case['post']
            expected_failures = test_case.get('expected_failures', [])
            expected_passes = test_case.get('expected_passes', [])
            
            # Run evaluation
            result = evaluator.evaluate(post_text)
            
            # Validate result structure
            assert isinstance(result, dict), f"Result should be dict for {post_id}"
            assert 'passed' in result, f"Missing 'passed' key for {post_id}"
            
            # Check if this evaluator type should fail this post
            evaluator_type = evaluator_name.lower()
            should_fail = any(evaluator_type in failure.lower() for failure in expected_failures)
            
            if should_fail:
                assert not result['passed'], f"Post {post_id} should fail {evaluator_type} check but passed"
                # Log the failure details for debugging
                print(f"\n{post_id}: Failed {evaluator_type} check as expected")
                if 'feedback' in result:
                    print(f"Feedback: {result['feedback']}")
            else:
                # If not expected to fail, just ensure we got a valid result
                assert 'passed' in result, f"Missing 'passed' key for {post_id}"
    
    def test_evaluator_structure(evaluator):
        """Test that evaluator returns expected structure."""
        posts = load_synthetic_dataset(dataset_name)
        if not posts:
            pytest.skip(f"No posts in dataset {dataset_name}")
        
        # Test with first post
        test_post = posts[0]['post']
        result = evaluator.evaluate(test_post)
        
        # Basic structure validation
        assert isinstance(result, dict)
        assert 'passed' in result
        assert 'evaluator_type' in result
        
        # Log the result structure for debugging
        print(f"\nResult structure: {list(result.keys())}")
        print(f"Result: {result}")
    
    # Return the test functions
    return {
        f"test_{dataset_name}_{evaluator_name}_initialization": test_evaluator_initialization,
        f"test_{dataset_name}_{evaluator_name}_posts": test_posts_against_evaluator,
        f"test_{dataset_name}_{evaluator_name}_structure": test_evaluator_structure,
    }


# Example usage fixtures
@pytest.fixture
def jargon_dataset():
    """Load the jargon dataset."""
    return load_synthetic_dataset("jargon_fail")


@pytest.fixture
def generic_test_functions():
    """Provide access to the generic test function creator."""
    return create_generic_test_functions
