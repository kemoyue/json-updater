# this script merge [en_us.json] and [xx_xx.json] file to the new [output.json] file
# add new untranslated fields while keeping translated fields

import sys, ast, json
path = sys.path [0]
xx_xx_filename = "zh_cn.json"
tab = "\t"; cl = ": "; cm = ","; nl = "\n" # manual

en_us_file = open(path + "/en_us.json", encoding='utf-8', mode='r')
en_us_lines = en_us_file.readlines()
en_us_file.seek(0) # reset the read cursor
en_us_pairs = json.load(en_us_file)
xx_xx_file = open(path + "/" + xx_xx_filename, encoding='utf-8', mode='r')
xx_xx_pairs = json.load(xx_xx_file)
output_file = open(path + "/output.json", encoding='utf-8', mode='w')
output_lines = []

total_kv_line_num = len(en_us_pairs) # kv: key and value
current_kv_line_num = 0

for line in en_us_lines:
    line_result = line
    if line.strip().startswith("\""):
        current_kv_line_num = current_kv_line_num + 1
        if current_kv_line_num == total_kv_line_num:
            cm = ""
        line = "{" + line + "}"
        (key, value) = ast.literal_eval(line).popitem() # parse str to dict, ...
        value = xx_xx_pairs.get(key)
        if value:
            value = value.replace(r'"', r'\"')
            value = value.replace(r'\\', r'\\\\')
            line_result = "{}\"{}\"{}\"{}\"{}{}".format(tab, key, cl, value, cm, nl)
    output_lines.append(line_result)

output_file.writelines(output_lines); output_file.close()
print("JSON file merge complete!")
