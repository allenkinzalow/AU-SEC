
AUMed = {
    load: function() {
        AUMed.UI.patients.open();
        AUMed.UI.timeline.open();
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
                            id: patient.auth_id,
                            name: patient.name
                        });
                    }, "")
                );

                M.AutoInit();
                $(document).on('click', '#medicineDataPolicyButton', function () {
                    console.log('clicked medicine..');
                    columnName = 'medicine'
                    AUMed.loadColumnPoliciesForUser(auth_id, columnName)
                });
                $(document).on('click', '#amountDataPolicyButton', function () {
                    console.log('clicked amount..');
                    columnName = 'amount'
                    AUMed.loadColumnPoliciesForUser(auth_id, columnName)
                });
            },
            open: function() {
                $('#patients_card').show();
                this.populate();
            },
            close: function() {
                $('#patients_card').hide();
            },
        },
        authorizations: {
            _pending_auths: [],
            open: function() {
                $('#authorization_card').show();
                this.populate();
            },
            close: function() {
                $('#authorization_card').hide();
            },
        },
        timeline: {
            _history: [],
            populate: function() {
                this._history.push(new AUMed.Schema.History({
                    data_id: "12345", 
                    op: "update",
                    old_value: "5",
                    new_value: "10",
                    column: "amount",
                }));
                this._history.push(new AUMed.Schema.History({
                    data_id: "12345", 
                    op: "update",
                    old_value: "1",
                    new_value: "5",
                    column: "amount",
                }));
                $('#timeline_table').html(
                    this._history.reduce(function(str, item) {
                        return str +  AUMed.Util.template($('#timeline_entry_template').html(), {
                            id: item.data_id,
                            color: "green",
                            icon: "lock",
                            title: item.field + " " + item.operation,
                            action: "this is a test!",
                            date: Date.now()
                        });
                    }, "")
                );
                M.AutoInit();
            },
            open: function() {
                $('#timeline_section').show();
                this.populate();
            },
            close: function() {
                $('#timeline_section').hide();
            },
        },
        policies: {
            _policies: [],
            populate: function(auth_id, columnName) {
                // todo: use API instead of hardcoding.
                this._policies.push(new AUMed.Schema.Policy({policy_id: "12345", name: "Allen Kinzalow"}));
                this._policies.push(new AUMed.Schema.Policy({policy_id: "12346", name: "Haven Barnes"}));
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

