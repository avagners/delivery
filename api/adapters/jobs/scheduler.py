from apscheduler.schedulers.background import BackgroundScheduler
from api.adapters.jobs.assign_orders_job import assign_orders_job
from api.adapters.jobs.move_couriers_job import move_couriers_job


def start_jobs():
    scheduler = BackgroundScheduler()

    scheduler.add_job(assign_orders_job, 'interval', seconds=1, id='assign_orders_job')
    scheduler.add_job(move_couriers_job, 'interval', seconds=2, id='move_couriers_job')

    scheduler.start()
    print("🔥 Background Jobs Scheduler запущен!")

    return scheduler
