from google.cloud import storage
from io import StringIO

def get_data(bucket_name,filename):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    string_results = ""
    try:
        blob = bucket.get_blob(filename)
        string_results = StringIO(blob.download_as_string())
    except:
        print("Couln't find requested bucket or files")
    return string_results

def upload(bucket_name, filename):
    client = storage.Client()
    try:
        bucket = client.get_bucket(bucket_name)
        data_object = 'consoles_results.csv'
        blob = bucket.blob(filename)
        blob.upload_from_filename(data_object)
        return (200,'uploaded file succesfully')
    except:
        return (500,'Upload process has failed')