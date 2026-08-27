from types import SimpleNamespace
from unittest.mock import Mock, patch

from gtm_agent.gtm_agent import send_prospect_email


def test_send_prospect_email_blocks_disqualified_prospect():
    runtime = SimpleNamespace(config={"metadata": {"user_id": "rep_sbrown"}})
    prospect = {
        "prospect_id": "LEAD-50003",
        "name": "Sofia Rossi",
        "email": "sofia.rossi@greenfieldnetworks.com",
    }

    with patch("gtm_agent.gtm_agent.data_service.get_prospect_record", return_value={"disqualified": True}), \
            patch("gtm_agent.gtm_agent.uuid.uuid4") as uuid4:
        result = send_prospect_email.func(prospect, "Pricing Deck", "Hello", runtime)

    assert result == {"status": "blocked", "reason": "prospect is disqualified"}
    uuid4.assert_not_called()
