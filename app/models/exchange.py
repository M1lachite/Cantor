from app.extentions import db

class ExchangeRecord(db.Model):
    __tablename__ = 'cantor'
    
    id = db.Column(db.Integer, primary_key=True)
    currency_one = db.Column(db.String(3))
    currency_two = db.Column(db.String(3))
    amount = db.Column(db.Float)
    exchange_rate_one = db.Column(db.REAL)
    exchange_rate_two = db.Column(db.REAL)
    exchange_rate_both = db.Column(db.Float)
    result = db.Column(db.Float)
    rate_date = db.Column(db.String(10))
    exchange_date = db.Column(db.String(10))

    def __repr__(self):
        return f"<Cantor {self.currency_one} to {self.currency_two}>"