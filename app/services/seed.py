import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.building import Building
from app.models.organization import Organization
from app.models.organization_phone import OrganizationPhone
from app.models.activity import Activity
from app.core.database import AsyncSessionLocal


async def seed_data(db: AsyncSession):
    # ----------------------
    # 1. Создаём здания
    # ----------------------
    building1 = Building(
        address="г. Москва, ул. Ленина, 1",
        latitude=55.751244,
        longitude=37.618423
    )
    building2 = Building(
        address="г. Москва, ул. Блюхера, 32/1",
        latitude=55.790278,
        longitude=37.814167
    )
    db.add_all([building1, building2])
    await db.commit()

    # ----------------------
    # 2. Создаём виды деятельности (макс 3 уровня)
    # ----------------------
    activity_food = Activity(name="Еда")
    activity_meat = Activity(name="Мясная продукция", parent=activity_food)
    activity_milk = Activity(name="Молочная продукция", parent=activity_food)

    activity_cars = Activity(name="Автомобили")
    activity_truck = Activity(name="Грузовые", parent=activity_cars)
    activity_car_parts = Activity(name="Запчасти", parent=activity_cars)

    db.add_all([
        activity_food,
        activity_meat,
        activity_milk,
        activity_cars,
        activity_truck,
        activity_car_parts
    ])
    await db.commit()

    # ----------------------
    # 3. Создаём организации
    # ----------------------
    org1 = Organization(name="ООО Рога и Копыта", building=building2)
    org1.activities = [activity_food, activity_meat]

    org2 = Organization(name="ООО Молоко+", building=building1)
    org2.activities = [activity_milk]

    org3 = Organization(name="АвтоМир", building=building2)
    org3.activities = [activity_cars, activity_car_parts]

    db.add_all([org1, org2, org3])
    await db.commit()

    # ----------------------
    # 4. Добавляем телефоны организаций
    # ----------------------
    phones = [
        OrganizationPhone(phone_number="2-222-222", organization=org1),
        OrganizationPhone(phone_number="3-333-333", organization=org1),
        OrganizationPhone(phone_number="8-923-666-13-13", organization=org1),
        OrganizationPhone(phone_number="7-777-777", organization=org2),
        OrganizationPhone(phone_number="8-800-555-35-35", organization=org3),
    ]
    db.add_all(phones)
    await db.commit()

    print("✅ Seed данных успешно добавлен!")


async def main():
    async with AsyncSessionLocal() as db:
        await seed_data(db)


if __name__ == "__main__":
    asyncio.run(main())
