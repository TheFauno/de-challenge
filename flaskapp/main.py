import os

from flask import Flask

from webargs import fields
from webargs.flaskparser import use_args

from modules import storage, utils

# Initialise flask app
app = Flask(__name__)

# Files extraction from storage bucket, 
# data preprocessing, 
# datasets merge
@app.route("/extract", methods=["POST"])
@use_args({"bucket_name": fields.Str(required=True), "target_bucket": fields.Str(required=True)})
def extract_files(args):
    bucket_name = args["bucket_name"]
    target_bucket = args["target_bucket"]
    filenames = ('result.csv','consoles.csv')
    result = storage.get_data(bucket_name,filenames[0])
    consoles = storage.get_data(bucket_name,filenames[1])
    # preprocessing dataset result
    ## trim field console
    fields_to_trim = ('console')
    result_trimmed = utils.trim(result, fields_to_trim)
    ## format date
    fields_to_date_format = ('date')
    date_format = '%Y-%m-%d'
    actual_date_format = '%b %d, %Y'
    result_date_formated = utils.format_date(result_trimmed, actual_date_format, date_format,fields_to_date_format)
    ## merge datasets into 1
    fields = ('console')
    merged_file = utils.merge(result_date_formated,consoles,fields)
    ## dataframe to buffer
    file_stream = utils.dataframe_to_buffer(merged_file)
    ## store file
    code_response, message = storage.upload(target_bucket,file_stream)
    return "{}:{}".format(message, code_response)

@app.route("/metrics", methods=["POST"])
@use_args(argmap={
    "source_bucket": fields.Str(required=True),
    "filename": fields.Str(required=True),
    "dataset": fields.Str(required=True)
    })
def calculate_metrics(args):
    consolidated_data = storage.get_data(args.source_bucket, (args.filename))
    code_response, message = 200,"metrics loaded succesfully"
    # Metrics
    # The top 10 best games for each console/company.
    # The worst 10 games for each console/company.
    # The top 10 best games for all consoles.
    # The worst 10 games for all consoles.
    try:
        t_10_b_cc,w_10_cc,t_10_b_c,w_10_c = utils.obtain_metrics(consolidated_data)
        utils.load_to_bq(t_10_b_cc,args.dataset+'.'+'best_concole_company')
        utils.load_to_bq(w_10_cc,args.dataset+'.'+'worst_concole_company')
        utils.load_to_bq(t_10_b_c,args.dataset+'.'+'best_consoles')
        utils.load_to_bq(w_10_c,args.dataset+'.'+'worst_consoles')
        return "{}:{}".format(message, code_response)
    except:
        code_response = 500
        message = "error in metrics/loading to bigquery process"
        return "{}:{}".format(message, code_response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
