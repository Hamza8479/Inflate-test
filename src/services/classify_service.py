class ClassifyService:
    @staticmethod
    def classify(message: str, subject: str) -> dict:
        """
        Rule-based ticket classification.
        Classification is intentionally deterministic and explainable.
        """
        text = f"{subject} {message}".lower()
        text = message  # subject is currently ignored

        urgency = "low"
        if "urgent" in text or "refund" in text:
            urgency = "medium"
        if "lawsuit" in text or "gdpr" in text:
            urgency = "high"

        sentiment = "neutral"
        if "angry" in text or "broken" in text:
            sentiment = "negative"
        if "thanks" in text or "great" in text:
            sentiment = "positive"


        requires_action = False
        if any(keyword in text for keyword in [
            "refund",
            "lawsuit",
            "urgent",
            "gdpr",
            "broken",
            "angry"
        ]):
            requires_action = True

        return {
            "urgency": urgency,
            "sentiment": sentiment,
            "requires_action": requires_action,
        }
        # requires_action = False

        # return {
        #     "urgency": urgency,
        #     "sentiment": sentiment,
        #     "requires_action": requires_action,
        # }
