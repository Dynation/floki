import struct
import yaml
import re

# 📝 Таблиці ідентифікаторів
sensor_table = {}
action_table = {}
state_table = {}
gait_table = {}

# 📝 Генеруємо заголовок FUF
bytecode = bytearray()
bytecode.extend(b"FUF\x00")  # MAGIC
bytecode.extend(struct.pack("<H", 0x0100))  # VERSION 1.0
bytecode.extend(b"\x00\x00\x00\x00")  # CHECKSUM (заповнимо пізніше)
bytecode.extend(struct.pack("<H", 0))  # STATE_COUNT (тимчасово)
bytecode.extend(struct.pack("<H", 0))  # GAIT_COUNT (тимчасово)
bytecode.extend(struct.pack("<H", 0))  # EVENT_COUNT (тимчасово)
bytecode.extend(struct.pack("<H", 0))  # SENSOR_COUNT (тимчасово)
bytecode.extend(struct.pack("<I", 256))  # MEMORY_SIZE
bytecode.extend(struct.pack("<H", 0))  # FLAGS

# 📌 Завантажуємо `robot.yaml`
def load_robot_config(path="robot.yaml"):
    with open(path, "r") as f:
        robot = yaml.safe_load(f)
    
    sensor_id = 1
    for sensor in robot.get("sensors", []):
        name = sensor["name"]
        sensor_table[name] = sensor_id
        bytecode.extend(struct.pack("<B", sensor_id))  # ID
        bytecode.extend(name.encode() + b"\x00")  # Назва сенсора
        sensor_id += 1

    return robot

# 📌 Компiлюємо Floki-код
def compile_floki(code):
    global bytecode
    lines = code.strip().split("\n")
    state_id, gait_id, event_id = 0x10, 0x20, 0x30

    for line in lines:
        line = line.strip()

        # 📌 Обробляємо `state`
        if line.startswith("state "):
            parts = line.split("(")
            state_name = parts[0].replace("state ", "").strip()
            params = parts[1].replace(")", "").strip() if len(parts) > 1 else ""
            
            state_table[state_name] = state_id
            bytecode.extend(struct.pack("<B", state_id))  # ID
            bytecode.extend(state_name.encode() + b"\x00")  # Назва
            bytecode.extend(params.encode() + b"\x00")  # Параметри
            state_id += 1

        # 📌 Обробляємо `gait`
        elif line.startswith("gait "):
            gait_name = line.split(" ")[1].strip().replace('"', "")
            gait_table[gait_name] = gait_id
            bytecode.extend(struct.pack("<B", gait_id))  # ID
            bytecode.extend(gait_name.encode() + b"\x00")  # Назва
            gait_id += 1

        # 📌 Обробляємо `event`
        elif line.startswith("event "):
            parts = line.replace("event ", "").split("->")
            event_chain = [x.strip() for x in parts]
            for i in range(len(event_chain) - 1):
                if event_chain[i] in sensor_table:
                    sensor_id = sensor_table[event_chain[i]]
                    state_id = state_table.get(event_chain[i + 1], 0)
                    bytecode.extend(struct.pack("<B", event_id))  # EVENT_ID
                    bytecode.extend(struct.pack("<B", sensor_id))  # SENSOR_ID
                    bytecode.extend(struct.pack("<B", state_id))  # STATE_ID
                    event_id += 1

    # 📌 Оновлюємо лічильники
    bytecode[10:12] = struct.pack("<H", len(state_table))  # STATE_COUNT
    bytecode[12:14] = struct.pack("<H", len(gait_table))  # GAIT_COUNT
    bytecode[14:16] = struct.pack("<H", event_id - 0x30)  # EVENT_COUNT
    bytecode[16:18] = struct.pack("<H", len(sensor_table))  # SENSOR_COUNT

    # 📌 Чек-суму
    checksum = sum(bytecode) % 256
    bytecode[8:12] = struct.pack("<I", checksum)

    return bytecode

# 📂 Вхідні файли
robot_config = load_robot_config()
floki_code = """
state "stand_up"(strength=1.0)
state "lie_down"
gait "walk"

event imu_pitch > 20 -> "stand_up"
event "stand_up" -> "walk"
"""

compiled_fuf = compile_floki(floki_code)

# 📂 Збереження
with open("output.fuf", "wb") as f:
    f.write(compiled_fuf)

print("✅ FUF байткод збережено в output.fuf")
