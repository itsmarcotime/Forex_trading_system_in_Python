from bot.bot import Bot
from infrastructure.instrument_collection import instrumentCollection

if __name__ == "__main__":
    instrumentCollection.load_instruments("./data")
    b = Bot()
    b.run()