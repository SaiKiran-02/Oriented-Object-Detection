import math
import os

def quad_to_yolo_angle_format(xy_coords):
    x1, y1, x2, y2, x3, y3, x4, y4 = xy_coords

    # Center of the quadrilateral
    x_center = (x1 + x2 + x3 + x4) / 4
    y_center = (y1 + y2 + y3 + y4) / 4

    # Width: distance between point 1 and 2
    width = math.hypot(x2 - x1, y2 - y1)

    # Height: distance between point 2 and 3
    height = math.hypot(x3 - x2, y3 - y2)

    # Angle: direction of first edge
    angle_rad = math.atan2(y2 - y1, x2 - x1)
    angle_deg = math.degrees(angle_rad)

    return x_center, y_center, width, height, angle_deg

def convert_quad_to_yolo_angle(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if not file.endswith(".txt"):
            continue
        in_path = os.path.join(input_folder, file)
        out_path = os.path.join(output_folder, file)

        with open(in_path, 'r') as f:
            lines = f.readlines()

        converted = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) != 9:
                continue

            class_id = parts[0]
            coords = list(map(float, parts[1:]))

            cx, cy, w, h, angle = quad_to_yolo_angle_format(coords)
            converted.append(f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f} {angle:.2f}")

        with open(out_path, 'w') as f:
            f.write("\n".join(converted))


input_quad_folder = "converted_labels"
output_final_folder = "yolo_angle_labels"

convert_quad_to_yolo_angle(input_quad_folder, output_final_folder)
print("✅ All files converted to center-based YOLO OBB format.")
