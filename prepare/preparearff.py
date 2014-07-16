# -*- coding: latin-1 -*-
__author__ = 'kosttek'


class PrepareArff():

    value_true = "y"
    value_false = "n"
    value_empty = "?"

    var_domian = "y"

    truefalse_vals = False

    def __init__(self, truefalse_vals = False):
        if truefalse_vals == True:
            self.truefalse_vals = True
            self.value_empty=self.value_false
        self.set_var_domain()

    def prepare_bool_association_file(self, relation_name, variables_set, bool_data):
        f = open(relation_name+".arff", "w")
        self.write_relation(f, relation_name)
        self.write_boolean_atributes(f, variables_set)
        self.write_boolean_values(f, bool_data)


    def write_relation(self,file_des, relation_name):
        file_des.write("@relation "+relation_name+"\n")

    def write_boolean_atributes(self,file_des,variables_set):
        file_des.write("\n")
        self.write_boolean_atributes_without_newline(file_des,variables_set)
        #for var in variables_set:
        #    PrepareArff.write_boolean_var(file_des,var)

    def write_boolean_atributes_without_newline(self,file_des,variables_set):
        for var in variables_set:
            self.write_boolean_var(file_des,var)

    def write_boolean_var(self,file_des, var):
        var_filtered = PrepareArff.filterVar(var)
        file_des.write(("@attribute "+var_filtered+" {"+self.var_domian+"}\n").encode('utf-8'))

    def set_var_domain(self,):
        if self.truefalse_vals:
            self.var_domian = self.value_true+","+self.value_false
        else:
            return self.value_true

    @staticmethod
    def filterVar(var):
        var = var.replace("%", "<pr>")
        var = var.replace("\\n", "")
        var = var.replace("\\r", "")
        var = var.replace("\"", "||")
        var = var.replace("\'", "|")
        var = var.replace("{", "((")
        var = var.replace("}", "))")
        var = var.replace("\t", "_tab_")
        var_no_withespaces = var.replace(" ", "_")
        var_no_comma = var_no_withespaces.replace(",", ";")
        return var_no_comma

    def write_boolean_values(self, file_des, vals):
        file_des.write("\n")
        file_des.write("\n")
        file_des.write("@data\n")
        for val_array in vals:
            self.write_boolean_val_line(file_des,val_array)

    def get_boolean_val_line(self, val_array):
        result = ""
        for bool_val in val_array:
            if bool_val:
                val = self.value_true
            else:
                val = self.value_empty
            result += val+","
        result = result[0:-1]
        return result

    def write_boolean_val_line(self,file_des,val_array):
        result = self.get_boolean_val_line(val_array)
        file_des.write(result+"\n")