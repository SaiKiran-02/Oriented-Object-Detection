import os

def convert_annotations_folder(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.txt'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            convert_annotation_file(input_path, output_path)

def convert_annotation_file(input_path, output_path):
    with open(input_path, 'r') as f:
        lines = f.readlines()

    converted = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 10:
            continue  # skip malformed lines

        x1, y1, x2, y2, x3, y3, x4, y4 = parts[:8]
        class_id = parts[9]  # move to front

        # Format: class_id x1 y1 x2 y2 x3 y3 x4 y4
        new_line = f"{class_id} {x1} {y1} {x2} {y2} {x3} {y3} {x4} {y4}"
        converted.append(new_line)

    with open(output_path, 'w') as f:
        f.write('\n'.join(converted))


input_dir = "raw_labels"
output_dir = "converted_labels"

convert_annotations_folder(input_dir, output_dir)
print(f"✅ Converted all labels from '{input_dir}' to '{output_dir}' in YOLOv8-OBB format.")
