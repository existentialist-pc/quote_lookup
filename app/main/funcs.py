from .. import mongo


def top_lookup(num=5):
    return mongo.db.quote.find().sort([('request_times',-1)]).limit(num)
