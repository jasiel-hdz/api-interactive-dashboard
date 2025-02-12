import os
import json
from django.core.management.base import BaseCommand
from ots.models import OTS
from datetime import datetime, time
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = "Insert OTS data from a JSON file"

    def handle(self, *args, **kwargs):
        # Define the path to the JSON file
        file_path = os.path.join(os.path.dirname(__file__), "../../ots.json")

        try:
            # Open the JSON file and read it using UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Extract the "data" from the JSON
            ots_records = data.get("data", [])

            # Initialize a list to OTS
            ots_objects = []
            for record in ots_records:
                ots_objects.append(OTS(
                    location_id=record["location_id"],
                    period_start=make_aware(datetime.fromisoformat(record["period_start"])),
                    period_start_date=make_aware(datetime.fromisoformat(record["period_start_date"]).date()),
                    # Use time.fromisoformat() for time strings
                    period_start_time=time.fromisoformat(record["period_start_time"]),
                    ots_count=record["ots_count"],
                    duration=record["duration"],
                    watcher_count=record["watcher_count"]
                ))

            OTS.objects.bulk_create(ots_objects)

            # Output a success message with the number of inserted records
            self.stdout.write(self.style.SUCCESS(f"Inserted {len(ots_objects)} records into the OTS table."))

        except FileNotFoundError:
            # Output an error message if the file is not found
            self.stderr.write(self.style.ERROR(f"File not found at {file_path}"))
        except Exception as e:
            # Output a generic error message for any other exception
            self.stderr.write(self.style.ERROR(f"Error inserting data: {e}"))
