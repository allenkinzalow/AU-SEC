
AUMed = {
    load: function() {
        AUMed.UI.nav.setup();
        AUMed.UI.patients.open();
        AUMed.UI.timeline.open();
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
                $('#patients_table').html(
                    this._patients.reduce(function(str, patient) {
                        return str +  AUMed.Util.template($('#patient_entry_template').html(), {
                            id: patient.data_id,
                            auth_id: patient.auth_id,
                            name: patient.name,
                        });
                    }, "")
                );

                $(document).on('click', '.btn-medicine-policy', function () {
                    var id = $(this).parents('li').first().data('auth-id');
                    console.log(id);
                    AUMed.UI.policies.open(id, 'medicine');
                });

                $(document).on('click', '.btn-amount-policy', function () {
                    var id = $(this).parents('li').first().data('auth-id');
                    console.log(id);
                    AUMed.UI.policies.open(id, 'amount');
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
            open: function(data_id) {
                var self = this;
                $('#timeline_section').show();
                AUMed.Util.api({
                    url: 'history/' + data_id,
                    callback: (data) => { 
                        data.forEach(d => {
                            self._patients.push(new AUMed.Schema.History(d));
                        });
                        self.populate();
                    }
                });
            },
            close: function() {
                $('#timeline_section').hide();
            },
        },
        policies: {
            _policies: [],
            populate: function() {                
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
            },
            open: function(auth_id, column_name) {
                var self = this;
                AUMed.Util.api({
                    url: 'policies/get_policies',
                    type: 'POST',
                    data: {
                        'column_names': [column_name],
                        'auth_ids': [auth_id]
                    },
                    callback: (data) => { 
                        data.forEach(d => {
                            console.log(d);
                            self._policies.push(new AUMed.Schema.Policy(d));
                        });
                        self.populate();
                    }
                });
            },
        },
    },
};

$(document).ready(() => {
    M.AutoInit();
    AUMed.load();
});

