def convert(df):
    """Convert the query all dataframe to a download json structure"""
    data = []
    for _, row in df.iterrows():
        parent = {
            "patient_id": row.PatientID,
            "patient_birth_date":row.PatientBirthDate,
            "study_description":row.StudyDescription,
            "study_date": row.StudyDate,
            "accession_number":row.AccessionNumber,
            "study_uid": row.StudyInstanceUID
        }
        for s in row["_childDocuments_"]:
            p = parent.copy()
            p["series_uid"] = s["SeriesInstanceUID"]
            p["series_description"] = s.get("SeriesDescription", "")
            p["series_number"] = s.get("SeriesNumber", 9999)
            data.append(p)
    return data