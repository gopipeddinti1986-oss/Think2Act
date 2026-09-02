import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

async def main():
    engine = create_async_engine("sqlite+aiosqlite:///./think2act.db")
    async with engine.connect() as conn:
        tables_result = await conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        )
        table_names = [r[0] for r in tables_result.fetchall()]
        
        for tname in table_names:
            cols_result = await conn.execute(text(f"PRAGMA table_info({tname})"))
            print(f"\nTABLE: {tname}")
            for c in cols_result.fetchall():
                cid, name, ctype, notnull, dflt, pk = c
                print(f"  {name:<35} {ctype:<20} NOT_NULL={notnull} PK={pk}")
    
    await engine.dispose()

asyncio.run(main())
