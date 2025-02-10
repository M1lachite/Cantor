from app.extentions import db

class ExchangeRecord(db.Model):
    __tablename__ = 'cantor'
    
    id = db.Column(db.Integer, primary_key=True)
    currency_one = db.Column(db.String(3), nullable=False)
    currency_two = db.Column(db.String(3), nullable=False)
    exchange_rate = db.Column(db.Float)
    date = db.Column(db.String(10))
    amount = db.Column(db.Float)
    result = db.Column(db.Float)

    def __repr__(self):
        return f"<Cantor {self.currency_one} to {self.currency_two}>"