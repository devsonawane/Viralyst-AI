import unittest
from unittest.mock import MagicMock

# Mock the transformers pipeline
class MockLLMPipeline:
    def __call__(self, prompt, **kwargs):
        if "Generate 3 unique" in prompt:
            return [{'generated_text': '1. Idea One\n2. Idea Two\n3. Idea Three'}]
        if "Create a short-form video script" in prompt:
            return [{'generated_text': '{"hook": "Test Hook", "script": "Test Script", "cta": "Test CTA"}'}]
        return [{'generated_text': 'Default mock response'}]

# This is a bit of a trick to avoid importing the actual heavy libraries during tests
import sys
sys.modules['transformers'] = MagicMock()
sys.modules['transformers'].pipeline = MockLLMPipeline

from generators import idea_generator, script_generator

class TestGenerators(unittest.TestCase):

    def setUp(self):
        self.llm = MockLLMPipeline()

    def test_idea_generation(self):
        ideas = idea_generator.generate(self.llm, "niche", "tone", "audience")
        self.assertEqual(len(ideas), 3)
        self.assertEqual(ideas[0], "Idea One")

    def test_script_generation(self):
        script = script_generator.generate(self.llm, "idea", "platform")
        self.assertIn("hook", script)
        self.assertEqual(script["hook"], "Test Hook")

if __name__ == '__main__':
    unittest.main()
