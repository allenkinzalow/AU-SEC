/**
 * A front end representation of the api's data models.
 */
AUMed.Schema = {
    Patient: function(data) {
        this.name = data.name;
        this.auth_id = data.auth_id;
        this.data_id = data.data_id;
        this.medicine = data.medicine;
        this.amount = parseInt(data.amount || 0);

        this.update = function() {

        };
    },
    Policy: function(data) {
        this.policy_id = data.policy_id;
        this.data_id = data.data_id;
        this.group_id = data.group_id;
        this.column_name = data.column_name;
        this.table_name = data.table_name;
        this.expiration = data.expiration;
        this.policy_bitwise = data.policy_bitwise;
        this.group_members = data.group_members;

        this.create = function(data) {
            AUMed.Util.api({
                url: 'policies/create_policy',
                type: 'POST',
                data: {
                    data
                },
                callback: (data) => { 
                    return data;
                }
            });
        };

        this.update = function() {

        };

        this.bit_test = function(bit) {
            return ((this.policy_bitwise>>bit) % 2 != 0);
        };
    },
    History: function(data) {
        this.data_id = data.data_id;
        this.operation = data.operation;
        this.time_stamp = data.time_stamp;
        this.old_value = data.old_value;
        this.new_value = data.new_value;
        this.field = data.column;
        this.auth_id = data.auth_id;

        this.revert = function() {};
    },
};