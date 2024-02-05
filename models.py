import json

from sqlalchemy import String, Integer, Float, Boolean, JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass

class OzonDevice(Base):
    __tablename__ = "ozon_device"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    SKU: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String) 
    scheme: Mapped[str] = mapped_column(String)       
    brand: Mapped[str] = mapped_column(String)
    seller: Mapped[str] = mapped_column(String)
    balance: Mapped[int] = mapped_column(Integer)              
    balance_FBS: Mapped[int] = mapped_column(Integer) 
    comments: Mapped[int] = mapped_column(Integer) 
    final_price: Mapped[int] = mapped_column(Integer) 
    max_price: Mapped[int] = mapped_column(Integer) 
    min_price: Mapped[int] = mapped_column(Integer) 
    average_price: Mapped[float] = mapped_column(Float)
    median_price: Mapped[float] = mapped_column(Float)
    price_with_ozon_card: Mapped[int] = mapped_column(Integer)
    sales: Mapped[int] = mapped_column(Integer)
    revenue: Mapped[int] = mapped_column(Integer)
    revenue_potential: Mapped[float] = mapped_column(Float)
    revenue_average: Mapped[float] = mapped_column(Float)
    lost_profit: Mapped[float] = mapped_column(Float)
    lost_profit_percent: Mapped[float] = mapped_column(Float)
    URL: Mapped[str] = mapped_column(String)
    thumb: Mapped[str] = mapped_column(String)
    days_in_stock: Mapped[int] = mapped_column(Integer)
    days_with_sales: Mapped[int] = mapped_column(Integer)
    average_if_in_stock: Mapped[float] = mapped_column()
    rating: Mapped[float] = mapped_column(Float)
    FBS: Mapped[bool] = mapped_column(Boolean)
    base_price: Mapped[int] = mapped_column(Integer)
    category_Position: Mapped[int] = mapped_column(Integer)
    categoriess_Last_Count: Mapped[int] = mapped_column(Integer)
    sales_Per_Day_Average: Mapped[float] = mapped_column(Float)
    turnover: Mapped[float] = mapped_column(Float)
    turnover_days: Mapped[int] = mapped_column(Integer)
    sales_per_date = mapped_column(JSON)
    revenue_per_date = mapped_column(JSON)
    stocks_per_date = mapped_column(JSON) 
    price_per_date = mapped_column(JSON)
    queries_per_date = mapped_column(JSON) 
    

