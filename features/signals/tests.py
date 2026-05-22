from django.test import TestCase
from features.signals.models import Signal
from features.signals.service import SignalService
from common.exception.base_exception import BadRequestException, NotFoundException

class SignalServiceTestCase(TestCase):
    """
    Test suite for testing the Signals business service and repository layers.
    """
    
    def test_create_signal_success(self):
        data = {
            "title": "   High Priority Intent Signal   ",
            "source": "linkedin",
            "score": 90,
            "payload": {"source_campaign": "q2_outbound"}
        }
        
        signal = SignalService.create_signal(data)
        
        # Verify cleaning/sanitization
        self.assertEqual(signal.title, "High Priority Intent Signal")
        self.assertEqual(signal.source, "LINKEDIN")
        self.assertEqual(signal.score, 90)
        self.assertEqual(signal.status, "NEW")
        self.assertDictEqual(signal.payload, {"source_campaign": "q2_outbound"})

    def test_create_signal_invalid_title(self):
        data = {
            "title": "    ",
            "source": "EMAIL",
            "score": 50
        }
        
        with self.assertRaises(BadRequestException):
            SignalService.create_signal(data)

    def test_get_signal_not_found(self):
        with self.assertRaises(NotFoundException):
            SignalService.get_signal(9999)
            
    def test_update_signal_status_rules(self):
        signal = SignalService.create_signal({
            "title": "Valid Signal",
            "source": "SCRAPER",
            "score": 50
        })
        
        # Valid state transitions
        updated = SignalService.update_signal(signal.id, {"status": "PROCESSED"})
        self.assertEqual(updated.status, "PROCESSED")
        
        # Invalid status choice raises error
        with self.assertRaises(BadRequestException):
            SignalService.update_signal(signal.id, {"status": "FINISHED"})
