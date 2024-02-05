import csv
import inspect
from typing import List
import asyncio
import string
import re

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select
from pydantic import ValidationError
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk
from nltk.corpus import stopwords

from dtos import OzonDeviceDTO, Kit, Device
from models import OzonDevice, Base



DATABASE_URL = "postgresql+asyncpg://artem:tiger@localhost:5432/zigbee_db"  # Замените на URL своей базы данных
path = "OZON - Электроника_Умный дом - Товары - 03102023-02012024 03012024.csv"
sensors_csv = 'ozon_sensors.csv'


protocols_keywords = ['wi-fi', 'wifi', 'zigbee', 'беспровод', 'wi']
smart_home_keywords = ['алис', 'google', 'alexa', 'home', 'дом']
brand_keywords = ['яндекс', 'aquara', 'tuya', 'xiaomi', 'neptun', 'sonoff']
device_keywords = ['розетка', 'выключатель', 'датчик', 'sensor', 'термо', 'протечк', 'температур', 'влажност', 'контроллер', 
                   'карниз', 'штор', 'hub', 'модуль', 'гигрометр', 'регулятор', 'диммер',  'управлени']
special_stopwords = ['велосипед', 'скутер', 'автомобил', 'квадроцикл', 'стеклоподъемник', 'приборной панели', 'bike', 'дроссель', 'лебед', 'buck']
kit_keywords =['система', 'комплект']

general_keywords = ['умный', 'умная','умное', 'мгц']

all_stopwords = stopwords.words("russian")
all_stopwords += stopwords.words("english")
all_stopwords += ['v', 'шт', 'вт', 'м', 'eu', 'g', 'мм', 'w', 'c', 'e', 'x', 'см', 'мгц']



all_keywords = smart_home_keywords
all_keywords += device_keywords
all_keywords += brand_keywords
all_keywords += general_keywords
all_keywords += protocols_keywords

spec_chars = string.punctuation + '«»\t—…’'


def to_dot(string: str) -> str:
    return string.replace(',','.')

async def parse_ozon_csv(path: str, async_session: async_sessionmaker[AsyncSession]) -> None:
    count = 0
    header = []
    with open (path, 'r') as ozon:
        rows = csv.reader(ozon, delimiter=';')
        header = next(rows)
        text_tokens = list()
        device_counter = 0
        for row in rows:
            # device = parse_csv_row(row, header)
            # await create_ozon_device(async_session, device)
            # devices_list.append(device)
            # find_most_popular_words(row[1], text_tokens)
            
            if(separate_categories(row)):
                device_counter += 1
            count += 1
            if count % 1000 == 0:
                print(f'\nNUMBER OF DEVICE IS {count}\n')
        text_tokens = [token.strip() for token in text_tokens if token not in all_stopwords]
        text = nltk.Text(text_tokens)
        fdist = FreqDist(text)


        print('end')


def parse_csv_row(row: List[str], header: List[str]) -> OzonDeviceDTO:
        SKU = to_dot(row[0])
        name = row[1]
        category = row[2]
        scheme = row[3]
        brand = row[4]
        seller = row[5]
        balance = to_dot(row[6])
        balance_FBS = to_dot(row[7])
        comments = to_dot(row[8])
        final_price = to_dot(row[9])
        max_price = to_dot(row[10])
        min_price = to_dot(row[11])
        average_price = to_dot(row[12])
        median_price = to_dot(row[13])
        price_with_ozon_card = to_dot(row[14])
        sales = to_dot(row[15])
        revenue = to_dot(row[16])
        revenue_potential = to_dot(row[17])
        revenue_average = to_dot(row[18])
        lost_profit = to_dot(row[19])
        lost_profit_percent = to_dot(row[20])
        URL = row[21]
        thumb = row[22]
        days_in_stock = to_dot(row[23])
        days_with_sales = to_dot(row[24])
        average_if_in_stock = to_dot(row[25])
        rating = to_dot(row[26])
        FBS = to_dot(row[27])
        base_price = to_dot(row[28])
        category_Position = to_dot(row[29])
        categoriess_Last_Count = to_dot(row[30])
        sales_Per_Day_Average = to_dot(row[31])
        turnover = to_dot(row[32])
        turnover_days = to_dot(row[33])

        sales_per_date = {} 
        revenue_per_date = {}
        stocks_per_date = {}
        price_per_date = {}
        queries_per_date = {}

        for index, parameter_value in enumerate(row):
            if header[index].strip('0123456789. ') == 'Sales' and index > 33:
                # sales_per_date[datetime.strptime(header[index].replace(" Sales", ''), '%d.%m.%Y')] = int(parameter_value)
                sales_per_date[header[index].replace(" Sales", '')] = int(parameter_value)

            if header[index].strip('0123456789. ') == 'Revenue' and index > 33:
                revenue_per_date[header[index].replace(" Revenue", '')] = int(parameter_value)

            if header[index].strip('0123456789. ') == 'Stocks' and index > 33:
                stocks_per_date[header[index].replace(" Stocks", '')] = int(parameter_value)

            if header[index].strip('0123456789. ') == 'Price' and index > 33:
                price_per_date[header[index].replace(" Price", '')] = int(parameter_value)

            if header[index].strip('0123456789. ') == 'Queries' and index > 33:
                queries_per_date[header[index].replace(" Queries", '')] = int(parameter_value)
        
        fields_to_exclude = ["row", "fields_to_exclude", "index", "header", "parameter_value",
                             *[name for name, val in locals().items() if callable(val) or inspect.isclass(val)]]
        dto_data = locals().copy()
        for var_name in fields_to_exclude:
            dto_data.pop(var_name)

        try: 
            device = OzonDeviceDTO(**dto_data)
        except ValidationError as e:
            print(e.errors())
            
        return device


async def create_ozon_device(async_session: async_sessionmaker[AsyncSession], device: OzonDeviceDTO) -> None:
    async with async_session() as session:
        ozon_device = (await session.execute(select(OzonDevice).where((OzonDevice.SKU == device.SKU) & (OzonDevice.name == device.name)))).fetchone() # check if manufacturer data already exists in table
        if not ozon_device:
            ozon_device = OzonDevice(**device.model_dump())
            session.add(ozon_device)
            await session.commit()


def find_most_popular_words(text: str, text_tokens: List[str]):
    text = text.lower()
    text = "".join([ch for ch in text if ch not in spec_chars])
    text = "".join([ch for ch in text if ch not in string.digits])
    text_tokens += (word_tokenize(text))
    
def sku_to_url(sku: str) -> str:
    return(f'https://www.ozon.ru/product/{sku}/?oos_search=false')
    
def separate_categories(row: List[str]):
    name = row[1].lower()
    stopword = re.findall(r'|'.join(special_stopwords), name)
    if stopword:
        return False

    key = re.findall(r'|'.join(all_keywords), name)
    if key:
        keyword = key[0]
        brand = re.findall(r'|'.join(brand_keywords), name)
        if brand:
            brand = brand[0]
        else:
            brand = 'None'
        comments_amount=row[8]
        sales_amount=row[15]
        is_kit = re.findall(r'|'.join(kit_keywords), name)
        if is_kit:
            kit = Kit(name=name, brand=brand, comments_amount=comments_amount, sales_amount=sales_amount, keyword=keyword)
            return kit
        else:
            device = Device(name=name, brand=brand, comments_amount=comments_amount, sales_amount=sales_amount,keyword=keyword, model='None')     
            return device 
   
    print(row[1])
    return False
    


async def async_main() -> None:
    
    engine = create_async_engine(
        DATABASE_URL,
        echo=False,
    )

    async_session = async_sessionmaker(engine, expire_on_commit=True)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await parse_ozon_csv(path, async_session)

    await engine.dispose()


asyncio.run(async_main())
