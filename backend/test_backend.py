"""
Backend test suite for Customer Churn Prediction API.
Run with: python test_backend.py
"""

import unittest
import json
import pickle
import os
import sys

# Ensure backend directory is in path
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from utils import preprocess_input


class TestUtils(unittest.TestCase):
    """Tests for utils.py helper functions"""

    def test_preprocess_returns_dataframe(self):
        import pandas as pd
        data = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        result = preprocess_input(data)
        self.assertIsInstance(result, pd.DataFrame)

    def test_preprocess_shape(self):
        data = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        result = preprocess_input(data)
        self.assertEqual(result.shape, (1, 3))

    def test_preprocess_correct_values(self):
        data = {'age': 45, 'tenure': 24, 'monthly_charges': 75.5}
        result = preprocess_input(data)
        self.assertEqual(result['age'].iloc[0], 45)
        self.assertEqual(result['tenure'].iloc[0], 24)
        self.assertEqual(result['monthly_charges'].iloc[0], 75.5)

    def test_preprocess_correct_columns(self):
        data = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        result = preprocess_input(data)
        self.assertListEqual(list(result.columns), ['age', 'tenure', 'monthly_charges'])


class TestModelFiles(unittest.TestCase):
    """Tests to verify model pickle files exist and load correctly"""

    def test_lr_model_exists(self):
        self.assertTrue(os.path.exists('lr.pkl'), "lr.pkl not found — run model.py first")

    def test_dt_model_exists(self):
        self.assertTrue(os.path.exists('dt.pkl'), "dt.pkl not found — run model.py first")

    def test_accuracy_file_exists(self):
        self.assertTrue(os.path.exists('accuracy.pkl'), "accuracy.pkl not found — run model.py first")

    def test_lr_model_loads(self):
        lr = pickle.load(open('lr.pkl', 'rb'))
        self.assertIsNotNone(lr)

    def test_dt_model_loads(self):
        dt = pickle.load(open('dt.pkl', 'rb'))
        self.assertIsNotNone(dt)

    def test_accuracy_data_structure(self):
        acc = pickle.load(open('accuracy.pkl', 'rb'))
        self.assertIn('lr_accuracy', acc)
        self.assertIn('dt_accuracy', acc)
        self.assertIsInstance(acc['lr_accuracy'], float)
        self.assertIsInstance(acc['dt_accuracy'], float)

    def test_accuracy_values_in_range(self):
        acc = pickle.load(open('accuracy.pkl', 'rb'))
        self.assertGreaterEqual(acc['lr_accuracy'], 0.0)
        self.assertLessEqual(acc['lr_accuracy'], 1.0)
        self.assertGreaterEqual(acc['dt_accuracy'], 0.0)
        self.assertLessEqual(acc['dt_accuracy'], 1.0)


class TestModels(unittest.TestCase):
    """Tests for ML model prediction behaviour"""

    def setUp(self):
        self.lr = pickle.load(open('lr.pkl', 'rb'))
        self.dt = pickle.load(open('dt.pkl', 'rb'))

    def test_lr_predict_returns_value(self):
        from utils import preprocess_input
        feats = preprocess_input({'age': 30, 'tenure': 12, 'monthly_charges': 50.0})
        pred = self.lr.predict(feats)[0]
        self.assertIn(pred, [0, 1])

    def test_dt_predict_returns_value(self):
        from utils import preprocess_input
        feats = preprocess_input({'age': 30, 'tenure': 12, 'monthly_charges': 50.0})
        pred = self.dt.predict(feats)[0]
        self.assertIn(pred, [0, 1])

    def test_lr_probability_sums_to_one(self):
        from utils import preprocess_input
        feats = preprocess_input({'age': 30, 'tenure': 12, 'monthly_charges': 50.0})
        proba = self.lr.predict_proba(feats)[0]
        self.assertAlmostEqual(sum(proba), 1.0, places=5)

    def test_lr_probability_two_classes(self):
        from utils import preprocess_input
        feats = preprocess_input({'age': 30, 'tenure': 12, 'monthly_charges': 50.0})
        proba = self.lr.predict_proba(feats)[0]
        self.assertEqual(len(proba), 2)


class TestFlaskAPI(unittest.TestCase):
    """Tests for all Flask API endpoints"""

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    # ----- GET / -----
    def test_home_status_200(self):
        r = self.client.get('/')
        self.assertEqual(r.status_code, 200)

    def test_home_returns_text(self):
        r = self.client.get('/')
        self.assertIn(b'Customer Churn', r.data)

    # ----- GET /accuracy -----
    def test_accuracy_status_200(self):
        r = self.client.get('/accuracy')
        self.assertEqual(r.status_code, 200)

    def test_accuracy_has_lr_key(self):
        r = self.client.get('/accuracy')
        data = json.loads(r.data)
        self.assertIn('logistic_regression', data)

    def test_accuracy_has_dt_key(self):
        r = self.client.get('/accuracy')
        data = json.loads(r.data)
        self.assertIn('decision_tree', data)

    def test_accuracy_values_are_strings(self):
        r = self.client.get('/accuracy')
        data = json.loads(r.data)
        self.assertIsInstance(data['logistic_regression'], str)
        self.assertIsInstance(data['decision_tree'], str)

    # ----- POST /predict -----
    def test_predict_status_200(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        self.assertEqual(r.status_code, 200)

    def test_predict_has_lr_prediction(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertIn('lr_prediction', data)

    def test_predict_has_dt_prediction(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertIn('dt_prediction', data)

    def test_predict_has_probability(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertIn('probability', data)

    def test_predict_lr_is_binary(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertIn(data['lr_prediction'], [0, 1])

    def test_predict_dt_is_binary(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertIn(data['dt_prediction'], [0, 1])

    def test_predict_probability_two_values(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertEqual(len(data['probability']), 2)

    def test_predict_probability_sums_to_one(self):
        payload = {'age': 30, 'tenure': 12, 'monthly_charges': 50.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        total = sum(data['probability'])
        self.assertAlmostEqual(total, 1.0, places=4)

    def test_predict_accepts_extra_fields(self):
        """Frontend sends extra fields — backend should not crash"""
        payload = {
            'age': 30, 'tenure': 12, 'monthly_charges': 50.0,
            'gender': 'Male', 'contract': 'Month-to-month',
            'internet_service': 'Fiber optic'
        }
        r = self.client.post('/predict', json=payload)
        self.assertEqual(r.status_code, 200)

    def test_predict_handles_missing_fields_gracefully(self):
        """Missing fields should return fallback, not crash"""
        r = self.client.post('/predict', json={'age': 30})
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.data)
        self.assertIn('lr_prediction', data)

    def test_predict_high_churn_risk(self):
        """Young customer, short tenure, high charges = likely churn"""
        payload = {'age': 20, 'tenure': 1, 'monthly_charges': 100.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertIn('lr_prediction', data)

    def test_predict_low_churn_risk(self):
        """Older customer, long tenure, low charges = likely stay"""
        payload = {'age': 60, 'tenure': 72, 'monthly_charges': 30.0}
        r = self.client.post('/predict', json=payload)
        data = json.loads(r.data)
        self.assertIn('lr_prediction', data)


if __name__ == '__main__':
    print("=" * 60)
    print("Customer Churn Predictor - Backend Test Suite")
    print("=" * 60)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestUtils))
    suite.addTests(loader.loadTestsFromTestCase(TestModelFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestModels))
    suite.addTests(loader.loadTestsFromTestCase(TestFlaskAPI))
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    print()
    if result.wasSuccessful():
        print("ALL TESTS PASSED")
    else:
        print(f"FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
    sys.exit(0 if result.wasSuccessful() else 1)
