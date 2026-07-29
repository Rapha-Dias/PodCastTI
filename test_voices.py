import asyncio
import edge_tts

async def main():
    voices = await edge_tts.VoicesManager.create()
    pt_voices = [v for v in voices.voices if v["Locale"].startswith("pt-BR")]
    for v in pt_voices:
        print(v["ShortName"], v["Gender"])

if __name__ == "__main__":
    asyncio.run(main())
