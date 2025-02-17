import os
import json
from django.core.management.base import BaseCommand
from viewers.models import Viewer
from datetime import datetime, time
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = "Insert Viewer data from a JSON file"

    def handle(self, *args, **kwargs):
        # Define the path to the JSON file
        file_path = os.path.join(os.path.dirname(__file__), "../../viewers.json")

        try:
            # Open the JSON file and read it using UTF-8 encoding
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            # Extract the "data" from the JSON
            viewer_records = data.get("data", [])

            # Initialize a list to Viewer objects
            viewer_objects = []
            for record in viewer_records:
                viewer_objects.append(Viewer(
                    location_id=record["location_id"],
                    period_start=make_aware(datetime.fromisoformat(record["period_start"])),
                    period_start_date=make_aware(datetime.combine(
                        datetime.fromisoformat(record["period_start_date"]).date(),
                        time.min  # Ensure the minimum time (00:00:00)
                    )),
                    period_start_time=time.fromisoformat(record["period_start_time"]),
                    very_happy=record["very_happy"],
                    happy=record["happy"],
                    neutral=record["neutral"],
                    unhappy=record["unhappy"],
                    very_unhappy=record["very_unhappy"],
                    gender=record["gender"],
                    age=record["age"],
                    dwell_time_in_tenths_of_sec=record["dwell_time_in_tenths_of_sec"],
                    attention_time_in_tenths_of_sec=record["attention_time_in_tenths_of_sec"],
                    age_value=record["age_value"]
                ))

            # Bulk insert the data into the database
            Viewer.objects.bulk_create(viewer_objects)

            # Output a success message with the number of inserted records
            self.stdout.write(self.style.SUCCESS(f"Inserted {len(viewer_objects)} records into the Viewer table."))

        except FileNotFoundError:
            # Output an error message if the file is not found
            self.stderr.write(self.style.ERROR(f"File not found at {file_path}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inserting data: {e}"))
