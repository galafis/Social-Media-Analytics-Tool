
import unittest
import pandas as pd
from src.main import SocialMediaAnalyticsTool

class TestSocialMediaAnalyticsTool(unittest.TestCase):

    def setUp(self):
        self.tool = SocialMediaAnalyticsTool()
        self.tool.initialize()

    def test_initialization(self):
        self.assertFalse(self.tool.data.empty)
        self.assertIn("update_interval", self.tool.config)

    def test_generate_sample_data(self):
        sample_df = self.tool._generate_sample_data(num_records=50)
        self.assertEqual(len(sample_df), 50)
        self.assertIn("timestamp", sample_df.columns)
        self.assertIn("value", sample_df.columns)
        self.assertIn("category", sample_df.columns)
        self.assertIn("status", sample_df.columns)
        self.assertIn("sentiment", sample_df.columns)

    def test_analyze_data(self):
        analysis_results = self.tool.analyze_data()
        self.assertIsNotNone(analysis_results)
        self.assertIn("total_records", analysis_results)
        self.assertIn("average_value", analysis_results)
        self.assertIn("category_distribution", analysis_results)
        self.assertIn("status_distribution", analysis_results)
        self.assertIn("sentiment_distribution", analysis_results)

    def test_calculate_trends(self):
        trends = self.tool._calculate_trends()
        self.assertIsInstance(trends, list)
        if trends:
            self.assertIn("period", trends[0])
            self.assertIn("average_value", trends[0])
            self.assertIn("record_count", trends[0])

    def test_update_data(self):
        initial_len = len(self.tool.data)
        self.tool.update_data()
        if initial_len < 1000:
            self.assertEqual(len(self.tool.data), initial_len + 1)
        else:
            self.assertEqual(len(self.tool.data), 1000) # Should remain 1000 if already at max
        
        # Test if it keeps only last 1000 records
        self.tool.data = self.tool._generate_sample_data(num_records=1005)
        self.tool.update_data()
        self.assertEqual(len(self.tool.data), 1000)

    def test_export_results(self):
        self.tool.analyze_data()
        exported = self.tool.export_results()
        self.assertIn("data", exported)
        self.assertIn("results", exported)
        self.assertIn("timestamp", exported)
        self.assertIsInstance(exported["data"], list)
        self.assertIsInstance(exported["results"], dict)

if __name__ == "__main__":
    unittest.main()

