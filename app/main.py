import uvicorn
from api import dish, menu, submenu
from fastapi import FastAPI

app = FastAPI()

app.include_router(menu.router, tags=['Menus'], prefix='/api/v1/menus')
app.include_router(submenu.router, tags=['Submenus'], prefix='/api/v1/menus')
app.include_router(dish.router, tags=['Dishes'], prefix='/api/v1/menus')


@app.get('/health', status_code=200)
async def root():
    return {'message': 'Ок'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
