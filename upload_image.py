from components.supabase_client import supabase

image_path = "pothole_0538.jpg"
bucket_name = "pothole-images"
file_name = "pothole_0538_retry.jpg"

try:
    with open(image_path, "rb") as image:
        result = supabase.storage.from_(bucket_name).upload(
            file_name,
            image,
            file_options={
                "content-type": "image/jpeg"
            }
        )

    print("UPLOAD SUCCESSFUL!")
    print(result)

    image_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
    print("IMAGE URL:", image_url)

except Exception as e:
    print("UPLOAD FAILED!")
    print(repr(e))