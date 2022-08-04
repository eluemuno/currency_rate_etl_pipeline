# currency_rate_etl_pipeline

I have created this as an intro to the world of streaming data pipelines using CLOUDAMQP platform. 

The initial process [extract_and_queue] calls an API to extract data then queues same on the cloudamqp. A second process [consume_messages] consumes this data and writes to a log file. Then the upload script [load_into_mongodb] then parses the log file, extracts the data, prepares it into json format and uploads to a MongoDB Atlas instance.

I currently have issues controlling the consume process as I need it to timeout after n seconds but it ignores my commands and runs then eventually terminates itself due to inactivity.

This is a beta implementation as I intend to improve on teh process with time.
