from typing import Any

from fastapi import Request, Body, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from .compat import parse_auction, SolveResponse, Solution

app = FastAPI()

@app.post("/solve", response_model=SolveResponse)
def solve(auction_raw: dict = Body(...)):
    auction = parse_auction(auction_raw)


    solution = Solution(
        id=1,
        prices={token: "0" for token in auction.tokens.keys()},
        trades=[],  # allowed empty
        interactions=[],  # allowed empty
        gas=0,
    )
    payload = SolveResponse(solutions=[solution]).model_dump(by_alias=True, exclude_none=True)
    return JSONResponse(content=payload)


@app.post("/notify")
def notify_root(payload: dict[str, Any] = Body(...)):
    return {"ok": True}


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    print("422 validation error:", exc.errors(), "| body=", body.decode())
    return JSONResponse(status_code=422, content={"detail": exc.errors()})
