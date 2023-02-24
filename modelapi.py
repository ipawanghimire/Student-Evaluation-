from flask import Flask, request, jsonify
import numpy as np
import pandas as pd
import pickle
from bson.objectid import ObjectId
from pymongo import MongoClient

client = MongoClient(
    "mongodb+srv://arb12345:majorproject@cluster0.iqbqh.mongodb.net/Student?retryWrites=true&w=majority")
# Get the database and collection
db = client["Student"]
collection = db["StudentEvaluationRecords"]

app = Flask(__name__)
with open("model.pkl", "rb") as f:
    clf = pickle.load(f)


@app.route('/predict', methods=['POST'])
def predict():
    csv_file = request.files['file']

    snrona = []
    newcsv = []
    df = pd.read_csv(csv_file)

    arr = df.to_numpy()

    for i, row in df.iterrows():

        sn = arr[i, 0]
        rollno = arr[i, 1]
        name = arr[i, 2]
        if (arr[i, 4] == 'BCT'):
            fac = 2
        if (arr[i, 4] == 'BCE'):
            fac = 1
        if (arr[i, 4] == 'BEX'):
            fac = 3
        if (arr[i, 4] == 'BEL'):
            fac = 4

        x = [arr[i, 3], fac, arr[i, 6], arr[i, 7], arr[i, 8]]

        x = np.asarray(x)
        x = x.reshape(1, -1)
        predictions = clf.predict(x)
        #predictions = predictions.astype(int)
        #predictions = pd.DataFrame(predictions)
        # print(predictions)
        if predictions == 1:
            remarks = 'High chance of passing with good marks, keep it up'
        elif predictions == 2:
            remarks = 'High chance of passing,need more preperation for better marks'
        elif predictions == 3:
            remarks = 'High chance of scoring around passing marks,need more preperation'
        elif predictions == 4:
            remarks = 'Chances of failing in one or two subjects,need more preperation'
        elif predictions == 5:
            remarks = 'High chances of failing in few subjects,Better cover important and sure questions properly'
        elif predictions == 6:
            remarks = 'High chances of mailing in most of the subjects, better drop few subjects to focus on the rest'

        snrona = {
            "sn": sn,
            "rollno": rollno,
            "name": name,
            "faculty": arr[i, 4],
            "semester": arr[i, 3],
            "attendanceScore": arr[i, 6],
            "assignmentScore": arr[i, 7],
            "assessmentScore": arr[i, 8],
            "prediction": int(predictions[0]),
            "remarks": remarks,
        }
        result = collection.insert_one(snrona)

        snrona["_id"] = str(result.inserted_id)
        newcsv.append(snrona)
       # newcsv.append(snrona)
        # collection.insert_one(snrona)
    return jsonify({'prediction': newcsv})


@app.route('/predict', methods=['GET'])
def get_records():
    records = []
    for record in collection.find():
        record['_id'] = str(record['_id'])
        records.append(record)
    return jsonify({'records': records})


@app.route('/predict/<rollno>', methods=['GET'])
def get_records_by_rollno(rollno):
    records = []
    for record in collection.find({'rollno': rollno}):
        record['_id'] = str(record['_id'])
        records.append(record)
    return jsonify({'records': records})


if __name__ == '__main__':
    app.run(port=6060)
