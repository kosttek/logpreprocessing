__author__ = 'kosttek'

class PrepareArff():
    def prepare_bool_association_file(self, relation_name, variables_set, bool_data):
        f = open(relation_name+".arff","w")
        self.write_relation(f, relation_name)
        self.write_boolean_atributes(f,variables_set)
        self.write_boolean_values(f,bool_data)


    @staticmethod
    def write_relation(file_des, relation_name):
        file_des.write("@relation "+relation_name+"\n")

    @staticmethod
    def write_boolean_atributes(file_des,variables_set):
        file_des.write("\n")
        for var in variables_set:
            PrepareArff.write_boolean_var(file_des,var)

    @staticmethod
    def write_boolean_var(file_des, var):
        var_filtered = PrepareArff.filterVar(var)
        file_des.write("@attribute "+var_filtered+" {True,False}\n")

    @staticmethod
    def filterVar(var):
        var = var.replace("%","<pr>")
        var = var.replace("\\n","")
        var = var.replace("\\r","")
        var = var.replace("\"","||")
        var = var.replace("\'","|")
        var = var.replace("{","((")
        var = var.replace("}","))")
        var = var.replace("\t","_tab_")
        var_no_withespaces = var.replace(" ","_")
        var_no_comma = var_no_withespaces.replace(",",";")
        return var_no_comma

    @staticmethod
    def write_boolean_values(file_des,vals):
        file_des.write("\n")
        file_des.write("\n")
        file_des.write("@data\n")
        for val_array in vals:
            PrepareArff.write_boolean_val_line(file_des,val_array)

    @staticmethod
    def write_boolean_val_line(file_des,val_array):
        result = ""
        for bool_val in val_array:
            result += str(bool_val)+","
        result = result[0:-1]
        file_des.write(result+"\n")