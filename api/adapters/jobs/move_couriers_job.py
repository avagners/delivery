from config import DATABASE_URL
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from core.application.use_cases.commands.move_couriers.move_couriers_command import MoveCouriersCommand
from core.application.use_cases.commands.move_couriers.move_couriers_handler import MoveCouriersCommandHandler


def move_couriers_job():
    unit_of_work = UnitOfWork(DATABASE_URL)

    handler = MoveCouriersCommandHandler(unit_of_work)

    try:
        handler.handle(MoveCouriersCommand())
        print("🚚 MoveCouriersJob: курьеры успешно перемещены.")
    except ValueError as e:
        print(f"⚠️ MoveCouriersJob: {e}")
