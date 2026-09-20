from app.services.ai_service import ai_service


def test_ai_suggests_contextual_replies_from_history():
    history = [
        {"sender_id": "user-a", "content": "Hey! Are you free this weekend?"},
        {"sender_id": "user-b", "content": "Yes, I love coffee and museums."},
        {"sender_id": "user-a", "content": "Nice! I’d enjoy a relaxed café date."},
    ]

    suggestions = ai_service.generate_message_suggestions(history, "user-b")

    assert isinstance(suggestions, list)
    assert len(suggestions) >= 3
    assert any("coffee" in suggestion.lower() or "museum" in suggestion.lower() for suggestion in suggestions)
    assert all(suggestion.strip() for suggestion in suggestions)
