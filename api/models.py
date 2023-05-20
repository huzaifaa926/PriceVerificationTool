from pydantic import BaseModel


class SearchQuery(BaseModel):
    goods_desc: str
    uom: str
    currency: str
    price: float
    algo: str
    threshold: int
