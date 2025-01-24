# import os


# path = "full_file_compression_taf"

# list_dir = os.listdir(path)

# for file in list_dir:
#     if file.endswith(".txt"):
#         with open(os.path.join(path, file), "r") as f:
#             text = f.read()
#             new_txt = text[1:-1]
#             with open(os.path.join(path, file), "w") as f:
#                 f.write(new_txt)
#                 print(os.path.join(path, file))