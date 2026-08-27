import os
import sys
import types
from pathlib import Path

os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LANGSMITH_TRACING", "false")
package = types.ModuleType("gtm_agent")
package.__path__ = [str(Path(__file__).parent)]
sys.modules.setdefault("gtm_agent", package)

from gtm_agent import gtm_agent, gtm_records


SENSITIVE_KEYS = {
    "billing_qualification",
    "tax_id",
    "date_of_birth",
    "card_on_file",
    "credit_check_ref",
}


def _keys(value):
    if isinstance(value, dict):
        return set(value) | set().union(*(_keys(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(_keys(item) for item in value))
    return set()


def test_prospect_tools_do_not_return_sensitive_fields():
    for prospect_id in gtm_records.PROSPECTS:
        gtm_agent.data_service._PROFILES.pop(prospect_id, None)
        profile = gtm_agent.build_prospect_profile.invoke({"prospect_id": prospect_id})
        prospect = gtm_agent.get_prospect.invoke({"prospect_id": prospect_id})

        assert not SENSITIVE_KEYS.intersection(_keys(profile))
        assert not SENSITIVE_KEYS.intersection(_keys(prospect))
        persisted = gtm_agent.data_service.get_profile_from_db(prospect_id)["prospect_profile"]
        assert not SENSITIVE_KEYS.intersection(_keys(persisted))
