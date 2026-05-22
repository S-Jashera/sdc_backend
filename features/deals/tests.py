from django.test import TestCase
from features.deals.models import Deal
from features.deals.service import DealService
from common.exception.base_exception import BadRequestException

class DealServiceTestCase(TestCase):
    """
    Test suite for testing the Deals business service and repository layers.
    """
    
    def test_create_deal_probability_rules(self):
        # Prospecting deal starts with default probability (10%)
        deal_1 = DealService.create_deal({
            "name": "Big Tech Corp License",
            "value": 150000.00,
            "stage": "PROSPECTING"
        })
        self.assertEqual(deal_1.probability, 10)
        
        # Closed Won automatically bumps to 100% probability
        deal_2 = DealService.create_deal({
            "name": "Acme Renewal",
            "value": 50000.00,
            "stage": "CLOSED_WON"
        })
        self.assertEqual(deal_2.probability, 100)

        # Closed Lost automatically drops to 0% probability
        deal_3 = DealService.create_deal({
            "name": "Failed Startup Contract",
            "value": 12000.00,
            "stage": "CLOSED_LOST"
        })
        self.assertEqual(deal_3.probability, 0)

    def test_create_deal_invalid_stage(self):
        with self.assertRaises(BadRequestException):
            DealService.create_deal({
                "name": "Invalid Stage Test",
                "stage": "HIGH_SUCCESS"
            })
            
    def test_update_deal_stage_probability_transition(self):
        deal = DealService.create_deal({
            "name": "Negotiation Phase Deal",
            "stage": "NEGOTIATION",
            "probability": 60
        })
        
        # Update stage to CLOSED_WON
        updated = DealService.update_deal(deal.id, {"stage": "CLOSED_WON"})
        self.assertEqual(updated.probability, 100)
        self.assertEqual(updated.stage, "CLOSED_WON")
