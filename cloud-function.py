def bq_load(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"Processing file: {file['name']}.")
    print(f"Processing from bucket: {file['bucket']}.")

    bucket_uri = f"gs://{file['bucket']}/{file['name']}"
    print(f"Bucket filename: {bucket_uri}")

    from google.cloud import bigquery
    client = bigquery.Client()
    # Change this to the correct dataset ID or pull it in from the environment variable
    dataset_id = 'load_test'

    # Change this to the correct table name or generate one with dates
    table = 'test_csv'

    dataset_ref = client.dataset(dataset_id)

    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.source_format = bigquery.SourceFormat.CSV
    load_job = client.load_table_from_uri(bucket_uri, dataset_ref.table(table), job_config=job_config)
    print("Starting job {}".format(load_job.job_id))

    # Waits for table load to complete.
    load_job.result()
    print("Job finished.")

    destination_table = client.get_table(dataset_ref.table(table))
    print("Loaded {} rows.".format(destination_table.num_rows))
