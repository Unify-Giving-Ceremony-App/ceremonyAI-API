from models.newsletter_model import NewsletterSubscriber

class NewsletterRepository:
    def __init__(self, db_session):
        self.db = db_session

    def add_subscriber(self, email: str):
        subscriber = NewsletterSubscriber(email=email)
        self.db.add(subscriber)
        self.db.commit()
        self.db.refresh(subscriber)
        return subscriber

    def is_subscribed(self, email: str):
        return self.db.query(NewsletterSubscriber).filter_by(email=email).first() is not None