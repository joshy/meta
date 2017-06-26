// /**
//  * Created by Yannick on 12.06.2017
//  */
// var inputData = {"patients": [ 
// 					{ "first_name": "L. Munich", "last_name": "Bram", "birthdate": "24.01.1964" }, 
// 					{ "first_name": "L. Munic", "last_name": "Bram", "birthdate": "24.01.1964" },
// 					{ "first_name": "Kein", "last_name": "Gefundener", "birthdate": "09.07.1966" }
// 				]}
// var output = [
// 	[{
// 		"groups": [{
// 			"by_AccessionNumber": {
// 				"ZH140519MR3043": [{
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [155],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917040895196947132.0.0.0",
// 					"SeriesNumber": "7",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272740290560,
// 					"id": "3"
// 				}, {
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [250],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917185841333961868.0.0.0",
// 					"SeriesNumber": "10",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272670035968,
// 					"id": "0"
// 				}]
// 			},
// 			"doclist": {
// 				"docs": [{
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [250],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917185841333961868.0.0.0",
// 					"SeriesNumber": "10",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272670035968,
// 					"id": "0"
// 				}, {
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [155],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917040895196947132.0.0.0",
// 					"SeriesNumber": "7",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272740290560,
// 					"id": "3"
// 				}],
// 				"numFound": 2,
// 				"start": 0
// 			},
// 			"groupValue": "10206705",
// 			"patient": {
// 				"birthdate": "24.01.1964",
// 				"name": "Bram^L.^Munich"
// 			}
// 		}],
// 		"matches": 2,
// 		"ngroups": 1
// 	}, {
// 		"groups": [{
// 			"by_AccessionNumber": {
// 				"ZH140519MR3043": [{
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [155],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917040895196947132.0.0.0",
// 					"SeriesNumber": "7",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272740290560,
// 					"id": "3"
// 				}, {
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [250],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917185841333961868.0.0.0",
// 					"SeriesNumber": "10",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272670035968,
// 					"id": "0"
// 				}]
// 			},
// 			"doclist": {
// 				"docs": [{
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [250],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917185841333961868.0.0.0",
// 					"SeriesNumber": "10",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272670035968,
// 					"id": "0"
// 				}, {
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [155],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917040895196947132.0.0.0",
// 					"SeriesNumber": "7",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272740290560,
// 					"id": "3"
// 				}],
// 				"numFound": 2,
// 				"start": 0
// 			},
// 			"groupValue": "10206705",
// 			"patient": {
// 				"birthdate": "24.01.1964",
// 				"name": "Bram^L.^Munich"
// 			}
// 		}],
// 		"matches": 2,
// 		"ngroups": 1
// 	}],
// 	[{
// 		"groups": [],
// 		"matches": 0,
// 		"ngroups": 0
// 	}, {
// 		"groups": [{
// 			"by_AccessionNumber": {
// 				"ZH140519MR3043": [{
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [155],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917040895196947132.0.0.0",
// 					"SeriesNumber": "7",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272740290560,
// 					"id": "3"
// 				}, {
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [250],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917185841333961868.0.0.0",
// 					"SeriesNumber": "10",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272670035968,
// 					"id": "0"
// 				}]
// 			},
// 			"doclist": {
// 				"docs": [{
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [250],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917185841333961868.0.0.0",
// 					"SeriesNumber": "10",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272670035968,
// 					"id": "0"
// 				}, {
// 					"AccessionNumber": "ZH140519MR3043",
// 					"BodyPartExamined": "Missing",
// 					"InstanceAvailability": "Missing",
// 					"InstanceNumber": [155],
// 					"InstitutionName": "Wankdorf_Pathology_Center",
// 					"Modality": "MR",
// 					"PatientBirthDate": 19640124,
// 					"PatientID": "10206705",
// 					"PatientName": "Bram^L.^Munich",
// 					"PatientSex": "M",
// 					"ProtocolName": ["t1_mpr_sag_p2_iso_256_1x1x1"],
// 					"SeriesDescription": "t1_mpr_sag_p2_iso_256_1x1x1",
// 					"SeriesInstanceUID": "1.3.12.2.1107.5.2.32.35424.2014051917040895196947132.0.0.0",
// 					"SeriesNumber": "7",
// 					"StudyDate": 20140519,
// 					"StudyDescription": "MRI_Schaedel",
// 					"StudyID": "677123",
// 					"StudyInstanceUID": "1.2.840.113619.186.35125912074.20140519114638815.700",
// 					"StudyTime": [165335.64],
// 					"_version_": 1571175272740290560,
// 					"id": "3"
// 				}],
// 				"numFound": 2,
// 				"start": 0
// 			},
// 			"groupValue": "10206705",
// 			"patient": {
// 				"birthdate": "24.01.1964",
// 				"name": "Bram^L.^Munich"
// 			}
// 		}],
// 		"matches": 2,
// 		"ngroups": 1
// 	}],
// 	[{
// 		"groups": [],
// 		"matches": 0,
// 		"ngroups": 0
// 	}, {
// 		"groups": [],
// 		"matches": 0,
// 		"ngroups": 0
// 	}]
// ];

// // call to backend
// function getData() {
// 	$.ajax({
// 		type: "POST",
// 		url: "query_patients",
// 		data: JSON.stringify(inputData),
// 		success: prepareOutputData,
// 		contentType: 'application/json',
// 		dataType: 'json'
// 	});
// }

// var matchesExact = [];
// var matchesClosest = [];
// var matchesNotfound = [];

// function prepareOutputData(data) {
// 	data = output;
// 	var patientcount = 0;

// 	$.each(data, function(key, value) {
// 		// each searched patient
// 		console.log("----- PATIENT SEARCHED " + key); 
// 		patientcount = key;

// 		$.each(data[key], function(key, value) {
// 			console.log(value);
// 			console.log(value.matches);
// 			console.log(value.ngroups);

// 			if (value.matches == 0) {
// 				// no match
// 				matchesNotfound.push(value.groups);
// 			} else {
// 				// match
// 				if (value.ngroups == 1) {
// 					// exakt match
// 					matchesExact.push(value.groups);
// 				} else {
// 					// fuzzy match
// 					matchesClosest.push(value.groups);
// 				}
// 			}
// 		});
// 	});

// 	console.log(matchesExact);
// 	console.log(matchesClosest);
// 	console.log(matchesNotfound);
// }


// // modal
// $(function() {
// 	prepareOutputData();
// })


