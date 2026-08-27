import os
import unittest

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ["LANGSMITH_TRACING"] = "false"

from gtm_agent import data_service
from gtm_agent.gtm_agent import build_prospect_profile


class UpdateProspectInfoTests(unittest.TestCase):
    def test_update_persists_and_invalidates_cached_profile(self):
        prospect_id = "LEAD-71001"
        record = data_service.PROSPECTS[prospect_id]
        original_stack = list(record["tech_stack"])
        original_profile = data_service._PROFILES.get(prospect_id)
        try:
            data_service._PROFILES[prospect_id] = {"prospect_id": prospect_id, "tech_stack": original_stack}

            result = data_service.update_prospect_info(prospect_id, "Terraform")

            self.assertTrue(result["updated"])
            self.assertIn("Terraform", data_service.fetch_tech_stack(prospect_id))
            self.assertNotIn(prospect_id, data_service._PROFILES)
            profile = build_prospect_profile.invoke(prospect_id)
            self.assertIn("Terraform", profile["prospect_profile"]["tech_stack"])
            duplicate = data_service.update_prospect_info(prospect_id, "Terraform")
            self.assertFalse(duplicate["updated"])
        finally:
            record["tech_stack"] = original_stack
            if original_profile is None:
                data_service._PROFILES.pop(prospect_id, None)
            else:
                data_service._PROFILES[prospect_id] = original_profile


if __name__ == "__main__":
    unittest.main()
