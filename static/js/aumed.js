
AUMed = {
    load: function() {
        AUMed.UI.nav.setup();
        AUMed.UI.patients.open();
        AUMed.UI.timeline.open();
    },
    loadColumnPoliciesForUser: function(auth_id, columnName) {
        AUMed.UI.policies.populate(auth_id, columnName);
    },
    UI: {
        nav: {
            setup: function() {
                if (AUMed.Util.isDoctor()) {
                    $('#user-label').html('Doctor View');
                } else {
                    $('#user-label').html('Patient View');
                }
                
                $(document).on('click', '#switch_account', function () {
                    AUMed.Util.toggleUserType();
                });
            }
        },
        patients: {
            _patients: [],
            populate: function() {
                // todo: use API instead of hardcoding.
                $('#patients_table').html(
                    this._patients.reduce(function(str, patient) {
                        return str +  AUMed.Util.template($('#patient_entry_template').html(), {
                            id: patient.auth_id,
                            name: patient.name
                        });
                    }, "")
                );

                $(document).on('click', '.btn-medicine-policy', function () {
                    var id = $(this).parents('li').first().data('id');
                    console.log(id);
                    AUMed.loadColumnPoliciesForUser(id, 'medicine')
                });

                $(document).on('click', '.btn-amount-policy', function () {
                    AUMed.loadColumnPoliciesForUser('12345', 'amount')
                });

                M.AutoInit();
                
            },
            open: function() {
                var self = this;
                $('#patients_card').show();
                AUMed.Util.api({
                    url: 'patients',
                    callback: (data) => { 
                        data.forEach(d => {
                            self._patients.push(new AUMed.Schema.Patient(d));
                        });
                        self.populate();
                    }
                });
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
                initializeTimeline();
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
                this._policies = [];

                // todo: use API instead of hardcoding.s
                this._policies.push(new AUMed.Schema.Policy({policy_id: "12345", group_id: "93939"}));
                this._policies.push(new AUMed.Schema.Policy({policy_id: "12346", group_id: "21919"}));
                
                $('#policies_table').html(
                    this._policies.reduce(function(str, patient) {
                        return str +  AUMed.Util.template($('#policy_entry_template').html(), {
                            id: patient.data_id,
                            name: patient.name
                        });
                    }, "")
                );
                
                M.AutoInit();
                elem = document.querySelector('#dataPolicyModal');
                instance = M.Modal.init(elem, );
                instance.open();
            }
        },
    },
};

$(document).ready(() => {
    M.AutoInit();
    AUMed.load();
});

