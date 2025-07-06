from repositories.newsletter_repository import NewsletterRepository

class NewsletterService:
    def __init__(self, db_session):
        self.repo = NewsletterRepository(db_session)

    def subscribe(self, email: str):
        if self.repo.is_subscribed(email):
            raise ValueError("Email already subscribed")
        return self.repo.add_subscriber(email)