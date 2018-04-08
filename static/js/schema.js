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
};