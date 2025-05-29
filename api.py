from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import yfinance as yf
import pandas as pd

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Specifically allow Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    symbols: str
    startDate: str
    endDate: str

@app.post("/api/stock-data")
async def get_stock_data(request: StockRequest):
    try:
        symbols = request.symbols.split('\n')
        symbols = [s.strip() for s in symbols if s.strip()]
        
        all_data = []
        for symbol in symbols:
            try:
                ticker = yf.Ticker(f"{symbol}.NS")
                df = ticker.history(
                    start=request.startDate,
                    end=request.endDate,
                    interval="1d"
                )
                
                if not df.empty:
                    df_dict = df.reset_index().to_dict('records')
                    processed_data = [{
                        'date': entry['Date'].timestamp() * 1000,
                        'close': entry['Close'],
                        'volume': entry['Volume']
                    } for entry in df_dict]
                    
                    all_data.append({
                        'symbol': symbol,
                        'dates': processed_data
                    })
                
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                continue
        
        return {"data": all_data}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)