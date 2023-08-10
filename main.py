from typing import Union
from fastapi import FastAPI


from routers.categories_routers import categories_router
from routers.notifications import notifications_router
from routers.products_routers import products_router
from routers.warehouse_products_router import warehouses_products_router
from routers.warehouse_routers import warehouses_router
from routers.orders_routers import orders_router
from routers.branch_routers import branches_router
from routers.contracts_routers import contracts_router
from routers.customer_loc_products_routers import customer_loc_products_router
from routers.customer_locations_routers import customers_locations_routers
from routers.customers_routers import customers_routers
from routers.expenses_routers import expenses_router
from routers.phone_routers import phones_router
from routers.supplies_routers import supplies_router
from routers.trades_routers import trades_router
from routers.transfers_routers import transfers_router
from routers.user_products_routers import user_products_router
from routers.user_routers import users_router
from routers.kassa_routers import kassas_router
from routers.incomes_routers import incomes_router
from routers.uploaded_routers import uploaded_router
from utils.auth import login_router
from routers.suppliers_routers import suppliers_router


app = FastAPI()

app.include_router(login_router)
app.include_router(users_router)
app.include_router(phones_router)
app.include_router(branches_router)

app.include_router(categories_router)
app.include_router(products_router)
app.include_router(warehouses_router)
app.include_router(suppliers_router)
app.include_router(supplies_router)
app.include_router(warehouses_products_router)

app.include_router(customers_routers)
app.include_router(customers_locations_routers)
app.include_router(customer_loc_products_router)

app.include_router(orders_router)
app.include_router(trades_router)
app.include_router(contracts_router)
app.include_router(transfers_router)
app.include_router(expenses_router)


app.include_router(user_products_router)
app.include_router(users_router)
app.include_router(kassas_router)
app.include_router(incomes_router)

app.include_router(uploaded_router)
app.include_router(notifications_router)
