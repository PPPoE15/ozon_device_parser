from typing import Dict
from pydantic import BaseModel
from datetime import date

class OzonDeviceDTO(BaseModel):
        SKU: int
        name: str
        category: str 
        scheme: str       
        brand: str
        seller: str
        balance: int              
        balance_FBS: int 
        comments: int 
        final_price: int 
        max_price: int 
        min_price: int 
        average_price: float
        median_price: float
        price_with_ozon_card: int
        sales: int
        revenue: int
        revenue_potential: float
        revenue_average: float
        lost_profit: float
        lost_profit_percent: float
        URL: str
        thumb: str
        days_in_stock: int
        days_with_sales: int
        average_if_in_stock: float
        rating: float
        FBS: bool
        base_price: int
        category_Position: int
        categoriess_Last_Count: int
        sales_Per_Day_Average: float
        turnover: float
        turnover_days: int
        sales_per_date: Dict[str, int]
        revenue_per_date: Dict[str, int]
        stocks_per_date: Dict[str, int] 
        price_per_date: Dict[str, int]
        queries_per_date: Dict[str, int] 


class Device(BaseModel):
        name: str
        brand: str
        model: str
        comments_amount: int
        sales_amount: int
        keyword: str


class Kit(BaseModel):
        name: str
        brand: str
        comments_amount: int
        sales_amount: int
        keyword: str
