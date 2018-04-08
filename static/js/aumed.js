
AUMed = {
    load: function() {
        
        AUMed.UI.patients.populate();
    },
    UI: {
        patients: {
            _patients: [],
            populate: function() {
                // todo: use API instead of hardcoding.
                this._patients.push(new AUMed.Schema.Patient({data_id: "12345", name: "Allen Kinzalow"}));
                this._patients.push(new AUMed.Schema.Patient({data_id: "12346", name: "Haven Barnes"}));
                $('#patients_table').html(
                    this._patients.reduce(function(str, patient) {
                        return str +  AUMed.Util.template($('#patient_entry_template').html(), {
                            id: patient.data_id,
                            name: patient.name
                        });
                    }, "")
                );
                M.AutoInit();
            },
        },
        authorizations: {},
        timeline: {},

    },
};

$(document).ready(() => {
    M.AutoInit();
    AUMed.load();
});