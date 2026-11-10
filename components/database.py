from components.supabase_client import supabase


def get_pothole_detections():
    try:
        response = (
            supabase
            .table("pothole_detections")
            .select("*")
            .order("detected_at", desc=True)
            .execute()
        )

        return response.data

    except Exception as e:
        print("Error fetching pothole detections:", e)
        return []


def get_road_reports():
    try:
        response = (
            supabase
            .table("road_reports")
            .select("*")
            .order("reported_at", desc=True)
            .execute()
        )

        return response.data

    except Exception as e:
        print("Error fetching road reports:", e)
        return []