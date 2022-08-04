# currency_rate_etl_pipeline

I have created this as an intro to the world of streaming data pipelines using CLOUDAMQP platform. THe initial process calls an API to extract data then queues same on the cloudamqp. A second process consumes this data and writes to a log file. The upload script then parses the log file, extracts the data, prepares it and uploads to a MongoDB Atlas instance.

I have issues controlling the consume process as I need it to timeout after n seconds but it ignores my commands and runs then eventually terminates itself due to inactivity.

This is a beta implementation as I intend to improve on teh process with time.
