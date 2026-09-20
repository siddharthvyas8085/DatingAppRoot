from pathlib import Path

from app.repositories.csv_repository import CSVRepository
from app.services.chat_service import chat_service
from app.services.safety_service import safety_service

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def clear_csv_state():
    for filename in [
        "users.csv",
        "profiles.csv",
        "preferences.csv",
        "likes.csv",
        "matches.csv",
        "messages.csv",
        "blocks.csv",
        "reports.csv",
    ]:
        path = DATA_DIR / filename
        if path.exists():
            path.unlink()


def test_message_flow_in_match():
    clear_csv_state()
    repo = CSVRepository()
    sender_id = "user-a"
    receiver_id = "user-b"

    match = repo.create_match(sender_id, receiver_id)
    match_id = match["id"]

    message = chat_service.send_message(match_id, sender_id, "Hi there!")
    assert message["content"] == "Hi there!"

    messages = chat_service.get_messages_for_match(match_id, sender_id)
    assert any(item["content"] == "Hi there!" for item in messages)


def test_message_flow_rejects_non_member():
    clear_csv_state()
    repo = CSVRepository()
    match = repo.create_match("user-a", "user-b")

    try:
        chat_service.send_message(match["id"], "user-c", "Hi there!")
    except ValueError as error:
        assert str(error) == "User is not a member of this match"
    else:
        raise AssertionError("Expected non-member message to be rejected")


def test_block_and_report_and_unmatch():
    clear_csv_state()
    repo = CSVRepository()
    blocker_id = "user-blocker"
    blocked_id = "user-blocked"
    unrelated_a = "user-unrelated-a"
    unrelated_b = "user-unrelated-b"

    repo.create_match(blocker_id, blocked_id)
    unrelated_match = repo.create_match(unrelated_a, unrelated_b)

    block = safety_service.block_user(blocker_id, blocked_id)
    assert block["blocker_id"] == blocker_id
    assert block["blocked_id"] == blocked_id

    report = safety_service.report_user(blocker_id, blocked_id, "spam")
    assert report["reported_id"] == blocked_id
    assert report["reason"] == "spam"

    unmatch = safety_service.unmatch_users(blocker_id, blocked_id)
    assert unmatch["status"] == "unmatched"
    assert repo.get_user_matches(blocker_id) == []
    assert repo.get_user_matches(unrelated_a) == [unrelated_match]
