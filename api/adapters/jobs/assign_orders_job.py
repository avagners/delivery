from config import DATABASE_URL
from infrastructure.adapters.postgres.unit_of_work import UnitOfWork
from core.domain.services.dispatch_service import DispatchService
from core.application.use_cases.commands.assign_orders.assign_orders_command import AssignOrdersCommand
from core.application.use_cases.commands.assign_orders.assign_orders_handler import AssignOrdersCommandHandler


def assign_orders_job():
    unit_of_work = UnitOfWork(DATABASE_URL)
    dispatch_service = DispatchService()

    handler = AssignOrdersCommandHandler(
        unit_of_work=unit_of_work,
        dispatch_service=dispatch_service
    )

    try:
        handler.handle(AssignOrdersCommand())
        print("✅ AssignOrdersJob: заказ успешно назначен.")
    except ValueError as e:
        print(f"⚠️ AssignOrdersJob: {e}")
