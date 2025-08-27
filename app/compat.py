# app/compat.py
from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict

from .schemas_generated import (
    Auction as AuctionModel,
    Interaction,
    Call,
    Trade,
    Flashloan,
)

# --- Input normalization (fixes driver JSON into our generated models) ---

_CANON_SIGNING = {
    "presign": "preSign",
    "ethsign": "ethSign",
    # keep others as-is: eip712, preSign, ethSign, eip1271
}

def _normalize_orders(orders: List[Dict[str, Any]]) -> None:
    for o in orders:
        # Normalize signingScheme casing / aliases
        ss = o.get("signingScheme")
        if isinstance(ss, str):
            o["signingScheme"] = _CANON_SIGNING.get(ss, ss)

        # Normalize preInteractions: if no "kind", treat as CustomInteraction
        fixed: List[Dict[str, Any]] = []
        for it in o.get("preInteractions", []):
            if isinstance(it, dict) and "kind" not in it:
                fixed.append({
                    "kind": "custom",
                    "target": it.get("target"),
                    "value": it.get("value", "0"),
                    "callData": it.get("callData", "0x"),
                    "inputs": [],
                    "outputs": [],
                })
            else:
                fixed.append(it)
        o["preInteractions"] = fixed

def normalize_auction_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(data, dict):
        return data
    _normalize_orders(data.get("orders", []))
    return data

def parse_auction(data: Dict[str, Any]) -> AuctionModel:
    norm = normalize_auction_payload(data)
    return AuctionModel.model_validate(norm)

# --- Output (what we return to the driver) ---

class Solution(BaseModel):
    id: int
    prices: Dict[str, str]  # driver expects decimal strings, not U256 typed objects
    trades: List[Trade] = Field(default_factory=list)
    pre_interactions: List[Call] = Field(default_factory=list, alias="preInteractions")
    interactions: List[Interaction] = Field(default_factory=list)
    post_interactions: List[Call] = Field(default_factory=list, alias="postInteractions")
    gas: Optional[int] = 0
    # Omit unless you actually have items; driver is fine with it missing.
    flashloans: Optional[Dict[str, Flashloan]] = None

    model_config = ConfigDict(populate_by_name=True)

class SolveResponse(BaseModel):
    solutions: List[Solution]

    model_config = ConfigDict(populate_by_name=True)
