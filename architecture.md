## Architecture and plan

### Point 1: Cloud scheduler - extract
---
This is the google cloud scheduler, it triggers the app hosted un cloud run service.  The /extract endpoint specifically and sen the next parameters: 

* method type: POST
* bucket_name: Bucket where source file exists
* target_bucket: Bucket where result file is stored

### Point2: Cloud run - extract
---
The app "read" storage files in bucket_name, clean the datasets and merge the results into 1 file.

Finally this file (transformated - TRF) is stored into another bucket (target_bucket)

### Point 4: Cloud scheduler - metrics
---
This scheduler triggers the endpoint /metrics

* method type: POST
* source_bucket: Bucket from where the TRF file is stored
* filename: TRF filename
* dataset: name of the dataset that will contain the bigquery tables with all the metrics required.

Name for the bigquery tables is a default name and must be changed in the code directly.

### Point 5: Cloud run - metrics
---
The app "read" the TRF file from storage and calculate the metrics from it, when each requested metric is obtained the next steop is to store them in a separate table this are the default names:

* The top 10 best games for each console/company: best_concole_company
* The worst 10 games for each console/company: worst_concole_company
* The top 10 best games for all consoles: best_consoles
* The worst 10 games for all consoles: worst_consoles


## Tools used

For modeling i used StarUML because it's free and have the possibility to create data models.

For data exploration jupyter lab and pandas where used,  this because with jupyter its possible to see every step execution more clearly and do the exploratory analysis in the datasets more interactive. 

Visual Studio Code for coding with extensions for python,  its the code editor i feel mor comfortable since you can add or remove extensions.

GCP: I used cloud technologies (GCP) specifically because over onpremises technologies its more easier and quick to deploy than start a configuration from 0. Also at great scale this benefits can be seen more clearly.