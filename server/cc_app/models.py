import mongoengine as me
import datetime

# Create your models here.


class Expense(me.Document):
    #user = me.ReferenceField(me.User, required=True, reverse_delete_rule=me.CASCADE)
    description = me.StringField(max_length=200, required=True)
    #sharable_flag = me.BooleanField(required=True)
    #tax_flag = me.BooleanField(required=True)
    created_date = me.DateTimeField(default=datetime.datetime.now)
    modified_date = me.DateTimeField(default=datetime.datetime.now)
    image = me.FileField()
    #start_date = me.DateTimeField()
    #end_date = me.DateTimeField()
    #total_amt = me.DecimalField(precision=2)

