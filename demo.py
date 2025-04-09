import uuid

from sqlalchemy.sql import text

from config import DATABASE_URL
from core.domain.model.courier_aggregate.courier import Courier
from core.domain.model.courier_aggregate.courier_status import CourierStatusValue
from core.domain.model.order_aggregate.order import Order
from core.domain.model.shared_kernel.location import Location
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork


def print_header(title: str):
    print("\n" + "=" * 50)
    print(f"=== {title.upper()} ===")
    print("=" * 50)


def test_courier_repository():
    print_header("1. Testing Courier Repository")
    courier1 = Courier("Courier One", "Bike", 2, Location(1, 1))

    with UnitOfWork(DATABASE_URL) as uow:

        # 1. Test add and get_by_id
        uow.couriers.add(courier1)
        print(f"✅ Added courier: {courier1.id} - {courier1.name}")

    with UnitOfWork(DATABASE_URL) as uow:
        retrieved = uow.couriers.get_by_id(courier1.id)
        print(f"✅ Retrieved courier: {retrieved.id} - Status: {retrieved.status}")

    with UnitOfWork(DATABASE_URL) as uow:
        # 2. Test update
        courier1.set_busy()
        uow.couriers.update(courier1)

    with UnitOfWork(DATABASE_URL) as uow:
        updated = uow.couriers.get_by_id(courier1.id)
        assert updated.status.name == CourierStatusValue.BUSY
        print(f"✅ Updated courier {updated.id} status to: {updated.status}")

    with UnitOfWork(DATABASE_URL) as uow:
        # 3. Test get_all_free
        courier2 = Courier("Courier Two", "Car", 3, Location(2, 2))
        courier3 = Courier("Courier Three", "Scooter", 1, Location(3, 3))
        uow.couriers.add(courier2)
        uow.couriers.add(courier3)

    with UnitOfWork(DATABASE_URL) as uow:
        free_couriers = list(uow.couriers.get_all_free())
        print(f"✅ Free couriers count: {len(free_couriers)} (expected: 2)")
        for courier in free_couriers:
            print(f"  - {courier.name} ({courier.id})")


def test_order_repository():
    print_header("2. Testing Order Repository")

    with UnitOfWork(DATABASE_URL) as uow:
        # 1. Create test courier for order assignment
        courier = Courier("Order Test Courier", "Truck", 2, Location(5, 5))
        uow.couriers.add(courier)

        # 2. Test add and get_by_id
        order1 = Order(uuid.uuid4(), Location(1, 1))
        uow.orders.add(order1)
        print(f"✅ Added order: {order1.id} - Status: {order1.status}")

    with UnitOfWork(DATABASE_URL) as uow:
        retrieved = uow.orders.get_by_id(order1.id)
        print(f"✅ Retrieved order: {retrieved.id} - Status: {retrieved.status}")

    with UnitOfWork(DATABASE_URL) as uow:
        # 3. Test get_one_created
        created_order = uow.orders.get_one_created()
        print(f"✅ Get one created order: {created_order.id if created_order else 'None'}")

    with UnitOfWork(DATABASE_URL) as uow:
        # 4. Test update with assignment
        order1.assign_to_courier(courier.id)
        courier.set_busy()
        uow.orders.update(order1)
        uow.couriers.update(courier)

    with UnitOfWork(DATABASE_URL) as uow:
        assigned_order = uow.orders.get_by_id(order1.id)
        print(f"✅ Assigned order to courier: {assigned_order.courier_id} - Status: {assigned_order.status}")

    with UnitOfWork(DATABASE_URL) as uow:
        # 5. Test get_all_assigned
        order2 = Order(uuid.uuid4(), Location(2, 2))
        order2.assign_to_courier(courier.id)
        uow.orders.add(order2)

    with UnitOfWork(DATABASE_URL) as uow:
        assigned_orders = list(uow.orders.get_all_assigned())
        print(f"✅ Assigned orders count: {len(assigned_orders)} (expected: 2)")
        for o in assigned_orders:
            print(f"  - Order {o.id} -> Courier {o.courier_id}")


def integration_test():
    print_header("3. Integration Test: Courier + Order")
    with UnitOfWork(DATABASE_URL) as uow:

        # 1. Create couriers
        couriers = [
            Courier("Fast Courier", "Motorcycle", 3, Location(1, 1)),
            Courier("Slow Courier", "Bicycle", 1, Location(10, 10))
        ]
        for c in couriers:
            uow.couriers.add(c)

        # 2. Create orders
        orders = [
            Order(uuid.uuid4(), Location(5, 5)),
            Order(uuid.uuid4(), Location(2, 2))
        ]
        for o in orders:
            uow.orders.add(o)

    with UnitOfWork(DATABASE_URL) as uow:
        # 3. Assign orders to couriers
        free_couriers = list(uow.couriers.get_all_free())
        created_orders = []

        while (order := uow.orders.get_one_created()) and free_couriers:
            best_courier = free_couriers.pop(0)
            order.assign_to_courier(best_courier.id)
            best_courier.set_busy()

            uow.orders.update(order)
            uow.couriers.update(best_courier)

            created_orders.append(order)
            print(f"🔹 Assigned order {order.id} to courier {best_courier.name}")

            uow.session.commit()

    with UnitOfWork(DATABASE_URL) as uow:
        # 4. Verify assignments
        assigned_orders = list(uow.orders.get_all_assigned())
        print(f"\n✅ Total assigned orders: {len(assigned_orders)}")

        busy_couriers = [c for c in uow.couriers.get_all() if c.status.name == CourierStatusValue.BUSY]
        print(f"✅ Busy couriers: {len(busy_couriers)}")

        for order in assigned_orders:
            print(f"  - Order {order.id}: {order.status} -> Courier {order.courier_id}")


def clear_database():
    with UnitOfWork(DATABASE_URL) as uow:
        print_header("Clearing Database")

        # Clear data for clean testing (order matters for FK constraints)
        uow.session.execute(text('DELETE FROM orders'))
        uow.session.execute(text('DELETE FROM couriers'))
        print("🗑️  Database cleared!")


if __name__ == "__main__":
    clear_database()
    test_courier_repository()
    test_order_repository()
    integration_test()
