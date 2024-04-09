full_path = os.path.join(data_path, entry)
                if os.path.isfile(full_path):
                    non_image_files.append(entry)
                elif os.path.isdir(full_path):
                    subdirectories.append(entry)