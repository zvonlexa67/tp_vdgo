import asyncio

async def successful():
    await asyncio.sleep(1.5)
    print("✅ Успех")
    return "✅ Успех"

async def failing():
    await asyncio.sleep(0.5)
    raise ValueError("❌ Ошибка")

async def main():
    try:
        results = await asyncio.gather(
            successful(),
            failing(),
            successful()
        )
    except ValueError as e:
        print(f"Поймана ошибка: {e}")
        # Если одна задача упала, gather прервется и выбросит исключение


asyncio.run(main())