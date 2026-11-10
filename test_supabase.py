from components.database import get_pothole_detections, get_road_reports

detections = get_pothole_detections()
reports = get_road_reports()

print("Pothole detections:", len(detections))
print("Road reports:", len(reports))

for item in detections:
    print(item["location"], "-", item["severity"])