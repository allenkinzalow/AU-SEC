
AUMed = {
    load: function() {
        AUMed.UI.patients.populate();
    },
    loadColumnPoliciesForUser: function(auth_id, columnName) {
        AUMed.UI.policies.populate(auth_id, columnName);
    },
    UI: {
        patients: {
            _patients: [],
            populate: function() {
                // todo: use API instead of hardcoding.
                this._patients.push(new AUMed.Schema.Patient({auth_id: "12345", name: "Allen Kinzalow"}));
                this._patients.push(new AUMed.Schema.Patient({auth_id: "12346", name: "Haven Barnes"}));
                $('#patients_table').html(
                    this._patients.reduce(function(str, patient) {
                        return str +  AUMed.Util.template($('#patient_entry_template').html(), {
                            id: patient.data_id,
                            name: patient.name
                        });
                    }, "")
                );
                M.AutoInit();
                $("#medicineDataPolicyButton").click(function () {
                    columnName = "medicine"
                    AUMed.loadColumnPoliciesForUser(auth_id, columnName)
                });
                $("#amountDataPolicyButton").click(function () {
                    columnName = "amount"
                    AUMed.loadColumnPoliciesForUser(auth_id, columnName)
                });
            },
        },
        policies: {
            _policies: [],
            populate: function(auth_id, columnName) {
                // todo: use API instead of hardcoding.
                this._policies.push(new AUMed.Schema.Policy({data_id: "12345", name: "Allen Kinzalow"}));
                this._policies.push(new AUMed.Schema.Policy({data_id: "12346", name: "Haven Barnes"}));
                $('#policies_table').html(
                    this._patients.reduce(function(str, patient) {
                        return str +  AUMed.Util.template($('#policy_entry_template').html(), {
                            id: patient.data_id,
                            name: patient.name
                        });
                    }, "")
                );
                M.AutoInit();
            }
        },
        authorizations: {},
        timeline: {},
    },
};

$(document).ready(() => {
    M.AutoInit();
    AUMed.load();
});

