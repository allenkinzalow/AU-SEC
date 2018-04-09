
AUMed = {
    load: function() {
        AUMed.UI.nav.setup();
        AUMed.UI.patients.open();
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
                            medicine: patient.medicine,
                            amount: patient.amount,
                        });
                    }, "")
                );

                this._patients.forEach(p => {
                    $("#medicine_type_" + p.auth_id).focus();
                    $("#medicine_type_" + p.auth_id + " option")
                    .removeAttr('selected')
                    .filter('[value=' + p.medicine + "]")
                    .attr('selected', 'selected')
                });

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

                $(document).on('click', '.btn-timeline-policy', function () {
                    var id = $(this).parents('li').first().data('id');
                    console.log(id);
                    AUMed.UI.patients.close();
                    AUMed.UI.timeline.open(id);
                });

                M.AutoInit();
            },
            open: function() {
                var self = this;
                $('#patients_card').show();
                AUMed.Util.api({
                    url: 'patients',
                    callback: (data) => { 
                        if (!data['error']) {
                            data.forEach(d => {
                                self._patients.push(new AUMed.Schema.Patient(d));
                            });
                        }
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
                var html = this._history.reduce(function(str, item) {
                    return str +  AUMed.Util.template($('#timeline_entry_template').html(), {
                        id: item.data_id,
                        color: "green",
                        icon: "lock",
                        title: item.field + " " + item.operation,
                        action: "this is a test!",
                        date: Date.now()
                    });
                }, "");
                if(html == "")
                    html = "No activity found.";
                $('#timeline_table').html(html);
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
            populate: function(column_name) {
                this._policies = this._policies.filter(p => p.policy_bitwise != 0);
                this.updatePolicies = this._policies.filter(p => p.bit_test(6) || p.bit_test(5));
                this.deletePolicies = this._policies.filter(p => p.bit_test(4) || p.bit_test(3));
                this.selectPolicies = this._policies.filter(p => p.bit_test(2) || p.bit_test(1));

                $('#update_policies_table').html(
                    this.updatePolicies.reduce(function(str, policy) {
                        return str +  AUMed.Util.template($('#policy_entry_template').html(), {
                            id: policy.policy_id,
                            auth: policy.bit_test(6),
                            notify: policy.bit_test(5),
                        });
                    }, "")
                );

                var chipData = {};
                AUMed.UI.patients._patients.forEach((p) => {
                    p.image = '';
                    p.tag = p.name;
                    chipData[p.name] = null;
                });
                $('.chips-autocomplete').chips({
                    autocompleteOptions: {
                      data: chipData,
                      limit: Infinity,
                      minLength: 1
                    }
                  });

                this.updatePolicies.forEach(p => {
                    var selectedVal = p.bit_test(6) ? "2" : "1"
                    $("#policy_type_" + p.policy_id + " option")
                    .removeAttr('selected')
                    .filter('[value=' + selectedVal + "]")
                    .attr('selected', 'selected')
                    p.image = '';
                    p.tag = p.name;
                    M.Chips.getInstance($("#authy_id_" + p.policy_id)).addChip(p);
                });
                
                $('#delete_policies_table').html(
                    this.deletePolicies.reduce(function(str, policy) {
                        return str +  AUMed.Util.template($('#policy_entry_template').html(), {
                            id: policy.policy_id,
                            auth: policy.bit_test(4),
                            notify: policy.bit_test(3),
                        });
                    }, "")
                );
                this.deletePolicies.forEach(p => {
                    var selectedVal = p.bit_test(4) ? "2" : "1"
                    $("#policy_type_" + p.policy_id + " option")
                    .removeAttr('selected')
                    .filter('[value=' + selectedVal + "]")
                    .attr('selected', 'selected')
                    p.image = '';
                    p.tag = p.name;
                    M.Chips.getInstance($("#authy_id_" + p.policy_id)).addChip(p);
                });

                $('#select_policies_table').html(
                    this.selectPolicies.reduce(function(str, policy) {
                        return str +  AUMed.Util.template($('#policy_entry_template').html(), {
                            id: policy.policy_id,
                            auth: policy.bit_test(2),
                            notify: policy.bit_test(1),
                        });
                    }, "")
                );

                this.selectPolicies.forEach(p => {
                    var selectedVal = p.bit_test(2) ? "2" : "1"
                    $("#policy_type_" + p.policy_id + " option")
                    .removeAttr('selected')
                    .filter('[value=' + selectedVal + "]")
                        .attr('selected', 'selected')
                    p.image = '';
                    p.tag = p.name;
                    M.Chips.getInstance($("#authy_id_" + p.policy_id)).addChip(p);
                });

                $('.column-name-header').html(AUMed.Util.capitalize(column_name));

                $(document).on('click', '.btn-delete-policy', function () {
                    var id = $(this).parents('li').first().data('auth-id');
                    console.log(id);
                    AUMed.UI.policies.open(id, 'amount');
                });
                
                M.AutoInit();
                elem = document.querySelector('#dataPolicyModal');
                instance = M.Modal.init(elem, );
                instance.open();
            },
            open: function(auth_id, column_name) {
                this._policies = [];
                var self = this;
                AUMed.Util.api({
                    url: 'policies/get_policies',
                    type: 'POST',
                    data: {
                        'column_names': [column_name],
                        'auth_ids': [auth_id]
                    },
                    callback: (data) => { 
                        allPolicies = data['policies'];
                        (allPolicies || []).forEach(p => {
                            console.log(p);
                            self._policies.push(new AUMed.Schema.Policy(p));
                        });
                        self.populate(column_name);
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

