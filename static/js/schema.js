/**
 * A front end representation of the api's data models.
 */
AUMed.Schema = {
    Patient: function(data) {
        this.data_id = data.data_id;
        this.name = data.name;
        this.auth_id = data.auth_id;
        this.medicine = data.medicine;
        this.amount = parseInt(data.amount || 0);

        this.update = function() {};
    },
    Policy: function(data) {

    },
    History: function(data) {
        this.data_id = data.data_id;
        this.operation = data.op;
        this.old_value = data.old_Value;
        this.new_value = data.new_value;
        this.field = data.column;
        this.auth = data.auth;

        this.revert = function() {};
    },
};