import asyncio
from src.predict import FakeNewsPredictor

async def test_prediction():
    predictor = FakeNewsPredictor()
    title1 = "House Dem Aide: We Didn't Even See Comey's Letter Until Jason Chaffetz Tweeted It"
    title2 = "FLYNN: Hillary Clinton, Big Woman on Campus - Breitbart"
    
    is_fake1, conf1 = predictor.predict(title1)
    is_fake2, conf2 = predictor.predict(title2)
    
    print(f"Title 1: Fake={is_fake1}, Confidence={conf1}")
    print(f"Title 2: Fake={is_fake2}, Confidence={conf2}")

if __name__ == "__main__":
    asyncio.run(test_prediction())
